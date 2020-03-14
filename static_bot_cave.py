import time
from adb_connector import *
from game_screen_connector import GameScreenConnector

playtime = 70

# Set this to true if you want to use generated data with TouchManager. Uses below coordinates path
UseGeneratedData = False
# Set this to true if keep receiving "No energy, wqiting for one minute"
UseManualStart = True
data_pack = 'datas'
buttons_corrdinates_filename = "data.py"
buttons_corrdinates_default_filename = "default_dict.py"
# screen resolution. Needed for future normalization
width = 1080
heigth = 2220

screen_connector = GameScreenConnector(width, heigth)


# Those are normalized coordinates of data to be taken and trained into a simple nn to predict game status (multiclass)
def getAttributesArr():
    calculus_width = 1080
    calculus_heigth = 2220
    attr = [
        [1024 / calculus_width, 530 / calculus_heigth],  # level up/initial ability choose (right up)
        [50 / calculus_width, 530 / calculus_heigth],  # level up/initial ability choose (left up)
        [1010 / calculus_width, 370 / calculus_heigth],  # blessing and devil (up right)
        [50 / calculus_width, 370 / calculus_heigth],  # blessing and devil (up left)
        [70 / calculus_width, 870 / calculus_heigth],  # Ending game green and ending final red (up left)
        [1110 / calculus_width, 870 / calculus_heigth],  # Ending game green and ending final red (up right)
        [713 / calculus_width, 1665 / calculus_heigth],
        # special prize color (ad when blessing and devil is yellow) (center right)
        [400 / calculus_width, 1665 / calculus_heigth],
        # special prize color (ad when blessing and devil is yellow) (center left)
        [193 / calculus_width, 1740 / calculus_heigth],  # Devil Reject
        [896 / calculus_width, 1740 / calculus_heigth],  # Devil Accept
        [113 / calculus_width, 1336 / calculus_heigth],  # Left ability background
        [446 / calculus_width, 1336 / calculus_heigth],  # Center ability background
        [784 / calculus_width, 1336 / calculus_heigth],  # Right ability background
        [184 / calculus_width, 1690 / calculus_heigth],  # Left angel blessing background
        [690 / calculus_width, 1690 / calculus_heigth],  # Right angel blessing background
        [500 / calculus_width, 1900 / calculus_heigth],  # Left playing joystick blue
        [570 / calculus_width, 1690 / calculus_heigth],  # Right playing joystick blue
        [1060 / calculus_width, 60 / calculus_heigth],  # up right money grey count playing
    ]
    return attr


def getAttributes(frame):
    pass


attributes = []


def getCoordinates():
    # Do not change this parameters, they are made for normalization
    calculus_width = 1080
    calculus_heigth = 2220

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
    return x, y, movements


buttons, x, y, movements = {}, 0, 0, {}


def swipe_points(start, stop, s):
    start = buttons[start]
    stop = buttons[stop]
    print("Swiping between points")
    adb_swipe([start[0] * width, start[1] * heigth, stop[2] * width, stop[3] * heigth], s)


def swipe(name, s):
    coord = movements[name]
    # convert back from normalized values
    adb_swipe([coord[0] * width, coord[1] * heigth, coord[2] * width, coord[3] * heigth], s)


def tap(name):
    x, y = buttons[name]
    # convert back from normalized values
    adb_tap((x * width, y * heigth))


def wait(s):
    time.sleep(s)


def goTroughDungeon():
    print("Going through dungeon")
    swipe('n', 1.5)
    swipe('w', .32)
    swipe('n', .5)
    swipe('e', .32)
    swipe('e', .32)
    swipe('n', .5)
    swipe('w', .32)
    swipe('n', 1.5)


def letPlay(_time=playtime):
    print("Letting player play")
    for i in range(_time, 0, -1):
        if i % 10 == 0:
            if screen_connector.checkEndFrame():
                print("Game ended")
                wait(5)
                print("Going back to menu...")
                tap('close_end')
                raise Exception('ended')
            elif screen_connector.checkLevelEnded():
                print("Just leveled up!")
                wait(1)
                return
        print(i)
        wait(1)


def normal_lvl():
    goTroughDungeon()
    letPlay()
    tap('ability_left')
    wait(1)
    tap('spin_wheel_back')  # guard not to click on watch
    wait(3)
    tap('ability_left')
    wait(1)
    tap('spin_wheel_back')  # guard not to click on watch or buy stuff (armor or others)
    wait(2)
    swipe('n', 2)


def heal_lvl():
    swipe('n', 1.5)
    tap('ability_daemon_reject')
    tap('ability_left')
    wait(1)
    tap('spin_wheel_back')
    wait(.5)
    swipe('n', .6)
    wait(1)
    tap('spin_wheel_back')
    wait(1)
    swipe('n', 1)


def boss_lvl():
    swipe('n', 2)
    swipe('n', 1.5)
    swipe('n', 1.5)
    letPlay()
    tap('lucky_wheel_start')
    wait(6)
    tap('spin_wheel_back')
    wait(1)
    tap('ability_daemon_reject')
    tap('ability_left')
    wait(1)
    tap('spin_wheel_back')  # guard not to click on watch
    wait(1)
    swipe('n', 1)


def intro_lvl():
    wait(3)
    tap('ability_daemon_reject')
    tap('ability_left')
    swipe('n', 3)
    wait(5)
    tap('lucky_wheel_start')
    wait(5)
    swipe('n', 2)


t_intro = 'intro'
t_normal = 'normal'
t_heal = 'heal'
t_boss = 'boss'

levels_type = {
    0: t_intro,
    1: t_normal,
    2: t_heal,
    3: t_normal,
    4: t_heal,
    5: t_boss,
    6: t_normal,
    7: t_heal,
    8: t_normal,
    9: t_heal,
    10: t_boss,
    11: t_normal,
    12: t_heal,
    13: t_normal,
    14: t_heal,
    15: t_boss,
    16: t_normal,
    17: t_heal,
    18: t_normal,
    19: t_heal,
    20: t_boss,
}


def play_cave(startlvl=0):
    if startlvl < 0 or startlvl > 20:
        print("level out of range: %d" % startlvl)
        exit(1)
    global playtime
    for lvl in range(startlvl, 21):
        print("Level %d: %s" % (lvl, str(levels_type[lvl])))
        if levels_type[lvl] == t_intro:
            intro_lvl()
        elif levels_type[lvl] == t_normal:
            normal_lvl()
        elif levels_type[lvl] == t_heal:
            heal_lvl()
        elif lvl == 20:
            boss_final()
        elif levels_type[lvl] == t_boss:
            boss_lvl()


def boss_final():
    wait(50)
    tap('start')
    wait(2)
    swipe('n', 5)
    wait(.5)
    tap('start')  # this is to wxit


def chooseCave():
    print("Main menu")
    tap('start')
    wait(3)


def main():
    global buttons, x, y, movements, attributes, width, heigth
    x, y, movements = getCoordinates()
    buttons = getGeneratedData()
    # Not used general attributes
    # attributes = getAttributesArr()
    # for a in attributes:
    #    a[0] *= width
    #    a[1] *= heigth
    # Here attributes are not normalized but direct pixel values depending on width, height
    device = get_device_id()
    if device is None:
        print("Error: no device discovered. Start adb server before executing this.")
        exit(1)
    print("Usb debugging device: %s" % device)
    while True:
        if UseManualStart:
            a = input("Press enter to start a game (your energy bar must be at least 5)")
        else:
            while not screen_connector.have_energy():
                print("No energy, waiting for one minute")
                wait(60)
        chooseCave()
        try:
            play_cave()
        except Exception as exc:
            if exc.args[0] == 'ended':
                print("Game ended. Farmed a little bit...")
            else:
                print("Got an unknown exception: %s" % exc)
                exit(1)


def import_method(folder, file, name):
    """
    loads a method from file (.py) inside a folder
    :param folder:
    :param file:
    :param name:
    :return:
    """
    module = folder + "." + file[:-3]
    module = __import__(module, fromlist=[name])
    return getattr(module, name)


def getGeneratedData():
    global buttons_corrdinates_filename, buttons_corrdinates_default_filename, UseGeneratedData
    if os.path.exists(os.path.join(data_pack, buttons_corrdinates_filename)):
        method = import_method(data_pack, buttons_corrdinates_filename, "getButtons")
        return method()
    elif os.path.exists(os.path.join(data_pack, buttons_corrdinates_default_filename)):
        method = import_method(data_pack, buttons_corrdinates_default_filename, "getButtons")
        return method()
    else:
        print("No %s or d%s scripts are available. check your files." % (
            buttons_corrdinates_filename, buttons_corrdinates_default_filename))
        exit(1)


if __name__ == "__main__":
    main()
