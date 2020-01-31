import time
from adb_connector import *

SkipDungeonChoose = False

playtime = 60

# screen resolution. Needed for future normalization
width = 1080
heigth = 2220

buttons = {
    'pause': [20 / width, 20 / heigth],
    'start': [540 / width, 1700 / heigth],
    'collect': [330 / width, 1490 / heigth],
    'ability_left': [210 / width, 1500 / heigth],
    'ability_center': [540 / width, 1500 / heigth],
    'ability_right': [870 / width, 1500 / heigth],
    'spin_wheel_back': [85 / width, 2140 / heigth],
    'lucky_wheel_start': [540 / width, 1675 / heigth],
    'ability_daemon_reject': [175 / width, 1790 / heigth]
}

# pointer base coordinates
x = 530 / width
y = 1800 / heigth

offsetx = 400 / width
offsety = 400 / heigth

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
    swipe('w', .40)
    swipe('n', .5)
    swipe('e', .40)
    swipe('e', .40)
    swipe('n', .5)
    swipe('w', .40)
    swipe('n', 1)


def letPlay(time=playtime):
    print("Letting player play")
    for i in range(time, 0, -1):
        print(i)
        wait(1)


def normal_lvl():
    goTroughDungeon()
    letPlay()
    tap('ability_left')
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
    tap('spin_wheel_back')
    wait(.5)
    swipe('n', .6)
    tap('spin_wheel_back')
    wait(1)
    swipe('n', 1)


def boss_lvl():
    swipe('n', 2)
    swipe('n', 2)
    swipe('n', 2)
    letPlay()
    tap('lucky_wheel_start')
    wait(6)
    tap('spin_wheel_back')
    wait(1)
    tap('ability_daemon_reject')
    tap('ability_left')
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
    17: t_heal,
    18: t_normal,
    19: t_heal,
    20: t_boss,
}


def play_cave():
    global playtime
    for lvl in range(1, 21):
        print("Level %d: boss" % levels_type[lvl])
        if levels_type[lvl] == t_intro:
            intro_lvl()
        elif levels_type[lvl] == t_normal:
            normal_lvl()
        elif levels_type[lvl] == t_heal:
            heal_lvl()
        elif levels_type[lvl] == t_boss:
            boss_lvl()


def chooseCave():
    print("Main menu")
    tap('start')
    wait(3)


def main():
    device = os.popen("adb devices").read().split('\n', 1)[1].split("device")[0].strip()
    if device is None:
        print("Error: no device discovered. Start adb server before executing this.")
        exit(1)
    print("Usb debugging device: %s" % device)
    if not SkipDungeonChoose:
        chooseCave()
    play_cave(11)


if __name__ == "__main__":
    main()
