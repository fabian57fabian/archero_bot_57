import json
import time
from datetime import datetime
from PyQt5.QtCore import QObject, pyqtSignal
from UsbConnector import UsbConnector
from GameScreenConnector import GameScreenConnector
from StatisticsManager import StatisticsManager
from Utils import loadJsonData, saveJsonData_oneIndent, saveJsonData_twoIndent, readAllSizesFolders, buildDataFolder, getCoordFilePath
import enum
import os


class HealingStrategy(str, enum.Enum):
    AlwaysHeal = "always_heal"
    AlwaysPowerUp = "always_power"


class CaveEngine(QObject):
    levelChanged = pyqtSignal(int)
    addLog = pyqtSignal(str)
    resolutionChanged = pyqtSignal(int, int)
    dataFolderChanged = pyqtSignal(str)
    noEnergyLeft = pyqtSignal()
    gameWon = pyqtSignal()
    healingStrategyChanged = pyqtSignal(HealingStrategy)
    currentDungeonChanged = pyqtSignal(int)

    # onDictionaryTapsChanged = pyqtSignal(dict)
    # onButtonLocationChanged = pyqtSignal(str)
    # onImageSelected = pyqtSignal()
    MAX_LEVEL = 20

    playtime = 60
    # Set this to true if you want to use generated data with TouchManager. Uses below coordinates path
    UseGeneratedData = False
    # Set this to true if keep receiving "No energy, waiting for 60 minute"
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

    chapters = {
        "1": "Verdant Prairie",
        "2": "Storm Desert",
        "3": "Abandoned Dungeon",
        "4": "Crystal Mines",
        "5": "Lost Castle",
        "6": "Cave of Bones",
        "7": "Barens of Shadow",
        "8": "Silent Expanse",
        "9": "Frozen Pinnacle",
        "10": "Land of Doom",
        "11": "The Capital",
        "12": "Dungeon of Traps",
        "13": "Lava Land",
        "14": "Eskimo Lands",
        "15": "Pharaoh's Chamber",
        "16": "Archaic Temple",
        "17": "Dragon Lair",
        "18": "Escape Chamber",
        "19": "devil's Tavern",
        "20": "Palace of Light",
        "21": "Nightmare Land",
        "22": "Tranquil Forest",
        "23": "Underwater Ruins",
        "24": "Silent Wilderness",
        "25": "Death Bar",
        "26": "Land of the Dead",
        "27": "Sky Castle",
        "28": "Sandy Town",
        "29": "dark forest",
        "30": "Shattered Abyss",
        "31": "Underwater City",
        "32": "Evil Castle",
        "33": "Aeon Temple",
        "34": "sakura Court"
    }

    allowed_chapters = [3, 6, 10]

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

    # lowest is better
    tier_list_abilities = {}

    def __init__(self, connectImmediately: bool = False):
        super(QObject, self).__init__()
        self.currentLevel = 0
        self.currentDungeon = 6 
        self.load_tier_list()
        self.statisctics_manager = StatisticsManager()
        self.start_date = datetime.now()
        self.stat_lvl_start = 0
        self.screen_connector = GameScreenConnector()
        self.screen_connector.debug = False
        self.width, self.heigth = 1080, 1920 
        self.device_connector = UsbConnector()
        self.device_connector.setFunctionToCallOnConnectionStateChanged(self.onConnectionStateChanged)
        self.buttons = {}
        self.movements = {}
        self.disableLogs = False
        self.stopRequested = False
        self.currentDataFolder = ''
        self.dataFolders = {}
        self.healingStrategy = HealingStrategy.AlwaysPowerUp
        self.current_settings = {}
        self.current_settings_path = 'current_settings.json'
        self.load_current_settings()
        self.centerAfterCrossingDungeon = False
        if connectImmediately:
            self.initDeviceConnector()
        self.check_seconds = 4

    def load_tier_list(self):
        print("Loading Abilities Tier List")
        file = os.path.join("datas", "abilities", "tier_list.json")
        with open(file) as file_in:
            self.tier_list_abilities = json.load(file_in)

    def initDataFolders(self):
        print("Initalizing Data Folders")
        self.dataFolders = readAllSizesFolders()
        deviceFolder = buildDataFolder(self.width, self.heigth)
        first_folder = list(self.dataFolders.keys())[0]
        if deviceFolder not in self.dataFolders:
            print("Error: not having %s coordinates. Trying with %s" % (deviceFolder, first_folder))
            deviceFolder = first_folder
        self.changeCurrentDataFolder(deviceFolder)

    def initdeviceconnector(self):
        print("Initalizing Device Connector")
        self.device_connector.connect()

    def _create_default_current_settings(self):
        print("Loading Default Settings")
        new_sett = {
            "healing_strategy": HealingStrategy.AlwaysHeal,
            "selected_dungeon": 6
        }
        saveJsonData_oneIndent(self.current_settings_path, new_sett)

    def load_current_settings(self):
        print("Loading Current Settings")
        if not os.path.exists(self.current_settings_path):
            print("Creating basic current settings...")
            self._create_default_current_settings()
        try:
            new_sett = loadJsonData(self.current_settings_path)
        except Exception as e:
            print("Unable to load existing {}: {}. setting to default.".format(self.current_settings_path, str(e)))
            self._create_default_current_settings()
            new_sett = loadJsonData(self.current_settings_path)
        if "healing_strategy" not in new_sett or "selected_dungeon" not in new_sett:
            print("Corrupted/errored current settings. ")
            print("Creating basic current settings...")
            self._create_default_current_settings()
        new_sett = loadJsonData(self.current_settings_path)
        self.current_settings = new_sett
        self.healingStrategy = HealingStrategy(self.current_settings["healing_strategy"])
        self.currentDungeon = int(self.current_settings["selected_dungeon"])

    def changeHealStrategy(self, strat: HealingStrategy):
        print("Loading Heal Strategy")
        self.healingStrategy = strat
        self.current_settings['healing_strategy'] = self.healingStrategy
        saveJsonData_oneIndent(self.current_settings_path, self.current_settings)
        self.healingStrategyChanged.emit(strat)

    def changeChapter(self, new_chapter):
        print("Loading Selected Chapter")
        self.currentDungeon = new_chapter
        self.current_settings['selected_dungeon'] = str(self.currentDungeon)
        saveJsonData_oneIndent(self.current_settings_path, self.current_settings)
        self.currentDungeonChanged.emit(new_chapter)

    def onConnectionStateChanged(self, connected):
        print("Detecting Connection State")
        if connected:
            print("Device Detected")
            self.initDataFolders()
            self.screen_connector.changeDeviceConnector(self.device_connector)
            self.updateScreenSizeByPhone()
        else:
            print("No Device Detected")

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
        print("Loading Coordinates")
        self.buttons = loadJsonData(getCoordFilePath(self.buttons_filename, sizePath = self.currentDataFolder))
        self.movements = loadJsonData(getCoordFilePath(self.movements_filename, sizePath = self.currentDataFolder))

    def setStopRequested(self):
        print("Stop Requested")
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
        print("Completing popup double check before exit")
        self.reactGamePopups()
        self.wait(1)
        self.log("No Loot Left")
        self.log("Leaveing Dungeon")
        if self.currentDungeon == 3:
            self.exit_movement_dungeon6()
        elif self.currentDungeon == 6:
            self.exit_movement_dungeon6()
        elif self.currentDungeon == 10:
            self.exit_movement_dungeon10()
        else:
            self.exit_movement_dungeon6()
        self.exit_dungeon_uncentered_simplified()

    def exit_movement_dungeon6(self):
        print("exit_dungeon_6")
        self.disableLogs = True
        self.swipe('w', 2)
        self.swipe('ne', 3)
        self.disableLogs = False

    def exit_movement_dungeon10(self):
        print("exit_dungeon_10")
        self.disableLogs = True
        self.swipe('e', 2)
        self.swipe('nw', 3)
        self.disableLogs = False

    def exit_dungeon_uncentered_simplified(self, do_second_check = True):
        self.wait(1)
        if do_second_check:
            print("conducting_dungeon_exit_simplified_check")
            if self.screen_connector.getFrameState() != "in_game":
                self.reactGamePopups()
                self.wait(1)
                self.exit_dungeon_uncentered_simplified(do_second_check = False)
                if self.currentDungeon == 3:
                    self.exit_movement_dungeon6()
                elif self.currentDungeon == 6:
                    self.exit_movement_dungeon6()
                elif self.currentDungeon == 10:
                    self.exit_movement_dungeon10()
                else:
                    self.exit_movement_dungeon6()
        print("exit_dungeon_uncentered_simplified")
        self.log("Left Dungeon")
        self.wait(1)  # Safety wait for extra check
   
    def goTroughDungeon10(self):
        print("Going through dungeon (designed for #10)")
        self.log("Crossing Dungeon 10")
        self.disableLogs = True
        self.swipe('n', .5)
        self.swipe('nw', 2.5)
        self.wait(2)
        self.swipe('ne', 1)
        self.wait(2)
        self.swipe('ne', 1.5)
        self.wait(2)
        self.swipe('nw', 2)
        self.swipe('s', .7)
        self.wait(2)
        self.swipe('e', .4)
        self.wait(2)
        self.swipe('ne', .5)
        self.swipe('n', 3)
        if self.currentLevel == 18:
            print("Adjusting lvl 18 Position")
            self.disableLogs = False
            self.log("Level 18 Argh!")
            self.disableLogs = True
            self.swipe('w', .4)
            self.swipe('s', .6)
            self.swipe('e', .6)
            self.swipe('n', 2.6)
            self.wait(3)
        self.disableLogs = False

    def goTroughDungeon_old(self):
        print("Going through dungeon old design 'S')")
        self.log("Cross dungeon (old)")
        self.disableLogs = True
        self.swipe('n', 1.5)
        self.swipe('w', .32)
        self.swipe('n', .5)
        self.swipe('e', .32)
        self.swipe('e', .32)
        self.swipe('n', .5)
        self.swipe('w', .325)
        self.swipe('n', 1.5)
        self.disableLogs = False

    def goTroughDungeon6(self):
        print("Going through dungeon (designed for #6)")
        self.log("Crossing Dungeon 6")
        self.disableLogs = True
        self.swipe('n', 1.5)
        self.swipe('w', .3)
        self.swipe('n', .6)
        self.wait(2)
        self.swipe('e', .6)
        self.swipe('n', .6)
        self.wait(2)
        self.swipe('w', .6)
        self.swipe('n', 1.5)
        self.wait(2)
        self.swipe('e', .3)
        self.swipe('n', 2)
        self.disableLogs = False

    def goTroughDungeon3(self):
        print("Going through dungeon (designed for #3)")
        self.log("Crossing Dungeon 3")
        self.disableLogs = True
        self.swipe('n', 1.5)
        self.swipe('w', .25)
        self.swipe('n', .5)
        self.wait(2)
        self.swipe('e', .25)
        self.swipe('n', 2)
        self.wait(2)
        # And now we need to go around possible obstacle
        self.swipe('w', 1)
        self.swipe('n', .5)
        self.swipe('e', 1)
        self.swipe('n', .3)
        self.disableLogs = False

    def goTroughDungeon(self):
        if self.currentDungeon == 3:
            self.goTroughDungeon3()
        elif self.currentDungeon == 6:
            self.goTroughDungeon6()
        elif self.currentDungeon == 10:
            self.goTroughDungeon10()
        else:
            self.goTroughDungeon_old()
        # Add movement if decentering is detected
        # Selfcenter scxript needs fixed don't caculate correctly
        # if self.centerAfterCrossingDungeon or self.currentLevel == 18: self.centerPlayer()

    def centerPlayer(self):
        px, dir = self.screen_connector.getPlayerDecentering()
        # Move in oppositye direction. Speed is made by y = mx + q
        # player location data is not acurate
        duration = 0.001 * abs(px)
        if px < self.screen_connector.door_width / 2:
            pass
        if dir == 'left':
            self.log("Centered Player <--")
            self.swipe('s', .5)
            self.swipe('e', duration)
        elif dir == 'right':
            self.log("Centered Player -->")
            self.swipe('s', .5)
            self.swipe('w', duration)
        elif dir == "center":
            pass

    def letPlay(self, _time: int, is_boss = False):
        check_exp_bar = not is_boss
        experience_bar_line = self.screen_connector.getLineExpBar()
        frame = self.screen_connector.getFrame()
        state = self.screen_connector.getFrameState(frame)
        self.wait(1)
        print("Auto attacking Let Play")
        recheck = False
        print("Checking for Exit")
        self.log("Checking for Exit")
        self.log("Do Some Patrols")
        for i in range(_time, 0, -1):
            if i % self.check_seconds == 0 or recheck:
                experience_bar_line = self.screen_connector.getLineExpBar()
                frame = self.screen_connector.getFrame()
                state = self.screen_connector.getFrameState(frame)
                recheck = False
                print("Checking screen... Let Play")
                print("Loop Counter / Kill Timer")
                print(i)
                print("state: %s" % state)
                if state == "unknown":
                    print("Unknown screen situation detected. Checking again...")
                    self.wait(2)
                    if self.screen_connector.getFrameState() == "unknown":
                        print("Unknown screen situation detected. Checking again x2...")
                        self.wait(2)
                        if self.screen_connector.getFrameState() == "unknown":
                            raise Exception('unknown_screen_state')
                        else:
                            recheck = True
                            continue
                    else:
                        recheck = True
                        continue
                elif state == "endgame" or state == "repeat_endgame_question":
                    if state == "repeat_endgame_question":
                        self.wait(5)
                    print("You died... Game Over")
                    self.log("You died... Game Over")
                    self.wait(1)
                    print("Going back to menu...")
                    self.log("Going back to menu")
                    self.tap('close_end')
                    self.wait(8)  # Wait to go to the menu
                    raise Exception('ended')
                elif state == "select_ability":
                    print("Level ended. New Abilities.")
                    self.log("New Abilities")
                    self.wait(1)
                    return
                elif state == "fortune_wheel" :
                    print("Level ended. Fortune Wheel.")
                    self.log("Fortune Wheel")
                    self.wait(1)
                    return
                elif state == "devil_question":
                    print("Level ended. Devil Arrived.")
                    self.log("Devil Arrived")
                    self.wait(1)
                    return
                elif state == "mistery_vendor":
                    print("Level ended. Mystery Vendor.")
                    self.log("Mystery Vendor")
                    self.wait(1)
                    return
                elif state == "ad_ask":
                    print("Level ended. Ad Ask.")
                    self.log("Ad Ask")
                    self.wait(1)
                    return
                elif check_exp_bar and self.screen_connector.checkExpBarHasChanged(experience_bar_line): #, frame):
                    print("Experience gained!")
                    self.log("Gained Experience")
                    self.wait(1)
                    return
                elif state == "in_game":
                    if self.screen_connector.checkDoorsOpen(frame):
                        print("Door is OPEN #1 <---------######")
                        self.log("The Door is Open")
                        self.wait(1)
                        return
                    if self.screen_connector.checkDoorsOpen1(frame):
                        print("Door is OPEN #2 <---------######")
                        self.log("The Door is Open")
                        self.wait(1)
                        return
                    if self.screen_connector.checkDoorsOpen2(frame):
                        print("Door is OPEN #3 <---------######")
                        self.log("The Door is Open")
                        self.wait(1)
                        return
                    else:
                        print("Still playing but level not ended")
                        print("state: %s" % state)
                        #added movement to increase efficency --AdminZero -------------------
                        self.log("Doing Patrol")
                        self.disableLogs = True
                        self.swipe('se', 0.6)
                        self.wait(3)
                        self.swipe('w', 0.5)
                        self.wait(3)
                        self.swipe('nw', 0.9)
                        self.wait(3)
                        self.swipe('e', 0.8)
                        self.disableLogs = False
                        #added movement to increase efficency --AdminZero -------------------
            self.wait(1)
            
    def _exitEngine(self):
        print ("Game Engine Closed")
        print("*** Saving Statistics #3 ***")
        self.statisctics_manager.saveOneGame(self.start_date, self.stat_lvl_start, self.currentLevel)
        exit(1)

    def reactGamePopups(self) -> int:
        state = ""
        i = 0
        while state != "in_game":
            if self.stopRequested:
                exit()
            if i > self.max_loops_game:
                print("Max React-Popups loops reached")
                self._manage_exit_from_endgame()    
            print("Checking screen... Game Popups")
            state = self.screen_connector.getFrameState()
            print("state: %s" % state)
            if state == "select_ability":
                self.chooseBestAbility()
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
                self.tap('heal_right' if self.healingStrategy == HealingStrategy.AlwaysHeal else 'heal_left')
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
            elif state == "menu_home":
                raise Exception('mainscreen')
            i += 1
            self.wait(.1)
        return i

    def chooseBestAbility(self):
        abilities = self.screen_connector.getAbilityType()
        try:
            t1 = self.tier_list_abilities[abilities['l']]
            t2 = self.tier_list_abilities[abilities['c']]
            t3 = self.tier_list_abilities[abilities['r']]
            best = ""
            if t1 < t2 and t1 < t3:
                to_press = 'ability_left'
                best = abilities['l']
            if t2 < t1 and t2 < t3:
                to_press = 'ability_center'
                best = abilities['c']
            if t3 < t2 and t3 < t1:
                to_press = 'ability_right'
                best = abilities['r']
            print("Found best ability as " + best)
            self.log("Choosing '{}'".format(best))
            self.disableLogs = True
            self.tap(to_press)
            self.disableLogs = False
        except Exception as e:
            print("Unable to correctly choose best ability. Randomly choosing left")
            self.log("Choosing 'Left Button'")
            self.disableLogs = True
            self.tap('ability_left')
            self.disableLogs = False

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
        self.chooseBestAbility()
        self.wait(1)
        self.tap('spin_wheel_back')  # guard not to click on watch
        self.wait(3)
        self.chooseBestAbility()
        self.wait(2)
        self.tap('spin_wheel_back')  # guard not to click on watch or buy stuff (armor or others)
        self.wait(1)
        self.exit_dungeon_uncentered()

    def heal_lvl(self):
        print("Centering Self")
        self.log("Centering Self")
        self.disableLogs = True
        self.swipe('s', 2)
        self.swipe('e', 3)
        self.swipe('w', .9)
        self.wait(1)
        self.disableLogs = False
        self.swipe('n', 1.5)
        self.reactGamePopups()
        self.swipe('n', .6)
        self.reactGamePopups()
        print("Exiting Heal")
        self.log("Leaving Healer")
        self.disableLogs = True
        self.swipe('e', .8)
        self.swipe('nw', 2)
        self.disableLogs = False
        self.log("Left Dungeon")
        self.wait(1)
        
    def heal_lvl_manual(self):
        print("Centering Self")
        self.log("Centering Self")
        self.disableLogs = True
        self.swipe('s', 2)
        self.swipe('e', 3)
        self.swipe('w', .9)
        self.wait(1)
        self.disableLogs = False
        self.swipe('n', 1.5)
        self.wait(1)
        self.tap('ability_daemon_reject')
        self.wait(1)
        self.tap('heal_right' if self.healingStrategy == HealingStrategy.AlwaysHeal else 'heal_left')
        self.wait(1.5)
        self.tap('spin_wheel_back')
        self.wait(1)
        self.swipe('n', .6)
        self.wait(1.5)
        self.tap('spin_wheel_back')
        self.wait(1.5)
        print("Exiting Heal")
        self.log("Leaving Healer")
        self.disableLogs = True
        self.swipe('e', .8)
        self.swipe('nw', 2)
        self.disableLogs = False
        self.log("Left Dungeon")
        self.wait(1)

    def boss_lvl(self):
        print("Attacking Boss")
        self.log("Attacking Boss")
        self.disableLogs = True
        self.wait(3)
        self.swipe('n', 1.5)
        self.wait(4)
        self.swipe('e', .7)
        self.wait(4)
        self.swipe('nw', 2.5)
        self.wait(2)
        self.swipe('ne', 2.5)
        self.wait(2)
        self.swipe('w', .3)
        self.swipe('nw', .7)
        self.disableLogs = False
        self.letPlay(self.playtime, is_boss = True)
        self.reactGamePopups()
        self.wait(1)
        self.log("Moving to Door")
        self.disableLogs = True
        self.swipe('s', .3)
        self.swipe('w', 1.5)
        self.swipe('n', 2)
        self.swipe('e', 1)
        self.disableLogs = False
        self.exit_dungeon_uncentered()

    def boss_lvl_manual(self):
        print("Attacking Boss")
        self.log("Attacking Boss")
        self.disableLogs = True
        self.wait(3)
        self.swipe('n', 1.5)
        self.wait(4)
        self.swipe('e', .7)
        self.wait(4)
        self.swipe('nw', 2.5)
        self.wait(2)
        self.swipe('ne', 2.5)
        self.wait(2)
        self.swipe('w', .3)
        self.swipe('nw', .7)
        self.disableLogs = False
        self.letPlay(self.playtime, is_boss = True)
        self.tap('lucky_wheel_start')
        self.wait(6)
        self.tap('spin_wheel_back')
        self.wait(1.5)
        self.tap('ability_daemon_reject')
        self.chooseBestAbility()
        self.wait(1.5)
        self.tap('spin_wheel_back')  # guard not to click for ad watch
        self.wait(1.5)
        self.chooseBestAbility()  # Extra guard for level up
        self.wait(1.5)
        self.log("Moving to Door")
        self.disableLogs = True
        self.swipe('s', .3)
        self.swipe('w', 1.5)
        self.swipe('n', 2)
        self.swipe('e', 1)
        self.disableLogs = False
        self.exit_dungeon_uncentered()

    def boss_final(self):
        state = self.screen_connector.getFrameState()
        print("state: %s" % state)
        print("Final Boss")
        self.log("Final Boss Appeared")
        self.wait(1)
        self.log("Attacking Boss")
        self.wait(2)
        self.swipe('w', 2)
        #BOSS LOOP BELOW HERE ********************************
        max_wait = 5
        sleep_btw_screens = 5
        i = 0
        while i < max_wait:
            self.wait(sleep_btw_screens)
            if self.screen_connector.checkBoss3Died():
                print("boss dead and door open #3")
                self.log("Boss Dead")
                break
            if self.screen_connector.checkBoss6Died():
                print("boss dead and door open #6")
                self.log("Boss Dead")
                break
            if self.screen_connector.checkBoss10Died():
                print("boss dead and door open #10")
                self.log("Boss Dead")
                break
            print(i)
            i += 1
        #BOSS LOOP ABOVE HERE ********************************
        state = self.screen_connector.getFrameState()
        print("state: %s" % state)
        self.reactGamePopups()
        self.log("No Loot Left")
        print("Exiting the Dungeon Final Boss")
        self.log("Leaving Dungeon")
        self.disableLogs = True
        self.wait(1)
        self.swipe('n', 5)
        self.wait(.25)
        self.swipe('ne', 3)
        self.disableLogs = False

    def intro_lvl(self):
        self.wait(6) #wait for game screen to refresh?
        print("Geting Start Items")
        self.disableLogs = True
        self.tap('ability_daemon_reject')
        self.disableLogs = False
        self.wait(4)
        self.chooseBestAbility()
        self.swipe('n', 3)
        self.wait(4)
        self.tap('lucky_wheel_start')
        self.wait(4)
        self.reactGamePopups()
        self.log("Leaving Start Room!")
        self.wait(1)
        self.swipe('n', 2)
        self.log("Entered Dungeon!")       

    def play_cave(self):
        if self.currentLevel < 0 or self.currentLevel > 20:
            print("level out of range: %d" % self.currentLevel)
            self._exitEngine()
        while self.currentLevel <= self.MAX_LEVEL:
            print("***********************************")
            print("Level %d: %s" % (self.currentLevel, str(self.levels_type[self.currentLevel])))
            print("***********************************")
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
                self.wait(4)
            self.changeCurrentLevel(self.currentLevel + 1)
        print("*** Saving Statistics #1 ***")
        self.statisctics_manager.saveOneGame(self.start_date, self.stat_lvl_start, self.currentLevel)
        if self.screen_connector.checkFrame('endgame'):
            print("You won!")
            self.log("You Won!")
            self.gameWon.emit()
        self._manage_exit_from_endgame()

    def _manage_exit_from_endgame(self):
        print("manage_exit_from_endgame")
        self.log("Exiting Endgame")
        self.wait(10)
        state = self.screen_connector.getFrameState()
        if state == 'menu_home':
            return
        if not state == 'endgame':
            # exit if i'm not on ending screen
            raise Exception("unknown screen")
        self.tap('close_end')
        self.wait(4)
        is_endgame = self.screen_connector.checkFrame('endgame')
        # check if i actually exited
        if is_endgame:
            print("Endgame Exit Double Check")
            self.tap('close_end')
            self.wait(3)
        is_endgame = self.screen_connector.checkFrame('endgame')
        if is_endgame:
            # can't exit
            raise Exception("unknown screen")

    def changeCurrentLevel(self, new_lvl):
        self.currentLevel = new_lvl
        self.levelChanged.emit(self.currentLevel)       

    def quick_test_functions(self):
        pass

    def start_infinite_play(self):
        # Only for test purposes on pressing play
        # self.quick_test_functions()
        while True:
            self.start_one_game()
            self.currentLevel = 0

    def start_one_game(self):
        i = 0
        while i < self.max_loops_game:
            self.screen_connector.checkDoorsOpen()
            self.start_date = datetime.now()
            self.stat_lvl_start = self.currentLevel
            self.stopRequested = False
            self.screen_connector.stopRequested = False
            self.log("New Game Started")
            print("New game. Starting from level %d" % self.currentLevel)
            self.wait(1)
            if self.screen_connector.checkFrame("popup_vip_rewards"):
                print("Collecting VIP-Privilege Rewards 1")
                self.log("VIP-Privilege Rewards 1")
                self.tap("collect_vip_rewards")
                self.wait(6)
                self.tap("close_vip_rewards")#click again somewhere to close popup with token things
                self.wait(6)
            if self.screen_connector.checkFrame("popup_vip_rewards"):
                print("Collecting VIP-Privilege Rewards 2")
                self.log("VIP-Privilege Rewards 2")
                self.tap("collect_vip_rewards")
                self.wait(6)
                self.tap("close_vip_rewards")#click again somewhere to close popup with token things
                self.wait(6)
            if self.screen_connector.checkFrame("time_prize"):
                print("Collecting time prize")
                self.log("Collecting Time Prize")
                self.tap("resume")
                self.wait(6)
            if self.screen_connector.checkFrame("popup_home_patrol"):
                print("Collecting time patrol")
                self.log("Collecting Time Patrol")
                self.tap("collect_hero_patrol")
                self.wait(6)
                self.tap("collect_hero_patrol")#click again somewhere to close popup with token things
            if self.screen_connector.checkFrame("btn_home_time_reward"):
                self.tap("close_hero_patrol")
                self.log("Closing Patrol")
                self.wait(6)
            if self.currentLevel == 0:
                if self.UseManualStart:
                    a = input("Press enter to start a game (your energy bar must be at least 5)")
                    self.log("Beging Dungeon Raid!")
                else:
                    while (not self.SkipEnergyCheck) and not self.screen_connector.checkFrame("least_5_energy"):
                        print("No energy, waiting for 60 minute")
                        self.log("No Energy")
                        self.noEnergyLeft.emit()
                        self.wait(3605)
            try:
                if self.currentLevel == 0:
                    print("start_one_game level = 0")
                    self.chooseCave()
                else:
                    print("start_one_game level > 0")
                    self.play_cave()
            except Exception as exc:
                if exc.args[0] == 'mainscreen':
                    print("Main Menu. Restarting game now.")
                    self.log("Restarting game now")
                    return
                if exc.args[0] == 'ended':
                    print("Game ended. Farmed a little bit...")
                    self.log("Game ended. Farmed a little bit...")
                    self.pressCloseEndIfEndedFrame()
                elif exc.args[0] == 'unable_exit_dungeon':
                    print("Unable to exit a room in a dungeon. Waiting instead of causing troubles")
                    self.log("Im Stuck in this room... halp!")
                    self._exitEngine()
                elif exc.args[0] == "unknown_screen_state":
                    print("Unknows screen state. Exiting instead of doing trouble")
                    self.log("Unknown Screens... halp!")
                    self._exitEngine()
                else:
                    print("Got an unknown exception: %s" % exc)
                    self.log("Unknown Problem... halp!")
                    self._exitEngine()
            self.pressCloseEndIfEndedFrame()
            print("*** Saving Statistics #2 ***")
            self.statisctics_manager.saveOneGame(self.start_date, self.stat_lvl_start, self.currentLevel)
            print("Completed Farm Loop ")
            print(i)            
            i += 1
        
    def chooseCave(self):
        self.levelChanged.emit(self.currentLevel)
        self.wait(1)
        print("Choosing Cave Start")
        self.log("Main Menu")
        self.tap('start')
        self.wait(3)
        self.tap('start_no_raid')
        self.wait(3)
        self.play_cave()

    def pressCloseEndIfEndedFrame(self):
        print("pressCoseEndIfEndedFrame Check")
        self.currentLevel = 0
        if self.screen_connector.checkFrame('endgame'):
            print("Going back to main Menu")
            self.log("Game ended")
            self.wait(2)
            self.tap('close_end')
            slef.wait(8) #wait for go back to main menu
