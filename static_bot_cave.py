import time
from adb_connector import *

SkipDungeonChoose = False

playtime = 80

#screen resolution. Needed for future normalization
width = 1080
heigth = 2220

buttons = {
    'pause': [20, 20],
    'start': [540, 1700],
    'collect': [330, 1490],
    'ability_left': [210, 1500],
    'ability_center': [540, 1500],
    'ability_right': [870, 1500],
    'spin_wheel_back': [85, 2140],
    'lucky_wheel_start': [540, 1675],
}

# pointer base coordinates
x = 530
y = 1800

offsetx = 400
offsety = 400

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
    adb_swipe(movements[name], s)


def tap(name):
    adb_tap(buttons[name])


def wait(s):
    time.sleep(s)


def goTroughDungeon():
    print("Going through dungeon")
    swipe('n', 1.5)
    swipe('w', .5)
    swipe('n', .5)
    swipe('e', .5)
    swipe('e', .5)
    swipe('n', .5)
    swipe('w', .55)
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
    tap('ability_left')
    tap('spin_wheel_back')
    wait(.5)
    swipe('n', .6)
    tap('spin_wheel_back')
    wait(.5)
    swipe('n', 1)


def boss_lvl():
    goTroughDungeon()
    letPlay()
    tap('lucky_wheel_start')
    wait(6)
    tap('spin_wheel_back')
    wait(1)
    tap('ability_left')
    tap('spin_wheel_back')  # guard not to click on watch
    wait(1)
    swipe('n', 1)


def intro_lvl():
    wait(2)
    tap('ability_left')
    swipe('n', 3)
    wait(5)
    tap('lucky_wheel_start')
    wait(5)
    swipe('n', 2)


def play_cave(start_lvl=0):
    global playtime
    for lvl in range(start_lvl, 21):
        if lvl == 0:
            print("Level 0: intro")
            intro_lvl()
            playtime = 30 # set low playtime at first dungeon
        elif lvl in [5, 10, 15, 20]:
            print("Level %d: boss" % lvl)
            boss_lvl()
        elif lvl % 2 == 0:
            print("Level %d: heal" % lvl)
            heal_lvl()
        else:
            print("Level %d:" % lvl)
            normal_lvl()
            playtime = 80 # set higher playtime after second


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
    play_cave(10)


if __name__ == "__main__":
    main()
