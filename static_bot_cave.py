import time
from adb_connector import *

# Change starting vars
StartLevel = 0
SkipDungeonChoose = StartLevel > 0

playtime = 60

# screen resolution. Needed for future normalization
width = 1080
heigth = 2220


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


buttons, x, y, movements = {}, 0, 0, {}


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


def letPlay(time=playtime):
    print("Letting player play")
    for i in range(time, 0, -1):
        # Check if screen is blocked then unlock it
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
    global buttons, x, y, movements
    buttons, x, y, movements = getCoordinates()
    device = os.popen("adb devices").read().split('\n', 1)[1].split("device")[0].strip()
    if device is None:
        print("Error: no device discovered. Start adb server before executing this.")
        exit(1)
    print("Usb debugging device: %s" % device)
    if not SkipDungeonChoose:
        chooseCave()
    play_cave(StartLevel)


if __name__ == "__main__":
    main()
