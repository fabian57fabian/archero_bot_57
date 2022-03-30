import os
from PIL import Image
import numpy as np


def test_diff(fn1, folder, plot=False):
    im1 = Image.open(fn1)
    np1 = np.array(im1.getdata())

    files, dists = [], []

    print("Distances from {}".format(fn1))
    for fn in os.listdir(folder):
        if fn == "ability_0.png":continue
        path = os.path.join(folder, fn)
        im2 = Image.open(path)
        np2 = np.array(im2.getdata())

        dist = np.mean(np.abs(np1 - np2))
        print("{:20}: {}".format(fn, dist))

        files.append(fn)
        dists.append(dist)

    if plot:
        import matplotlib.pyplot as plt
        plt.figure()
        plt.bar(files, dists)
        plt.title("Distances from "+fn1)
        plt.show()

        #plt.figure()
        #plt.hist(dists, 30)
        #plt.title("Distances from " + fn1)
        #plt.show()


if __name__ == '__main__':
    fld = "..\\datas\\1080x1920\\abilities"
    fn = "..\\datas\\1080x1920\\abilities\\ability_30.png"

    test_diff(fn, fld, plot=True)
