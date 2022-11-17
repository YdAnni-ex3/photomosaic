import pathlib
import json
import os
import math
import random

import numpy as np
import cv2

# for getting avg color of all the jpg in dataset 
def get_average_color(img):
    average_color = np.average(np.average(img, axis=0), axis=0)
    average_color = np.around(average_color, decimals=-1)       # helps user to evenly round array elements to the given number of decimals
    average_color = tuple(int(i) for i in average_color)
    return average_color

def get_closest_color(color, colors):                           # (i/p img tile, o/p img tile)
    cr, cg, cb = color

    min_difference = float("inf")
    closest_color = None
    for c in colors:
        r, g, b = eval(c)
        difference = math.sqrt((r - cr) ** 2 + (g - cg) ** 2 + (b - cb) ** 2)       # distance formula
        if difference < min_difference:                                             # updat'g min_diff 
            min_difference = difference
            closest_color = eval(c)

    return closest_color

if "cache.json" not in os.listdir():
    imgs_dir = pathlib.Path("animals")
    images = list(imgs_dir.glob("*\\*.jpg"))

    data = {}
    for img_path in images:
        img = cv2.imread(str(img_path))
        average_color = get_average_color(img)
        if str(tuple(average_color)) in data:
            data[str(tuple(average_color))].append(str(img_path))       # appending values in the existing key 
        else:
            data[str(tuple(average_color))] = [str(img_path)]           # creating new key value pair 
    with open("cache.json", "w") as file:
        json.dump(data, file, indent=2, sort_keys=True)                 # writing in cache.json
    print("Caching done")

with open("cache.json", "r") as file:
    data = json.load(file)                                              # assig'g "data" with "cache" 

img = cv2.imread("image.jpg")
img_height, img_width, _ = img.shape        # _ -> extra channel info
tile_height, tile_width = 10, 10
num_tiles_h, num_tiles_w = img_height // tile_height, img_width // tile_width       # calculating no of tiles per height and width
img = img[:tile_height * num_tiles_h, :tile_width * num_tiles_w]

tiles = []
for y in range(0, img_height, tile_height):
    for x in range(0, img_width, tile_width):
        tiles.append((y, y + tile_height, x, x + tile_width))           # 4 coord. of all pixels 

for tile in tiles:
    y0, y1, x0, x1 = tile                   # values for tile size in i/p img
    try:
        average_color = get_average_color(img[y0:y1, x0:x1])
    except Exception:
        continue
    closest_color = get_closest_color(average_color, data.keys())

    i_path = random.choice(data[str(closest_color)])                    # randomly selecting img in same key
    i = cv2.imread(i_path)
    i = cv2.resize(i, (tile_width, tile_height))                        # resizing img to tile dimension
    img[y0:y1, x0:x1] = i

    cv2.imshow("Image", img)
    cv2.waitKey(5)

cv2.imwrite("output.jpg", img)
