import cv2
import numpy as np 
from skimage import color, feature
from scipy.stats import kurtosis
from PIL import Image,ImageDraw
import requests
import re
import os
import json
from datetime import datetime
import threading
from DataStoreSet import DataStore

def download_tile(url, headers, channels):
    response = requests.get(url, headers=headers)
    arr =  np.asarray(bytearray(response.content), dtype=np.uint8)
    if channels == 3:
        return cv2.imdecode(arr, 1)
    return cv2.imdecode(arr, -1)

def project_with_scale(lat, lon, scale):
    siny = np.sin(lat * np.pi / 180)
    siny = min(max(siny, -0.9999), 0.9999)
    x = scale * (0.5 + lon / 360)
    y = scale * (0.5 - np.log((1 + siny) / (1 - siny)) / (4 * np.pi))
    return x, y

def download_image(lat1: float, lon1: float, lat2: float, lon2: float,
    zoom: int, url: str, headers: dict, tile_size: int = 256, channels: int = 3) -> np.ndarray:
    scale = 1 << zoom
    tl_proj_x, tl_proj_y = project_with_scale(lat1, lon1, scale)
    br_proj_x, br_proj_y = project_with_scale(lat2, lon2, scale)
    tl_pixel_x = int(tl_proj_x * tile_size)
    tl_pixel_y = int(tl_proj_y * tile_size)
    br_pixel_x = int(br_proj_x * tile_size)
    br_pixel_y = int(br_proj_y * tile_size)
    tl_tile_x = int(tl_proj_x)
    tl_tile_y = int(tl_proj_y)
    br_tile_x = int(br_proj_x)
    br_tile_y = int(br_proj_y)
    img_w = abs(tl_pixel_x - br_pixel_x)
    img_h = br_pixel_y - tl_pixel_y
    img = np.zeros((img_h, img_w, channels), np.uint8)
    def build_row(tile_y):
        for tile_x in range(tl_tile_x, br_tile_x + 1):
            tile = download_tile(url.format(x=tile_x, y=tile_y, z=zoom), headers, channels)
            if tile is not None:
                # Find the pixel coordinates of the new tile relative to the image
                tl_rel_x = tile_x * tile_size - tl_pixel_x
                tl_rel_y = tile_y * tile_size - tl_pixel_y
                br_rel_x = tl_rel_x + tile_size
                br_rel_y = tl_rel_y + tile_size
                # Define where the tile will be placed on the image
                img_x_l = max(0, tl_rel_x)
                img_x_r = min(img_w + 1, br_rel_x)
                img_y_l = max(0, tl_rel_y)
                img_y_r = min(img_h + 1, br_rel_y)
                # Define how border tiles will be cropped
                cr_x_l = max(0, -tl_rel_x)
                cr_x_r = tile_size + min(0, img_w - br_rel_x)
                cr_y_l = max(0, -tl_rel_y)
                cr_y_r = tile_size + min(0, img_h - br_rel_y)
                img[img_y_l:img_y_r, img_x_l:img_x_r] = tile[cr_y_l:cr_y_r, cr_x_l:cr_x_r]
    threads = []
    for tile_y in range(tl_tile_y, br_tile_y + 1):
        thread = threading.Thread(target=build_row, args=[tile_y])
        thread.start()
        threads.append(thread)
    
    for thread in threads:
        thread.join()
    print(img.size)
    return img

def loadAndReturnImage(Place,lat,lon):
    file_dir = os.path.dirname(__file__)
    prefs_path = os.path.join(file_dir, 'preferences.json')
    default_prefs = {
            'url': 'https://mt.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
            'tile_size': 1024,
            'channels': 3,
            'dir': os.path.join(file_dir, 'images'),
            'headers': {
                'cache-control': 'max-age=0',
                'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'none',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36'
            },
            'tl': '',
            'br': '',
            'zoom': ''
        }
    store = DataStore()
    place = Place
    latitude = float(lat)
    longitude = float(lon)
    target_point = (latitude, longitude)
    nearest_segment_id, min_distance = store.get_nearest_line_segment_id(place, target_point)
    if nearest_segment_id:
        print("Nearest line segment ID found:", nearest_segment_id)
        print("Minimum distance:", min_distance, "meters")
    else:
        print("No line segment found")
    with open(os.path.join(file_dir, 'preferences.json'), 'r', encoding='utf-8') as f:
        prefs = json.loads(f.read())

    topLeft = store.data[nearest_segment_id]['top_left']
    bottomRight = store.data[nearest_segment_id]['bottom_right']
    pointA = store.data[nearest_segment_id]['point_a']
    pointB = store.data[nearest_segment_id]['point_b']

    zoom = 20
    channels = int(prefs['channels'])
    tile_size = int(prefs['tile_size'])
    lat1 = topLeft[0]
    lon1 = topLeft[1]
    lat2 = bottomRight[0]
    lon2 = bottomRight[1]

    img = download_image(lat1, lon1, lat2, lon2, zoom, prefs['url'],prefs['headers'], tile_size, channels)
    print('image shape :',img.shape)
    img = Image.fromarray(img)
    img.save('./imagesD/downlod.png')
    return img