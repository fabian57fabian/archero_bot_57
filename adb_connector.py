import os
from PIL import Image
import numpy as np


def adb_screen_getpixels():
    os.system("adb exec-out screencap -p > screen.png")
    pixval = None
    with Image.open("screen.png", 'r') as im:
        pixval = np.array(im.getdata())
    return pixval


def adb_swipe(locations, s):
    """
    Executes sdb swipe function

    Parameters:
    locations (array(int), size=4): [x1,y1,x2,y2] coords
    duration (int): duration (seconds)
    """
    s = int(s * 1000)
    x1, y1, x2, y2 = locations[0], locations[1], locations[2], locations[3]
    print("Swiping from (%d, %d) --> (%d, %d) in %d" % (int(x1), int(y1), int(x2), int(y2), s))
    os.system("adb shell input swipe %d %d %d %d %d" % (int(x1), int(y1), int(x2), int(y2), s))


def adb_tap(coord):
    """
    Executes sdb tap function

    Parameters:
    coord (tuple(x, y)): coordinate of tap
    """
    x, y = coord[0], coord[1]
    print("Tapping on (%d, %d)" % (int(x), int(y)))
    os.system("adb shell input tap %d %d" % (int(x), int(y)))
