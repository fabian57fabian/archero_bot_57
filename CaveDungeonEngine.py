import time

from PyQt5.QtCore import QObject, pyqtSignal

from pure_adb_connector import *
# from pure_adb_connector import *
from game_screen_connector import GameScreenConnector
import sys


class CaveEngine(QObject):
    levelChanged = pyqtSignal(int)
    addLog = pyqtSignal(str)

    # onDictionaryTapsChanged = pyqtSignal(dict)
    # onButtonLocationChanged = pyqtSignal(str)
    # onImageSelected = pyqtSignal()
    MAX_LEVEL = 20

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
    print_names_movements = {
        "n": "up",
        "s": "down",
        "e": "right",
        "w": "left",
        "ne": "up-right",
        "nw": "up-left",
        "se": "down-right",
        "sw": "down-left",
    }

    t_intro = 'intro'
    t_normal = 'normal'
    t_heal = 'heal'
    t_boss = 'boss'
    t_final_boss = 'final_boss'

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
        20: t_final_boss,
    }
    max_loops_game = 20

    def __init__(self):
        super(QObject, self).__init__()
        self.currentLevel = 0
        self.buttons = self.getGeneratedData()
        self.x, self.y, self.movements = self.getCoordinates()
        self.width, self.heigth = 0, 0
        self.screen_connector: GameScreenConnector = None
        self.initConnection()
        self.disableLogs = False
        self.stopRequested = False

    def setStopRequested(self):
        self.stopRequested = True
        self.screen_connector.stopRequested = True

    def initConnection(self):
        device = get_device_id()
        if device is None:
            print("Error: no device discovered. Start adb server before executing this.")
            exit(1)
        print("Usb debugging device: %s" % device)
        self.width, self.heigth = adb_get_size()
        print("Your resolution is %dx%d" % (self.width, self.heigth))
        self.screen_connector = GameScreenConnector(self.width, self.heigth)
        self.screen_connector.debug = False

    def log(self, log: str):
        """
        Logs an important move in the bot game
        """
        if not self.disableLogs:
            self.addLog.emit(log)

    def getCoordinates(self):
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

    def swipe_points(self, start, stop, s):
        start = self.buttons[start]
        stop = self.buttons[stop]
        print("Swiping between %s and %s in %f" % (start, stop, s))
        adb_swipe([start[0] * self.width, start[1] * self.heigth, stop[2] * self.width, stop[3] * self.heigth], s)

    def swipe(self, name, s):
        if self.stopRequested:
            exit()
        coord = self.movements[name]
        print("Swiping %s in %f" % (self.print_names_movements[name], s))
        self.log("Swipe %s in %.2f" % (self.print_names_movements[name], s))
        # convert back from normalized values
        adb_swipe([coord[0] * self.width, coord[1] * self.heigth, coord[2] * self.width, coord[3] * self.heigth], s)

    def tap(self, name):
        if self.stopRequested:
            exit()
        self.log("Tap %s" % name)
        # convert back from normalized values
        x, y = int(self.buttons[name][0] * self.width), int(self.buttons[name][1] * self.heigth)
        print("Tapping on %s at [%d, %d]" % (name, x, y))
        adb_tap((x, y))

    def wait(self, s):
        if self.stopRequested:
            exit()
        decimal = s
        if int(s) > 0:
            decimal = s - int(s)
            for _ in range(int(s)):
                time.sleep(1)
        time.sleep(decimal)

    def exit_dungeon_uncentered(self):
        # Center
        px, dir = self.screen_connector.getPlayerDecentering()
        self.wait(0.5)
        if dir == 'left':
            self.swipe('ne', 4)
        elif dir == 'right':
            self.swipe('nw', 4)
        else:
            self.swipe('n', 2)

    def exit_dungeon_uncentered_old(self):
        self.wait(2)
        upper_line = self.screen_connector.getHorLine("hor_up_line")
        print("Going trough door to exit...")
        self.wait(1)
        self.swipe('n', 2)
        self.wait(2)
        if not self.screen_connector.checkUpperLineHasChanged(upper_line):
            print("Not exiting, trying right...")
            self.wait(1)
            self.swipe('ne', 3)
            self.wait(2)
            if not self.screen_connector.checkUpperLineHasChanged(upper_line):
                print("Not exiting, trying left...")
                self.wait(1)
                self.swipe('nw', 4)
                self.wait(2)
                if not self.screen_connector.checkUpperLineHasChanged(upper_line):
                    raise Exception('unable_exit_dungeon')
        self.log("Exit level")

    def goTroughDungeon_old(self):
        print("Going through dungeon")
        self.log("Cross dungeon (old)")
        self.swipe('n', 1.5)
        self.swipe('w', .32)
        self.swipe('n', .5)
        self.swipe('e', .32)
        self.swipe('e', .32)
        self.swipe('n', .5)
        self.swipe('w', .325)
        self.swipe('n', 1.5)

    def goTroughDungeon(self):
        print("Going through dungeon")
        self.log("Cross dungeon")
        self.disableLogs = True
        self.swipe('n', 1.5)
        self.swipe('w', .32)
        self.swipe('n', .5)
        self.swipe('e', .32)
        self.swipe('e', .32)
        self.swipe('n', .7)
        self.swipe('w', .325)
        self.swipe('w', .3)
        self.swipe('n', 1.6)
        self.swipe('e', .28)
        self.swipe('n', 2)
        self.disableLogs = False

    def letPlay(self, _time: int, is_boss=False):
        check_exp_bar = not is_boss
        self.wait(2)
        print("Auto attacking")
        self.log("Auto attacking")
        experience_bar_line = self.screen_connector.getLineExpBar()
        recheck = False
        for i in range(_time, 0, -1):
            if i % 10 == 0 or recheck:
                recheck = False
                print("Checking screen...")
                self.log("screen check")
                frame = self.screen_connector.getFrame()
                state = self.screen_connector.getFrameState(frame)
                if state == "unknown":
                    print("Unknown screen situation detected. Checking again...")
                    self.wait(2)
                    if self.screen_connector.getFrameState() == "unknown":
                        raise Exception('unknown_screen_state')
                    else:
                        recheck = True
                        continue
                elif state == "in_game":
                    print("In game. Playing but level not ended")
                elif state == "endgame" or state == "repeat_endgame_question":
                    if state == "repeat_endgame_question":
                        self.wait(5)
                    print("Game ended")
                    self.log("Game over")
                    self.wait(1)
                    print("Going back to menu...")
                    self.tap('close_end')
                    self.wait(8)  # Wait to go to the menu
                    raise Exception('ended')
                elif state == "select_ability" or state == "fortune_wheel" or state == "devil_question" or state == "mistery_vendor" or state == "ad_ask":
                    print("Level ended. Collecting results for leveling up.")
                    self.wait(1)
                    return
                elif check_exp_bar and self.screen_connector.checkExpBarHasChanged(experience_bar_line, frame):
                    print("Experience gained!")
                    self.log("Gained experience")
                    self.wait(3)
                    return
            self.wait(1)

    def reactGamePopups(self, ):
        state = ""
        i = 0
        while state != "in_game":
            if self.stopRequested:
                exit()
            if i > self.max_loops_game:
                print("Max loops reached")
                self.log("Max loops reached")
                exit(1)
            self.log("screen check")
            state = self.screen_connector.getFrameState()
            print("state: %s" % state)
            if state == "select_ability":
                self.tap('ability_left')
                self.wait(3)
            elif state == "fortune_wheel":
                self.tap('lucky_wheel_start')
                self.wait(6)
            elif state == "repeat_endgame_question":
                self.tap('spin_wheel_back')
                self.wait(3)
            elif state == "devil_question":
                self.tap('ability_daemon_reject')
                self.wait(3)
            elif state == "ad_ask":
                self.tap('spin_wheel_back')
                self.wait(3)
            elif state == "mistery_vendor":
                self.tap('spin_wheel_back')
                self.wait(3)
            elif state == "special_gift_respin":
                self.tap('spin_wheel_back')
                self.wait(3)
            elif state == "angel_heal":
                self.tap('heal_right')
                self.wait(3)
            elif state == "on_pause":
                self.tap('resume')
                self.wait(3)
            elif state == "endgame":
                raise Exception('ended')
            i += 1
            self.wait(.1)

    def normal_lvl(self):
        self.goTroughDungeon()
        self.letPlay(self.playtime)
        self.reactGamePopups()
        self.exit_dungeon_uncentered()

    def normal_lvl_manual(self):
        self.goTroughDungeon()
        self.letPlay(self.playtime)
        self.tap('spin_wheel_back')  # guard not to click on mistery vendor
        self.wait(1)
        self.tap('ability_left')
        self.wait(1)
        self.tap('spin_wheel_back')  # guard not to click on watch
        self.wait(3)
        self.tap('ability_left')
        self.wait(2)
        self.tap('spin_wheel_back')  # guard not to click on watch or buy stuff (armor or others)
        self.wait(1)
        self.exit_dungeon_uncentered()

    def heal_lvl(self):
        self.swipe('n', 1.7)
        self.reactGamePopups()
        self.swipe('n', .8)
        self.reactGamePopups()
        self.exit_dungeon_uncentered()

    def heal_lvl_manual(self):
        self.swipe('n', 1.7)
        self.wait(1)
        self.tap('ability_daemon_reject')
        self.tap('ability_right')
        self.wait(1.5)
        self.tap('spin_wheel_back')
        self.wait(1)
        self.swipe('n', .8)
        self.wait(1.5)
        self.tap('spin_wheel_back')
        self.wait(1.5)
        self.exit_dungeon_uncentered()

    def boss_lvl(self):
        self.swipe('n', 2)
        self.swipe('n', 1.5)
        self.letPlay(self.playtime, is_boss=True)
        self.reactGamePopups()
        self.exit_dungeon_uncentered()

    def boss_lvl_manual(self):
        self.swipe('n', 2)
        self.swipe('n', 1.5)
        self.swipe('n', 1)
        self.letPlay(self.playtime, is_boss=True)
        self.tap('lucky_wheel_start')
        self.wait(6)
        self.tap('spin_wheel_back')
        self.wait(1.5)
        self.tap('ability_daemon_reject')
        self.tap('ability_left')
        self.wait(1.5)
        self.tap('spin_wheel_back')  # guard not to click on watch
        self.wait(1.5)
        self.tap('ability_left')  # Extra guard for level up
        self.wait(1.5)
        self.exit_dungeon_uncentered()

    def intro_lvl(self):
        self.wait(3)
        self.tap('ability_daemon_reject')
        self.tap('ability_left')
        self.swipe('n', 3)
        self.wait(5)
        self.tap('lucky_wheel_start')
        self.wait(5)
        self.swipe('n', 2)

    def play_cave(self):
        self.levelChanged.emit(self.currentLevel)
        if self.currentLevel < 0 or self.currentLevel > 20:
            print("level out of range: %d" % self.currentLevel)
            exit(1)
        while self.currentLevel <= self.MAX_LEVEL:
            print("Level %d: %s" % (self.currentLevel, str(self.levels_type[self.currentLevel])))
            if self.levels_type[self.currentLevel] == self.t_intro:
                self.intro_lvl()
            elif self.levels_type[self.currentLevel] == self.t_normal:
                self.normal_lvl()
            elif self.levels_type[self.currentLevel] == self.t_heal:
                self.heal_lvl()
            elif self.levels_type[self.currentLevel] == self.t_final_boss:
                self.boss_final()
            elif self.levels_type[self.currentLevel] == self.t_boss:
                self.boss_lvl()
            self.changeCurrentLevel(self.currentLevel + 1)

    def changeCurrentLevel(self, new_lvl):
        self.currentLevel = new_lvl
        self.levelChanged.emit(self.currentLevel)

    def boss_final(self):
        self.wait(2)
        self.swipe('w', 3)
        self.wait(50)
        self.tap('start')
        self.wait(2)
        self.swipe('n', 5)
        self.wait(.5)
        self.swipe('ne', 3)
        self.wait(5)
        self.tap('close_end')  # this is to wxit

    def chooseCave(self):
        print("Main menu")
        self.tap('start')
        self.wait(3)

    def quick_test_functions(self):
        pass

    def start_infinite_play(self):
        while True:
            self.start_one_game()
            self.currentLevel = 0

    def start_one_game(self):
        self.setStopRequested(False)
        self.log("New game started")
        print("New game. Starting from level %d" % self.currentLevel)
        if self.currentLevel == 0:
            if self.UseManualStart:
                a = input("Press enter to start a game (your energy bar must be at least 5)")
            else:
                while (not self.SkipEnergyCheck) and not self.screen_connector.checkFrame("least_5_energy"):
                    print("No energy, waiting for one minute")
                    self.wait(60)
            self.chooseCave()
        try:
            self.play_cave()
        except Exception as exc:
            if exc.args[0] == 'ended':
                print("Game ended. Farmed a little bit...")
            elif exc.args[0] == 'unable_exit_dungeon':
                print("Unable to exit a room in a dungeon. Waiting instead of causing troubles")
                exit(1)
            elif exc.args[0] == "unknown_screen_state":
                print("Unknows screen state. Exiting instead of doing trouble")
                exit(1)
            else:
                print("Got an unknown exception: %s" % exc)
                exit(1)

    def import_method(self, folder, file, name):
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

    def getGeneratedData(self):
        if os.path.exists(os.path.join(self.data_pack, self.buttons_corrdinates_filename)):
            method = self.import_method(self.data_pack, self.buttons_corrdinates_filename, "getButtons")
            return method()
        elif os.path.exists(os.path.join(self.data_pack, self.buttons_corrdinates_default_filename)):
            method = self.import_method(self.data_pack, self.buttons_corrdinates_default_filename, "getButtons")
            return method()
        else:
            print("No %s or d%s scripts are available. check your files." % (
                self.buttons_corrdinates_filename, self.buttons_corrdinates_default_filename))
            exit(1)
