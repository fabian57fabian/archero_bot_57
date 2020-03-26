import time
from pure_adb_connector import *
# from adb_connector import *
from game_screen_connector import GameScreenConnector
import sys

playtime = 70

# Set this to true if you want to use generated data with TouchManager. Uses below coordinates path
UseGeneratedData = False
# Set this to true if keep receiving "No energy, wqiting for one minute"
UseManualStart = False
# Set this to true if want to automatically check for energy
SkipEnergyCheck = False
data_pack = 'datas'
buttons_corrdinates_filename = "data.py"
buttons_corrdinates_default_filename = "default_dict.py"

device = get_device_id()
if device is None:
    print("Error: no device discovered. Start adb server before executing this.")
    exit(1)
print("Usb debugging device: %s" % device)
width, heigth = adb_get_size()
print("Your resolution is %dx%d" % (width, heigth))
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


def exit_dungeon_uncentered():
    wait(2)
    upper_line = screen_connector.getLineUpper()
    print("Going trough door to exit...")
    swipe('n', 2)
    wait(2)
    if not screen_connector.checkUpperLineHasChanged(upper_line):
        print("Not exiting, trying right...")
        swipe('ne', 3)
        wait(2)
        if not screen_connector.checkUpperLineHasChanged(upper_line):
            print("Not exiting, trying left...")
            swipe('nw', 4)
            wait(2)
            if not screen_connector.checkUpperLineHasChanged(upper_line):
                raise Exception('unable_exit_dungeon')


def goTroughDungeon_old():
    print("Going through dungeon")
    swipe('n', 1.5)
    swipe('w', .32)
    swipe('n', .5)
    swipe('e', .32)
    swipe('e', .32)
    swipe('n', .5)
    swipe('w', .325)
    swipe('n', 1.5)


def goTroughDungeon():
    print("Going through dungeon")
    swipe('n', 1.5)
    swipe('w', .32)
    swipe('n', .5)
    swipe('e', .32)
    swipe('e', .32)
    swipe('n', .7)
    swipe('w', .325)
    swipe('w', .3)
    swipe('n', 1.6)
    swipe('e', .28)
    swipe('n', 2)


def letPlay(_time=playtime, is_boss=False):
    check_exp_bar = not is_boss
    print("Auto attacking")
    experience_bar_line = screen_connector.getLineExpBar()
    for i in range(_time, 0, -1):
        if i % 10 == 0:
            print("Checking screen...")
            frame = screen_connector.getFrame()
            if screen_connector.checkEndFrame(frame):
                print("Game ended")
                wait(5)
                print("Going back to menu...")
                tap('close_end')
                wait(4)  # Wait to go to the menu
                raise Exception('ended')
            elif screen_connector.checkLevelEnded(frame):
                print("Just leveled up!")
                wait(1)
                return
            elif check_exp_bar and screen_connector.checkExpBarHasChanged(experience_bar_line, frame):
                print("Experience gained!")
                wait(3)
                return
        print(i)
        wait(1)


def normal_lvl():
    goTroughDungeon()
    letPlay()
    tap('spin_wheel_back')  # guard not to click on mistery vendor
    wait(1)
    tap('ability_left')
    wait(1)
    tap('spin_wheel_back')  # guard not to click on watch
    wait(3)
    tap('ability_left')
    wait(2)
    tap('spin_wheel_back')  # guard not to click on watch or buy stuff (armor or others)
    wait(1)
    exit_dungeon_uncentered()


def heal_lvl():
    swipe('n', 1.7)
    wait(1)
    tap('ability_daemon_reject')
    tap('ability_left')
    wait(1.5)
    tap('spin_wheel_back')
    wait(1)
    swipe('n', .8)
    wait(1.5)
    tap('spin_wheel_back')
    wait(1.5)
    exit_dungeon_uncentered()


def boss_lvl():
    swipe('n', 2)
    swipe('n', 1.5)
    swipe('n', 1)
    letPlay(is_boss=True)
    tap('lucky_wheel_start')
    wait(6)
    tap('spin_wheel_back')
    wait(1.5)
    tap('ability_daemon_reject')
    tap('ability_left')
    wait(1.5)
    tap('spin_wheel_back')  # guard not to click on watch
    wait(1.5)
    tap('ability_left')  # Extra guard for level up
    wait(1.5)
    exit_dungeon_uncentered()


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
    wait(2)
    swipe('w', 3)
    wait(50)
    tap('start')
    wait(2)
    swipe('n', 5)
    wait(.5)
    swipe('ne', 3)
    wait(5)
    tap('close_end')  # this is to wxit


def chooseCave():
    print("Main menu")
    tap('start')
    wait(3)


def get_start_lvl_from_args():
    start_lvl = 0
    if len(sys.argv) > 1:
        try:
            arg = sys.argv[1]
            start_lvl = int(arg)
            if start_lvl < 0 or start_lvl > 20:
                print("Given starting level is not a valid start level in [0,20]. Starting from zero")
                start_lvl = 0
        except:
            print("Given starting level is not a valid start level. Starting from zero")
            start_lvl = 0
    return start_lvl


def quick_test_functions():
    pass


def main():
    global buttons, x, y, movements, attributes, width, heigth
    start_lvl = get_start_lvl_from_args()
    x, y, movements = getCoordinates()
    buttons = getGeneratedData()
    # Not used general attributes
    # attributes = getAttributesArr()
    # for a in attributes:
    #    a[0] *= width
    #    a[1] *= heigth
    # Here attributes are not normalized but direct pixel values depending on width, height
    quick_test_functions()
    while True:
        if start_lvl == 0:
            if UseManualStart:
                a = input("Press enter to start a game (your energy bar must be at least 5)")
            else:
                while (not SkipEnergyCheck) and not screen_connector.have_energy():
                    print("No energy, waiting for one minute")
                    wait(60)
            chooseCave()
        try:
            play_cave(start_lvl)
        except Exception as exc:
            if exc.args[0] == 'ended':
                print("Game ended. Farmed a little bit...")
            elif exc.args[0] == 'unable_exit_dungeon':
                print("Unable to exit a room in a dungeon. Waiting instead of causing troubles")
                exit(1)
            else:
                print("Got an unknown exception: %s" % exc)
                exit(1)
        start_lvl = 0


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
