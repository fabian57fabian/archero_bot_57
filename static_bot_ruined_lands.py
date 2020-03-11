import time
from adb_connector import *
from game_screen_connector import GameScreenConnector

playtime = 70

# Set this to true if you want to use generated data with TouchManager. Uses below coordinates path
UseGeneratedData = False
buttons_corrdinates_filename = "data.py"

# screen resolution. Needed for future normalization
width = 1080
heigth = 2220

screen_connector = GameScreenConnector(width, heigth)


def pixel_equals(px1, px2):
    return px1[0] == px2[0] and px1[1] == px2[1] and px1[2] == px2[2] and px1[3] == px2[3]


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
        'close_end': [540 / calculus_width, 1993 / calculus_heigth],
    }
    return buttons


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


def chooseLands():
    print("Main menu")
    tap('start')
    wait(3)


def play_lands():
    # Play intro
    wait(2)
    tap('ability_daemon_reject')
    tap('ability_left')
    swipe('n', 3)
    wait(5)
    tap('lucky_wheel_start')
    wait(5)
    swipe('n', 2)
    # First level
    swipe('n', 1.5)
    swipe('n', .5)


def main():
    global buttons, x, y, movements, attributes, width, heigth
    x, y, movements = getCoordinates()
    buttons = getGeneratedData() if UseGeneratedData else getDefaultButtons()
    device = get_device_id()
    if device is None:
        print("Error: no device discovered. Start adb server before executing this.")
        exit(1)
    print("Usb debugging device: %s" % device)
    while True:
        while not screen_connector.have_energy():
            print("No energy, waiting for one minute")
            wait(60)
        chooseLands()
        play_lands()
        while not screen_connector.checkEndFrame():
            print("Still playing, waiting for 5 secs")
            time.sleep(5)
        print("Game ended!!")
        wait(5)
        print("Going back to menu...")
        tap('close_end')
        wait(2)


def getGeneratedData():
    global buttons_corrdinates_filename
    if os.path.exists(buttons_corrdinates_filename):
        from data.py import getButtons
        return getButtons()


if __name__ == "__main__":
    main()
