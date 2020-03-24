from ppadb.client import Client as AdbClient
import os
from PIL import Image
import numpy as np
import io

"""
This is the library
https://pypi.org/project/pure-python-adb/
"""

print("Initializing ppadb library")
os.system("adb devices")  # this is done to make it connect (like __init__ )
# Default is "127.0.0.1" and 5037
_client = AdbClient(host="127.0.0.1", port=5037)
devs = _client.devices()
if len(devs) < 1:
    print("No devices running.")
    exit(1)
my_device = _client.device(devs[0].get_serial_no())


def get_device_id():
    return my_device.get_serial_no()


def adb_get_size():
    bytes_screen = my_device.screencap()
    im = Image.open(io.BytesIO(bytes_screen))
    w, h = im.size
    im.close()
    return w, h


def adb_screen(name:str = "screen.png"):
    """
    Executes a screen and saved it in current folder as 'screen.png'
    :return:
    """
    os.system("adb exec-out screencap -p > "+name)


def adb_screen_getpixels():
    bytes_screen = my_device.screencap()
    pixval = None
    with Image.open(io.BytesIO(bytes_screen)) as im:
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
    my_device.input_swipe(int(x1), int(y1), int(x2), int(y2), s)


def adb_tap(coord):
    """
    Executes sdb tap function

    Parameters:
    coord (tuple(x, y)): coordinate of tap
    """
    x, y = coord[0], coord[1]
    print("Tapping on (%d, %d)" % (int(x), int(y)))
    my_device.input_tap(int(x), int(y))


keycodes = {
    "KEYCODE_UNKNOWN": 0,
    "KEYCODE_MENU": 1,
    "KEYCODE_SOFT_RIGHT": 2,
    "KEYCODE_HOME": 3,
    "KEYCODE_BACK": 4,
    "KEYCODE_CALL": 5,
    "KEYCODE_ENDCALL": 6,
    "KEYCODE_0": 7,
    "KEYCODE_1": 8,
    "KEYCODE_2": 9,
    "KEYCODE_3": 10,
    "KEYCODE_4": 11,
    "KEYCODE_5": 12,
    "KEYCODE_6": 13,
    "KEYCODE_7": 14,
    "KEYCODE_8": 15,
    "KEYCODE_9": 16,
    "KEYCODE_STAR": 17,
    "KEYCODE_POUND": 18,
    "KEYCODE_DPAD_UP": 19,
    "KEYCODE_DPAD_DOWN": 20,
    "KEYCODE_DPAD_LEFT": 21,
    "KEYCODE_DPAD_RIGHT": 22,
    "KEYCODE_DPAD_CENTER": 23,
    "KEYCODE_VOLUME_UP": 24,
    "KEYCODE_VOLUME_DOWN": 25,
    "KEYCODE_POWER": 26,
    "KEYCODE_CAMERA": 27,
    "KEYCODE_CLEAR": 28,
    "KEYCODE_A": 29,
    "KEYCODE_B": 30,
    "KEYCODE_C": 31,
    "KEYCODE_D": 32,
    "KEYCODE_E": 33,
    "KEYCODE_F": 34,
    "KEYCODE_G": 35,
    "KEYCODE_H": 36,
    "KEYCODE_I": 37,
    "KEYCODE_J": 38,
    "KEYCODE_K": 39,
    "KEYCODE_L": 40,
    "KEYCODE_M": 41,
    "KEYCODE_N": 42,
    "KEYCODE_O": 43,
    "KEYCODE_P": 44,
    "KEYCODE_Q": 45,
    "KEYCODE_R": 46,
    "KEYCODE_S": 47,
    "KEYCODE_T": 48,
    "KEYCODE_U": 49,
    "KEYCODE_V": 50,
    "KEYCODE_W": 51,
    "KEYCODE_X": 52,
    "KEYCODE_Y": 53,
    "KEYCODE_Z": 54,
    "KEYCODE_COMMA": 55,
    "KEYCODE_PERIOD": 56,
    "KEYCODE_ALT_LEFT": 57,
    "KEYCODE_ALT_RIGHT": 58,
    "KEYCODE_SHIFT_LEFT": 59,
    "KEYCODE_SHIFT_RIGHT": 60,
    "KEYCODE_TAB": 61,
    "KEYCODE_SPACE": 62,
    "KEYCODE_SYM": 63,
    "KEYCODE_EXPLORER": 64,
    "KEYCODE_ENVELOPE": 65,
    "KEYCODE_ENTER": 66,
    "KEYCODE_DEL": 67,
    "KEYCODE_GRAVE": 68,
    "KEYCODE_MINUS": 69,
    "KEYCODE_EQUALS": 70,
    "KEYCODE_LEFT_BRACKET": 71,
    "KEYCODE_RIGHT_BRACKET": 72,
    "KEYCODE_BACKSLASH": 73,
    "KEYCODE_SEMICOLON": 74,
    "KEYCODE_APOSTROPHE": 75,
    "KEYCODE_SLASH": 76,
    "KEYCODE_AT": 77,
    "KEYCODE_NUM": 78,
    "KEYCODE_HEADSETHOOK": 79,
    "KEYCODE_FOCUS": 80,
    "KEYCODE_PLUS": 81,
    "KEYCODE_MENU_2": 82,
    "KEYCODE_NOTIFICATION": 83,
    "KEYCODE_SEARCH": 84,
    "TAG_LAST_KEYCODE": 85, }


def adb_tap_key(keycode: str):
    # global keycodes
    if keycode in keycodes:
        my_device.input_keyevent(keycodes[keycode])
