import os
import json
from PIL import Image
# from pure_adb_connector import *
import numpy as np
from game_screen_connector import GameScreenConnector


def getImageFrame(path: str):
    with Image.open(path, 'r') as im:
        pixval = np.array(im.getdata())
    return pixval


# width, heigth = adb_get_size()
width, heigth = 1080, 2220

screen_conector = GameScreenConnector(width, heigth)
screen_conector.debug = True
static_coords = screen_conector.static_coords

screens_path = "screens/samsung_s8+"
files = os.listdir(screens_path)

for file in files:
    full_path = os.path.join(screens_path, file)
    frame = getImageFrame(full_path)
    complete_frame = screen_conector.getFrameStateComplete(frame)
    computed = {}
    sum = 0
    last_true = ""
    for k, v in complete_frame.items():
        computed[k] = 1 if v else 0
        if computed[k]:
            last_true = k
        sum += computed[k]
    if sum == 0:
        print("NO_DETECTION - %s" % file)
    elif sum == 1:
        print("OK - %s: %s" % (file, last_true))
    else:
        ones_name = [k for k, v in computed.items() if v == 1]
        print("MULTIPLE_DETECTIONS - %s: %s" % (file, ", ".join(ones_name)))
