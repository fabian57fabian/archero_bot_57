from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import os


# Same coordinates as for static_bot_cave
def getCoordinates():
    # Do not change this parameters, they are made for normalization
    calculus_width = 1080
    calculus_heigth = 2220

    buttons = {
        'pause': [20 / calculus_width, 20 / calculus_heigth],
        'start': [540 / calculus_width, 1700 / calculus_heigth],
        'collect': [330 / calculus_width, 1490 / calculus_heigth],
        'ability_left': [210 / calculus_width, 1500 / calculus_heigth],
        'ability_center': [540 / calculus_width, 1500 / calculus_heigth],
        'ability_right': [870 / calculus_width, 1500 / calculus_heigth],
        'spin_wheel_back': [85 / calculus_width, 2140 / calculus_heigth],
        'lucky_wheel_start': [540 / calculus_width, 1675 / calculus_heigth],
        'ability_daemon_reject': [175 / calculus_width, 1790 / calculus_heigth]
    }

    # pointer base coordinates
    x = 530 / calculus_width
    y = 1800 / calculus_heigth

    offsetx = 400 / calculus_width
    offsety = 400 / calculus_heigth

    movements = {
        'n': [x, y, x, y - offsety],
        's': [x, y, x, y + offsety],
        'e': [x, y, x + offsetx, y],
        'w': [x, y, x - offsetx, y],
        'ne': [x, y, x + offsetx, y - offsety],
        'nw': [x, y, x - offsetx, y - offsety],
        'se': [x, y, x + offsetx, y + offsety],
        'sw': [x, y, x + offsety, y + offsety]
    }
    return buttons, x, y, movements


# Having cellphones with big screens make image show too big. change this paramenter in [0,1] to resize automatically
resize_factor_show = 1
images_path = '../screens/1080x2220/'
save_images = False
# All saved images goes to screens_out folder if save_images is true

buttons, x, y, movements = getCoordinates()

for image_path in os.listdir(images_path):
    with Image.open(os.path.join(images_path, image_path)) as im:
        w, h = im.size
        print("\nImage %s with size: %dx%d" % (image_path, w, h))
        # im.show()
        wrong_coise = True
        choise = ""
        while wrong_coise:
            print("Choose from: ")
            for name in buttons.keys():
                print("%s" % name)
            choise = input("Choose what you want to draw: ")
            draw = ImageDraw.Draw(im)
            if choise in buttons:
                wrong_coise = False
            else:
                print("Entered wrong choise, select again:")
                wrong_coise = True
        _x, _y = buttons[choise]
        _x *= w
        _y *= h
        # horizontal line
        draw.line((0, _y, w, _y), fill=128, width=10)
        # vertical line
        draw.line((_x, 0, _x, h), fill=128, width=10)
        im.thumbnail((int(resize_factor_show * w), int(resize_factor_show * h)))
        plt.imshow(im)
        plt.title(choise + "->" + image_path)
        if save_images:
            plt.savefig(os.path.join("../screens/out/", "_" + image_path))
        plt.show()
        # im.show()
        # a = input("press enter to contine")
