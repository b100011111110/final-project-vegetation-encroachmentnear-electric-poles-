import os
import json
import loadDLModel
from PictureDraw import *
from PIL import Image, ImageDraw
from shapely.geometry import LineString, Polygon
from downloadImage import download_tile,project_with_scale,download_image
from DataStoreSet import DataStore

model = loadDLModel.LoadDllModel()

file_dir = os.path.dirname(__file__+'download')
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

def run(place,latitude,longitude):

    store = DataStore()
    store.import_from_csv('./data/data.csv')
    print(store.data)

    target_point = (latitude, longitude)

    nearest_segment_id, min_distance = store.get_nearest_line_segment_id(place, target_point)

    if nearest_segment_id:
        print("Nearest line segment ID found:", nearest_segment_id)
        print("Minimum distance:", min_distance, "meters")
    else:
        print("No line segment found")
        exit()

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
    shape = img.shape
    print(shape)
    img = Image.fromarray(img)
    img.save('./static/downlod.png')

    start = lat_lon_to_pixel(pointA[0],pointA[1],shape[1],shape[0],lat1=topLeft[0],lon1=topLeft[1],lat2=bottomRight[0],lon2=bottomRight[1])
    end = lat_lon_to_pixel(pointB[0],pointB[1],shape[1],shape[0],lat1=topLeft[0],lon1=topLeft[1],lat2=bottomRight[0],lon2=bottomRight[1])
    PIXEL_VALUE = lat_lon_to_pixel(latitude,longitude,shape[1],shape[0],lat1=topLeft[0],lon1=topLeft[1],lat2=bottomRight[0],lon2=bottomRight[1])
    imge = extract_features_and_color_NLines('./static/downlod.png',model=model,lines=[[start,end]])
    imge.save('./static/finalOutput.png')
    fimg = draw_square(imge,PIXEL_VALUE)
    fimg.save('./static/finalOutput.png')
    return fimg