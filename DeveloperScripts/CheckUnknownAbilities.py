import os
from PIL import Image
import numpy as np
import sys
sys.path.insert(0, "../")
from Utils import get_matrix_diff


def test_diffs(templates, images_unknown, plot=False, thresh=1.0, debug=True):
    print("Testing all distances")

    for np1, fn in images_unknown:
        files, dists = [], []
        files_found = []
        for np_template, fn_template in templates:
            dist = get_matrix_diff(np1, np_template)
            if debug: print("{:20}: {}".format(fn, dist))
            files.append(fn)
            dists.append(dist)
            if dist < thresh:
                files_found.append(fn_template)
        print("File {}: Max={}, Min={}, Abilities={}".format(fn, max(dists), min(dists), ", ".join(files_found)))

        if plot:
            import matplotlib.pyplot as plt
            plt.figure()
            plt.bar(files, dists)
            plt.title("Distances from "+fn)
            plt.show()

            plt.figure()
            plt.hist(dists, 30)
            plt.title("Distances from " + fn)
            plt.show()


def load_file_as_np(filename):
    im1 = Image.open(filename)
    np1 = np.array(im1.getdata())
    return np1


def check_all():
    fld_templates = "..\\datas\\abilities\\abilities_templates"
    fld_unknown = "..\\abilities_unknown"
    print("Loading templates")
    templates = []
    for file in os.listdir(fld_templates):
        templates.append([load_file_as_np(os.path.join(fld_templates, file)), file])
    print("Loading images")
    images_unknown = []
    for file in os.listdir(fld_unknown):
        images_unknown.append([load_file_as_np(os.path.join(fld_unknown, file)), file])
    test_diffs(templates, images_unknown, plot=False, thresh=4, debug=False)


def check_one():
    fld_templates = "..\\datas\\abilities\\abilities_templates"
    fn = "..\\abilities_unknown\\unknown_ability_12.png"
    templates = []
    for file in os.listdir(fld_templates):
        templates.append([load_file_as_np(os.path.join(fld_templates, file)), file])
    images_unknown = [load_file_as_np(fn), os.path.basename(fn)]

    test_diffs(templates, images_unknown, plot=True, thresh=4, debug=False)

if __name__ == '__main__':
    #check_one()
    check_all()
