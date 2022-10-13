import os
from PIL import Image
import numpy as np


def test_diff(fn1, folder, plot=False, thresh=1.0, debug=True):
    im1 = Image.open(fn1)
    np1 = np.array(im1.getdata())

    files, dists = [], []
    files_found = []

    for fn in os.listdir(folder):
        if fn == "ability_0.png":continue
        path = os.path.join(folder, fn)
        im2 = Image.open(path)
        np2 = np.array(im2.getdata())

        dist = np.mean(np.abs(np1 - np2))
        if debug: print("{:20}: {}".format(fn, dist))

        files.append(fn)
        dists.append(dist)
        if dist < thresh: files_found.append(fn)

    print("File {}: Max={}, Min={}, Abilities={}".format(fn1, max(dists), min(dists), ", ".join(files_found)))

    if plot:
        import matplotlib.pyplot as plt
        plt.figure()
        plt.bar(files, dists)
        plt.title("Distances from "+fn1)
        plt.show()

        plt.figure()
        plt.hist(dists, 30)
        plt.title("Distances from " + fn1)
        plt.show()


def check_all():
    fld = "..\\datas\\abilities\\abilities_templates"
    fld_unknown = "..\\abilities_unknown"
    for file in os.listdir(fld_unknown):
        fn = os.path.join(fld_unknown, file)
        test_diff(fn, fld, plot=False, thresh=4, debug=False)


def check_one():
    fld = "..\\datas\\abilities\\abilities_templates"
    fn = "..\\abilities_unknown\\unknown_ability_12.png"
    test_diff(fn, fld, plot=True, thresh=4, debug=False)


if __name__ == '__main__':
    #check_one()
    check_all()
