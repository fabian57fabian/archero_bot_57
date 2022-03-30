import os
import numpy as np
from PIL import Image
import json


def create_abilities_dict(in_path:str, out_fn:str):
    abilities_dict = {}
    for fn in os.listdir(in_path):
        filename = os.path.join(in_path, fn)
        abilities_dict[fn[-4]] = 0
    with open(out_fn, 'w') as f:
        json.dump(abilities_dict, f, indent=2)

if __name__ == '__main__':
    create_abilities_dict(in_path='../datas/abilities/abilities_templates', out_fn='..\\datas\\abilities\\abilities_dists.json')