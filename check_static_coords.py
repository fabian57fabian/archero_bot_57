import os
import sys
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
# width, heigth = 1080, 1920
width, heigth = 1080, 2220

screen_conector = GameScreenConnector(width, heigth)
screen_conector.debug = len(sys.argv) > 1
static_coords = screen_conector.static_coords

# screens_path = "../archero_my_screens/Craciun"
screens_path = "screens/samsung_s8+"
files = os.listdir(screens_path)
files.sort()
for file in files:
    full_path = os.path.join(screens_path, file)
    frame = getImageFrame(full_path)
    complete_frame = screen_conector.getFrameStateComplete(frame)
    computed = [k for k, v in complete_frame.items() if v]
    sum = len(computed)
    if sum == 0:
        print("NO_DETECTION - %s" % file)
    elif sum == 1:
        print("OK - %s: %s" % (file, computed[0]))
    else:
        ones_name_purged_singular = [k for k in computed if len(screen_conector.static_coords[k]["coordinates"]) > 1]
        removed = [k for k in computed if k not in ones_name_purged_singular]
        if len(ones_name_purged_singular) == 0:
            print("MUL_DETECTIONS %s: %s" % (file, ", ".join(computed)))
        elif len(ones_name_purged_singular) == 1:
            print("OK - %s: %s. Extra detected singulars: %s" % (file, ones_name_purged_singular[0], ", ".join(removed)))
        else:
            print("MUL_DETECTIONS %s: %s" % (file, ", ".join(ones_name_purged_singular)))
