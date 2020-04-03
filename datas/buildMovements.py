import json


def saveMovements(path: str):
    # Do not change this parameters, they are made for normalization
    calculus_width = 1080
    calculus_heigth = 2220

    # pointer base coordinates
    x = 530 / calculus_width
    y = 1800 / calculus_heigth

    offsetx = 400 / calculus_width
    offsety = 400 / calculus_heigth

    movements = {
        'n': [[x, y], [x, y - offsety]],
        's': [[x, y], [x, y + offsety]],
        'e': [[x, y], [x + offsetx, y]],
        'w': [[x, y], [x - offsetx, y]],
        'ne': [[x, y], [x + offsetx, y - offsety]],
        'nw': [[x, y], [x - offsetx, y - offsety]],
        'se': [[x, y], [x + offsetx, y + offsety]],
        'sw': [[x, y], [x - offsetx, y + offsety]]
    }
    with open(path, 'w') as fp:
        json.dump(movements, fp)


saveMovements('movements.json')
