import os
import numpy as np
from PIL import Image
from pure_adb_connector import adb_screen_getpixels

screenshot_path = 'screens/samsung_s10e/Screenshot_20200315-002432_Archero.png'
x,y = 0.194444, 0.675676


width = 1080
height = 2220
x, y = x * width, y * height
# print("Taking a screenshot...")
# frame = adb_screen_getpixels()

pixval = []
with Image.open(screenshot_path, 'r') as im:
    frame = np.array(im.getdata())
pos = int(y * width + x)
pixel = frame[pos]
print("pixel:")
print(pixel)
