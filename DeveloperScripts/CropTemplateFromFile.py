import os
import numpy as np
from PIL import Image


def crop_from_file(fn:str, coords):
    with Image.open(fn) as im:
        cr1 = im.crop(coords)
        i = 1
        while os.path.exists(fn+"_{}.png".format(i)):
            i+= 1
        path_out = fn+"_{}.png".format(i)
        cr1.save(path_out, 'PNG')


if __name__ == '__main__':
    y1 = 630
    y2 = 650
    x1 = 480
    x2 = 600

    bbox = (x1, y1, x2, y2)
    crop_from_file(fn='..\\datas\\1080x1920\\screens\\play_lvl18_doors_open.png', coords=bbox)