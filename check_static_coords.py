import os
import sys
import json
from PIL import Image
# from pure_adb_connector import *
import numpy as np
from game_screen_connector import GameScreenConnector

all_screens_folder = "screens"


def getImageFrame(path: str):
    with Image.open(path, 'r') as im:
        pixval = np.array(im.getdata())
    return pixval


def loadScreenshotsFolders(all_screens_folder):
    screensFolders = {}
    for folder in os.listdir(all_screens_folder):
        try:
            if 'x' in folder:
                splat = folder.split('x')
                if len(splat) >= 2:
                    w, h = int(splat[0]), int(splat[1])
                    screensFolders[folder] = [w, h]
        except Exception as e:
            print("Got error parsing screen folder %s. skipping" % folder)
    return screensFolders


screens_data = loadScreenshotsFolders(all_screens_folder)
keys = [k for k in screens_data.keys()]

for i in range(len(keys)):
    print("%d: %s" % (i, keys[i]))
choosen = input("Select your number")
folder = keys[int(choosen)]
screens_path = os.path.join(all_screens_folder, folder)
print("Using %s" % screens_path)

width, heigth = screens_data[folder]
excluded = []

screen_conector = GameScreenConnector(width, heigth)
screen_conector.debug = len(sys.argv) > 1
static_coords = screen_conector.static_coords

files = os.listdir(screens_path)
files.sort()
all_ok = True
for file in files:
    if file not in excluded:
        full_path = os.path.join(screens_path, file)
        frame = getImageFrame(full_path)
        complete_frame = screen_conector.getFrameStateComplete(frame)
        computed = [k for k, v in complete_frame.items() if v]
        sum = len(computed)
        ok = False
        if sum == 0:
            print("NO_DETECTION - %s" % file)
        elif sum == 1:
            print("OK - %s: %s" % (file, computed[0]))
            ok = True
        else:
            ones_name_purged_singular = [k for k in computed if
                                         len(screen_conector.static_coords[k]["coordinates"]) > 1]
            removed = [k for k in computed if k not in ones_name_purged_singular]
            if len(ones_name_purged_singular) == 0:
                print("MUL_DETECTIONS %s: %s" % (file, ", ".join(computed)))
            elif len(ones_name_purged_singular) == 1:
                print("OK - %s: %s. Extra detected singulars: %s" % (
                    file, ones_name_purged_singular[0], ", ".join(removed)))
                ok = True
            else:
                print("MUL_DETECTIONS %s: %s" % (file, ", ".join(ones_name_purged_singular)))
        all_ok = all_ok and ok

if all_ok:
    print("All tests passed!")
else:
    print(
        "Got some failed tests. It is advised not to use the bot. Infinite loops and damage can be done by randomply clicking without knowledge.")
