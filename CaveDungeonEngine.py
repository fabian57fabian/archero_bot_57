import time
from datetime import datetime
from PyQt5.QtCore import QObject, pyqtSignal
from UsbConnector import UsbConnector
from GameScreenConnector import GameScreenConnector
from StatisticsManager import StatisticsManager
from Utils import loadJsonData, saveJsonData_oneIndent, saveJsonData_twoIndent, readAllSizesFolders, buildDataFolder, \
    getCoordFilePath


class CaveEngine(QObject):
    levelChanged = pyqtSignal(int)
    addLog = pyqtSignal(str)
    resolutionChanged = pyqtSignal(int, int)
    dataFolderChanged = pyqtSignal(str)
    noEnergyLeft = pyqtSignal()
    gameWon = pyqtSignal()

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
    coords_path = 'coords'
    buttons_filename = "buttons.json"
    movements_filename = "movements.json"
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

    def __init__(self, connectImmediately: bool = False):
        super(QObject, self).__init__()
        self.currentLevel = 0
        self.statisctics_manager = StatisticsManager()
        self.start_date = datetime.now()
        self.stat_lvl_start = 0
        self.screen_connector = GameScreenConnector()
        self.screen_connector.debug = False
        self.width, self.heigth = 1080, 2220
        self.device_connector = UsbConnector()
        self.device_connector.setFunctionToCallOnConnectionStateChanged(self.onConnectionStateChanged)
        self.buttons = {}
        self.movements = {}
        self.disableLogs = False
        self.stopRequested = False
        self.currentDataFolder = ''
        self.dataFolders = {}
        if connectImmediately:
            self.initDeviceConnector()

    def initDataFolders(self):
        self.dataFolders = readAllSizesFolders()
        deviceFolder = buildDataFolder(self.width, self.heigth)
        first_folder = list(self.dataFolders.keys())[0]
        if deviceFolder not in self.dataFolders:
            print("Error: not having %s coordinates. Trying with %s" % (deviceFolder, first_folder))
            deviceFolder = first_folder
        self.changeCurrentDataFolder(deviceFolder)

    def initdeviceconnector(self):
        self.device_connector.connect()

    def onConnectionStateChanged(self):
        if self.device_connector.connected:
            self.initDataFolders()
            self.screen_connector.changeDeviceConnector(self.device_connector)
            self.updateScreenSizeByPhone()

    def updateScreenSizeByPhone(self):
        if self.device_connector is not None:
            w, h = self.device_connector.adb_get_size()
            self.changeScreenSize(w, h)
            self.screen_connector.changeScreenSize(w, h)
        else:
            print("Device connector is none. initialize it before calling this method!")

    def changeCurrentDataFolder(self, new_folder):
        self.currentDataFolder = new_folder
        self.loadCoords()
        self.dataFolderChanged.emit(new_folder)

    def loadCoords(self):
        self.buttons = loadJsonData(getCoordFilePath(self.buttons_filename, sizePath=self.currentDataFolder))
        self.movements = loadJsonData(getCoordFilePath(self.movements_filename, sizePath=self.currentDataFolder))

    def setStopRequested(self):
        self.stopRequested = True
        self.screen_connector.stopRequested = True
        self.statisctics_manager.saveOneGame(self.start_date, self.stat_lvl_start, self.currentLevel)

    def changeScreenSize(self, w, h):
        self.width, self.heigth = w, h
        print("New resolution set: %dx%d" % (self.width, self.heigth))
        self.resolutionChanged.emit(w, h)

    def __unused__initConnection(self):
        device = self.device_connector._get_device_id()
        if device is None:
            print("Error: no device discovered. Start adb server before executing this.")
            exit(1)
        print("Usb debugging device: %s" % device)

    def log(self, log: str):
        """
        Logs an important move in the bot game
        """
        if not self.disableLogs:
            self.addLog.emit(log)

    def swipe_points(self, start, stop, s):
        start = self.buttons[start]
        stop = self.buttons[stop]
        print("Swiping between %s and %s in %f" % (start, stop, s))
        self.device_connector.adb_swipe(
            [start[0] * self.width, start[1] * self.heigth, stop[2] * self.width, stop[3] * self.heigth], s)

    def swipe(self, name, s):
        if self.stopRequested:
            exit()
        coord = self.movements[name]
        print("Swiping %s in %f" % (self.print_names_movements[name], s))
        self.log("Swipe %s in %.2f" % (self.print_names_movements[name], s))
        # convert back from normalized values
        self.device_connector.adb_swipe(
            [coord[0][0] * self.width, coord[0][1] * self.heigth, coord[1][0] * self.width, coord[1][1] * self.heigth],
            s)

    def tap(self, name):
        if self.stopRequested:
            exit()
        self.log("Tap %s" % name)
        # convert back from normalized values
        x, y = int(self.buttons[name][0] * self.width), int(self.buttons[name][1] * self.heigth)
        print("Tapping on %s at [%d, %d]" % (name, x, y))
        self.device_connector.adb_tap((x, y))

    def wait(self, s):
        decimal = s
        if int(s) > 0:
            decimal = s - int(s)
            for _ in range(int(s)):
                if self.stopRequested:
                    exit()
                time.sleep(1)
        if self.stopRequested:
            exit()
        time.sleep(decimal)

    def exit_dungeon_uncentered(self):
        # Center
        px, dir = self.screen_connector.getPlayerDecentering()
        self.wait(0.5)
        if dir == 'left':
            self.swipe('ne', 4)
        elif dir == 'right':
            self.swipe('nw', 4)
        elif dir == "center":
            self.swipe('n', 2)
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
                elif state == "in_game":
                    print("In game. Playing but level not ended")
            self.wait(1)

    def _exitEngine(self):
        self.statisctics_manager.saveOneGame(self.start_date, self.stat_lvl_start, self.currentLevel)
        exit(1)

    def reactGamePopups(self, ):
        state = ""
        i = 0
        while state != "in_game":
            if self.stopRequested:
                exit()
            if i > self.max_loops_game:
                print("Max loops reached")
                self.log("Max loops reached")
                self._exitEngine()
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
            elif state == "time_prize":
                print("Collecting time prize and ending game. Unexpected behaviour but managed")
                self.tap("collect_time_prize")
                self.wait(3)
                raise Exception('ended')
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
        self.swipe('n', 2)
        self.letPlay(self.playtime, is_boss=True)
        self.reactGamePopups()
        self.exit_dungeon_uncentered()

    def boss_lvl_manual(self):
        self.swipe('n', 2)
        self.swipe('n', 1.2)
        if self.currentLevel != 15:
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
            self._exitEngine()
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
        self.wait(5)
        if self.screen_connector.checkFrame('endgame'):
            self.tap('close_end')
            self.gameWon.emit()

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
        self.start_date = datetime.now()
        self.stat_lvl_start = self.currentLevel
        self.stopRequested = False
        self.screen_connector.stopRequested = False
        self.log("New game started")
        print("New game. Starting from level %d" % self.currentLevel)
        self.wait(4)
        if self.screen_connector.checkFrame("time_prize"):
            print("Collecting time prize")
            self.tap("resume")
            self.wait(3)
        if self.currentLevel == 0:
            if self.UseManualStart:
                a = input("Press enter to start a game (your energy bar must be at least 5)")
            else:
                while (not self.SkipEnergyCheck) and not self.screen_connector.checkFrame("least_5_energy"):
                    print("No energy, waiting for one minute")
                    self.noEnergyLeft.emit()
                    self.wait(60)
            self.chooseCave()
        try:
            self.play_cave()
        except Exception as exc:
            if exc.args[0] == 'ended':
                print("Game ended. Farmed a little bit...")
            elif exc.args[0] == 'unable_exit_dungeon':
                print("Unable to exit a room in a dungeon. Waiting instead of causing troubles")
                self._exitEngine()
            elif exc.args[0] == "unknown_screen_state":
                print("Unknows screen state. Exiting instead of doing trouble")
                self._exitEngine()
            else:
                print("Got an unknown exception: %s" % exc)
                self._exitEngine()
        self.statisctics_manager.saveOneGame(self.start_date, self.stat_lvl_start, self.currentLevel)
