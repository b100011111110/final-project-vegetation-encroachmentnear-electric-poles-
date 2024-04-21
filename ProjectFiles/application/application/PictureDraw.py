from PIL import Image, ImageDraw
import numpy as np
from shapely.geometry import LineString, Polygon
from featureExtraction import extract_features
import cv2 

def extract_features_and_color(image_path, output_folder_path, model):
    # Open the large image
    large_image = Image.open(image_path)

    # Get the size of the large image
    width, height = large_image.size

    # Define the size of the smaller images
    tile_size = 16
    arrr = []
    
    # Create a copy of the original image to draw on
    img_draw = large_image.copy()
    draw = ImageDraw.Draw(img_draw)

    # Loop through the large image and create smaller tiles
    for y in range(0, height, tile_size):
        for x in range(0, width, tile_size):
            # Crop a 32x32 region from the large image
            tile = large_image.crop((x, y, x + tile_size, y + tile_size))
            
            # Convert the tile to a numpy array
            tile_np = np.array(tile)
            thickness = 2
            # Extract features using the defined function
            features = extract_features(tile_np)
            
            # Predict using the model and check if p > 0.5
            prediction = model.predict(np.array([list(features.values())]))
            
            # Append the prediction result to arrr
            arrr.append(prediction)
            
            # Color the tile based on the prediction
            color = (255, 0, 0) if prediction > 0.05 else (0, 255, 0)
            for i in range(thickness):
                draw.rectangle([x - i, y - i, x + tile_size + i, y + tile_size + i], outline=color)

    img_draw.save(output_folder_path)
    return arrr

def extract_features_and_color_1line(input_image_path, model, line_points,output_folder_path=None):
    # Open the large image
    large_image = Image.open(input_image_path)
    # Get the size of the large image
    width, height = large_image.size
    # Define the size of the smaller images
    tile_size = 16
    arrr = []
    # Create a copy of the original image to draw on
    img_draw = large_image.copy()
    draw = ImageDraw.Draw(img_draw)
    # Loop through the large image and create smaller tiles
    for y in range(0, height, tile_size):
        for x in range(0, width, tile_size):
            # Crop a 16x16 region from the large image
            tile = large_image.crop((x, y, x + tile_size, y + tile_size))

            # Convert the tile to a numpy array
            tile_np = np.array(tile)
            thickness = 2


            # Create a LineString object from the input points
            line = LineString(line_points)

            # Convert the tile to a Shapely Polygon
            tile_polygon = Polygon([(x, y), (x + tile_size, y), (x + tile_size, y + tile_size), (x, y + tile_size)])

            # Check for intersection between the line and the tile
            if line.intersects(tile_polygon):
                # Append the prediction result to arrr
                features = extract_features(tile_np)

                # Predict using the model and check if p > 0.5
                prediction = model.predict(np.array([list(features.values())]))
                arrr.append(prediction)

                # Color the tile based on the prediction
                color = (255, 0, 0) if prediction > 0.5 else (0, 255, 0)
                for i in range(thickness):
                    draw.rectangle([x - i, y - i, x + tile_size + i, y + tile_size + i], outline=color)

            else:
                arrr.append(0)  # If no intersection, append 0 to arrr
    draw.line(line_points, fill=(0, 0, 255), width=4)
    if output_folder_path != None:
        img_draw.save(output_folder_path)
    
    return ImageDraw

def extract_features_and_color_NLines(input_image_path, model, lines, output_folder_path=None):
    # Open the large image
    large_image = Image.open(input_image_path)
    # Get the size of the large image
    width, height = large_image.size
    # Define the size of the smaller images
    tile_size = 16
    arrr = []
    # Create a copy of the original image to draw on
    img_draw = large_image.copy()
    draw = ImageDraw.Draw(img_draw)

    # Draw blue lines on the image for each line in the list
    for line_points in lines:
        draw.line(line_points, fill=(0, 255, 255), width=4)

    # Loop through the large image and create smaller tiles
    for y in range(0, height, tile_size):
        for x in range(0, width, tile_size):
            # Crop a 16x16 region from the large image
            tile = large_image.crop((x, y, x + tile_size, y + tile_size))

            # Convert the tile to a numpy array
            tile_np = np.array(tile)
            thickness = 2

            # Convert the tile to a Shapely Polygon
            tile_polygon = Polygon([(x, y), (x + tile_size, y), (x + tile_size, y + tile_size), (x, y + tile_size)])

            # Check for intersection between each line and the tile
            for line_points in lines:
                line = LineString(line_points)
                if line.intersects(tile_polygon):
                    # Append the prediction result to arrr
                    features = extract_features(tile_np)

                    # Predict using the model and check if p > 0.5
                    prediction = model.predict(np.array([list(features.values())]))
                    arrr.append(prediction)

                    # Color the tile based on the prediction
                    color = (255, 0, 0) if prediction > 0.5 else (0, 255, 0)
                    for i in range(thickness):
                        draw.rectangle([x - i, y - i, x + tile_size + i, y + tile_size + i], outline=color)
                    break  # Break out of the loop once an intersection is found

            else:
                arrr.append(0)  # If no intersection, append 0 to arrr
    if output_folder_path != None:
        img_draw.save(output_folder_path)
    return img_draw

def lat_lon_to_pixel(lat, lon, image_width, image_height, lat1, lon1, lat2, lon2):
    x = (lon - lon1) / (lon2 - lon1) * image_width
    y = (lat - lat1) / (lat2 - lat1) * image_height
    return int(x), int(y)

def draw_square(image, center_pixel, size=150, color=(237, 6, 245), thickness=2):

    image = np.array(image)
    # Calculate the coordinates of the top-left corner of the square
    top_left_x = center_pixel[0] - size // 2
    top_left_y = center_pixel[1] - size // 2
    
    # Calculate the coordinates of the bottom-right corner of the square
    bottom_right_x = center_pixel[0] + size // 2
    bottom_right_y = center_pixel[1] + size // 2
    
    # Draw the square boundary box
    cv2.rectangle(image, (top_left_x, top_left_y), (bottom_right_x, bottom_right_y), color, thickness)
    red_count = 0
    total_pixels = 0

    for x in range(top_left_x, bottom_right_x):
        for y in range(top_left_y, bottom_right_y):
            #print(x,y)
            if image[y, x][2] == 0 and image[y, x][0] == 255 and image[y, x][1] == 0:  # Checking if R=255, G=0, B=0
                red_count += 1
                print(red_count)
            total_pixels += 1

    if int(red_count) != 0:
        print('encroachment detected')
        image[0, 0] = [0, 0, 0]  # Cyan color (BGR format)
    else:
        print('encroachment NOT detected')
    # Calculate the percentage of red pixels
    red_percent = (red_count / total_pixels) * 100
    print(red_percent,red_count)

    return Image.fromarray(image)

