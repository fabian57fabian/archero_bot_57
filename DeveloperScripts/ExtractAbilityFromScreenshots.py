import os
import numpy as np
from PIL import Image


def crop_abilities(path_screens:str, path_out:str):
    if not os.path.exists(path_out): os.makedirs(path_out)
    #if both exists
    w, h = 1080, 1920

    sw, sh = 239, 239
    y1 = 1157
    x1, x2, x3 = 90, 420, 750

    c1 = (x1, y1, x1+sw, y1+sh)
    c2 = (x2, y1, x2+sw, y1+sh)
    c3 = (x3, y1, x3+sw, y1+sh)

    c = 66
    for fn in os.listdir(path_screens):
        path = os.path.join(path_screens, fn)
        with Image.open(path) as im:
            #img_np = np.array(img.getdata())
            cr1 = im.crop(c1)
            cr1.save(os.path.join(path_out, "ability_{}.png".format(c)), 'PNG')
            c+=1
            cr2 = im.crop(c2)
            cr2.save(os.path.join(path_out, "ability_{}.png".format(c)), 'PNG')
            c += 1
            cr3 = im.crop(c3)
            cr3.save(os.path.join(path_out, "ability_{}.png".format(c)), 'PNG')
            c += 1


if __name__ == '__main__':
    crop_abilities(path_screens='..\\datas\\1080x1920\\abilities_sc', path_out='..\\datas\\1080x1920\\abilities_new')