import time
from adb_connector import *

# Change starting vars
StartLevel = 6
SkipDungeonChoose = StartLevel > 0
CheckLevelEnded = False
playtime = 60

# Set this to true if you want to use generated data with TouchManager. Uses below coordinates path
UseGeneratedData = False
buttons_corrdinates_filename = "data.py"

# screen resolution. Needed for future normalization
width = 1080
heigth = 2220


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


def getDefaultButtons():
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
        'ability_daemon_reject': [175 / calculus_width, 1790 / calculus_heigth],
        'click_neutral_away': [998 / calculus_width, 2102 / calculus_heigth],
        'lock_swap_unlock': [543 / calculus_width, 1112 / calculus_heigth],
        'lock_swap_unlock_up': [0.501235, 0.354569],
    }
    return buttons


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


def getframe():
    return adb_screen_getpixels().reshape(width, heigth, 4)


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


def continous_status_check():
    appeard = False
    while not appeard:
        arr = adb_screen_getpixels()


yellow = [255, 181, 0, 255]
blue = [0, 140, 255, 255]
px_blue = [540, 1110]
px_yellow_skill = [100, 530]


def pixel_equals(px1, px2):
    return px1[0] == px2[0] and px1[1] == px2[1] and px1[2] == px2[2] and px1[3] == blue[3]


def letPlay(time=playtime):
    print("Letting player play")
    for i in range(time, 0, -1):
        if CheckLevelEnded and i % 10 == 0:
            tap('click_neutral_away')
            wait(.5)
            pixs = adb_screen_getpixels()
            pixel_skill_appeard = pixs[px_yellow_skill[1] * width + px_yellow_skill[0]]
            print("Got yellow pixel: [%d, %d, %d, %d]" % (
                pixel_skill_appeard[0], pixel_skill_appeard[1], pixel_skill_appeard[2], pixel_skill_appeard[3]))
            if pixel_equals(pixel_skill_appeard, yellow):
                print("Found ability menu appeard")
                break
            pixel_blue = pixs[px_blue[1] * width + px_blue[0]]
            print("Got blue pixel: [%d, %d, %d, %d]" % (
                pixel_blue[0], pixel_blue[1], pixel_blue[2], pixel_blue[3]))
            if pixel_equals(pixel_blue, blue):
                swipe_points('lock_swap_unlock', 'lock_swap_unlock-up', 1)
        # TODO: Check if screen is blocked then unlock it
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
    wait(2)
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
    buttons = getGeneratedData() if UseGeneratedData else getDefaultButtons()
    attributes = getAttributesArr()
    for a in attributes:
        a[0] *= width
        a[1] *= heigth
    # Here attributes are not normalized but direct pixel values depending on width, height
    device = get_device_id()
    if device is None:
        print("Error: no device discovered. Start adb server before executing this.")
        exit(1)
    print("Usb debugging device: %s" % device)
    if not SkipDungeonChoose:
        chooseCave()
    play_cave(StartLevel)


def getGeneratedData():
    global buttons_corrdinates_filename
    if os.path.exists(buttons_corrdinates_filename):
        from data.py import getButtons
        return getButtons()


if __name__ == "__main__":
    main()
