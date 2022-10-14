import json
import time
from datetime import datetime
from PyQt5.QtCore import QObject, pyqtSignal
from UsbConnector import UsbConnector
from GameScreenConnector import GameScreenConnector
from StatisticsManager import StatisticsManager
from Utils import loadJsonData, saveJsonData_oneIndent, saveJsonData_twoIndent, readAllSizesFolders, buildDataFolder, getCoordFilePath
from GameChapters import ChapterInfo, ChapterLevelType, DungeonLevelType, BuildChapters, BuildLevelsTypes, MaxLevelFromType
import enum
import os

class HealingStrategy(str, enum.Enum):
    AlwaysHeal = "always_heal"
    AlwaysPowerUp = "always_power"
    SmartHeal = "smart_heal"

class EnergyStrategy(str, enum.Enum):
    AlwaysBuy = "always_buy"
    AlwaysBuy2 = "always_buy2"
    AlwaysBuy3 = "always_buy3"
    AlwaysBuy4 = "always_buy4"
    AlwaysIgnore = "always_ignore"

class VIPSub(str, enum.Enum):
    TrueVIP = "vip_true"
    FalseVIP = "vip_false"

class BattlepassAdvSub(str, enum.Enum):
    TrueBPAdv = "bpadv_true"
    FalseBPAdv = "bpadv_false"

class ReviveIfDead(str, enum.Enum):
    TrueRevive = "revive_true"
    FalseRevive = "revive_false"

class CaveEngine(QObject):
    levelChanged = pyqtSignal(int)
    addLog = pyqtSignal(str)
    resolutionChanged = pyqtSignal(int, int)
    dataFolderChanged = pyqtSignal(str)
    noEnergyLeft = pyqtSignal()
    gameWon = pyqtSignal()
    gamePaused = pyqtSignal()
    healingStrategyChanged = pyqtSignal(HealingStrategy)
    energyStrategyChanged = pyqtSignal(EnergyStrategy)
    vipSubChanged = pyqtSignal(VIPSub)
    bpadvSubChanged = pyqtSignal(BattlepassAdvSub)
    reviveIfDeadChanged = pyqtSignal(ReviveIfDead)
    currentDungeonChanged = pyqtSignal(int)
    
    max_level = 20 # set loops for playCave and linked to GUI logs(default is 20, DO NOT CHANGE)
    playtime = 50 # set loop time for letPlay (default 50, total loops = playtime/self.check_seconds)
    max_loops_popup = 10 # set loops for reactGamePopups (default 10, times to check for popups)
    max_loops_game = 100 # set loops for start_one_game (default 100, farming cycles)
    max_wait = 5 # set loops for final_boss (default 5, increase sleep screens if need more time)
    sleep_btw_screens = 8 # set wait between loops for final_boss (default 8, in seconds)

    UseGeneratedData = False # Set True to use TouchManager generated data
    
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

    allowed_chapters = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]

    ''' dictionary of strings (chapter number), each one is a ChapterInfo '''
    chapters_info = BuildChapters()

    ''' dictionary of ChapterLevelType, each one is a dictionary of int num -> DungeonLevelType '''
    levels_info = BuildLevelsTypes()


    def __init__(self, connectImmediately: bool = False):
        super(QObject, self).__init__()
        self.debug = False # set True to show print debug messages in console
        self.deadcheck = False # controled by GUI dropdown, works <50% of time to revive; costs gems unless BPAdv Sub
        self.smartHealChoice = False # controled by GUI dropdown, works >90% of the time
        self.currentLevel = 0
        self.currentDungeon = 6 
        self.check_seconds = 5
        self.energy_count = 1
        self.load_tier_list()
        self.statisctics_manager = StatisticsManager()
        self.start_date = datetime.now()
        self.stat_lvl_start = 0
        self.screen_connector = GameScreenConnector()
        self.screen_connector.debug = False # set true to see screen_connector degbug messages in console
        self.width, self.heigth = 1080, 1920 
        self.device_connector = UsbConnector()
        self.device_connector.setFunctionToCallOnConnectionStateChanged(self.onConnectionStateChanged)
        self.buttons = {}
        self.movements = {}
        self.disableLogs = False # do not change
        self.stopRequested = False # do not change
        self.currentDataFolder = ''
        self.dataFolders = {}
        self.healingStrategy = HealingStrategy.SmartHeal
        self.energyStrategy = EnergyStrategy.AlwaysIgnore
        self.vipSub = VIPSub.FalseVIP
        self.bpadvSub = BattlepassAdvSub.FalseBPAdv
        self.reviveIfDead = ReviveIfDead.FalseRevive
        self.centerAfterCrossingDungeon = False # do not ghange
        self.current_settings = {}
        self.current_settings_path = 'current_settings.json'
        self.load_current_settings()
        if connectImmediately:
            self.initDeviceConnector()

    def load_tier_list(self):
        if self.debug: print("Loading Abilities Tier List")
        file = os.path.join("datas", "abilities", "tier_list.json")
        with open(file) as file_in:
            self.tier_list_abilities = json.load(file_in)

    def initDataFolders(self):
        if self.debug: print("Initalizing Data Folders")
        self.dataFolders = readAllSizesFolders()
        deviceFolder = buildDataFolder(self.width, self.heigth)
        first_folder = list(self.dataFolders.keys())[0]
        if deviceFolder not in self.dataFolders:
            if self.debug: print("Error: not having %s coordinates. Trying with %s" % (deviceFolder, first_folder))
            deviceFolder = first_folder
        self.changeCurrentDataFolder(deviceFolder)

    def initdeviceconnector(self):
        if self.debug: print("Initalizing Device Connector")
        self.device_connector.connect()

    def _create_default_current_settings(self):
        if self.debug: print("Loading Default Settings")
        new_sett = {
            "selected_dungeon": 3,
            "healing_strategy": HealingStrategy.SmartHeal,
            "energy_strategy": EnergyStrategy.AlwaysIgnore,
            "vip_sub": VIPSub.FalseVIP,
            "bpadv_sub": BattlepassAdvSub.FalseBPAdv,
            "revive_ifdead": ReviveIfDead.FalseRevive
        }
        saveJsonData_oneIndent(self.current_settings_path, new_sett)

    def load_current_settings(self):
        if self.debug: print("Loading Current Settings")
        if not os.path.exists(self.current_settings_path):
            if self.debug: print("Creating basic current settings...")
            self._create_default_current_settings()
        try:
            new_sett = loadJsonData(self.current_settings_path)
        except Exception as e:
            if self.debug: print("Unable to load existing {}: {}. setting to default.".format(self.current_settings_path, str(e)))
            self._create_default_current_settings()
            new_sett = loadJsonData(self.current_settings_path)
        if "selected_dungeon" not in new_sett or "healing_strategy" not in new_sett or "energy_strategy" not in new_sett or "vip_sub" not in new_sett or "bpadv_sub" not in new_sett or "revive_ifdead" not in new_sett:
            if self.debug: print("Corrupted/errored current settings. ")
            if self.debug: print("Creating basic current settings...")
            self._create_default_current_settings()
        new_sett = loadJsonData(self.current_settings_path)
        self.current_settings = new_sett
        self.currentDungeon = int(self.current_settings["selected_dungeon"])
        self.healingStrategy = HealingStrategy(self.current_settings["healing_strategy"])
        self.energyStrategy = EnergyStrategy(self.current_settings["energy_strategy"])
        self.vipSub = VIPSub(self.current_settings["vip_sub"])
        self.bpadvSub = BattlepassAdvSub(self.current_settings["bpadv_sub"])
        self.reviveIfDead = ReviveIfDead(self.current_settings["revive_ifdead"])

    def changeHealStrategy(self, strat: HealingStrategy):
        print("Loading Heal Strategy")
        self.healingStrategy = strat
        self.current_settings['healing_strategy'] = self.healingStrategy
        saveJsonData_oneIndent(self.current_settings_path, self.current_settings)
        self.healingStrategyChanged.emit(strat)

    def changeEnergyStrategy(self, strat1: EnergyStrategy):
        print("Loading Energy Strategy")
        self.energyStrategy = strat1
        self.current_settings['energy_strategy'] = self.energyStrategy
        saveJsonData_oneIndent(self.current_settings_path, self.current_settings)
        self.energyStrategyChanged.emit(strat1)

    def changeVIPSub(self, strat2: VIPSub):
        print("Updating VIP Subscripton")
        self.vipSub = strat2
        self.current_settings['vip_sub'] = self.vipSub
        saveJsonData_oneIndent(self.current_settings_path, self.current_settings)
        self.vipSubChanged.emit(strat2)

    def changeBattlepassAdvSub(self, strat3: BattlepassAdvSub):
        print("Updating Battlepass Choice")
        self.bpadvSub = strat3
        self.current_settings['bpadv_sub'] = self.bpadvSub
        saveJsonData_oneIndent(self.current_settings_path, self.current_settings)
        self.bpadvSubChanged.emit(strat3)

    def changeReviveIfDead(self, strat4: ReviveIfDead):
        print("Updating Revive Choice")
        self.reviveIfDead = strat4
        self.current_settings['revive_ifdead'] = self.reviveIfDead
        saveJsonData_oneIndent(self.current_settings_path, self.current_settings)
        self.reviveIfDeadChanged.emit(strat4)
        
    def changeChapter(self, new_chapter):
        print("Loading Selected Chapter")
        self.currentDungeon = new_chapter
        self.current_settings['selected_dungeon'] = str(self.currentDungeon)
        saveJsonData_oneIndent(self.current_settings_path, self.current_settings)
        self.currentDungeonChanged.emit(new_chapter)

    def onConnectionStateChanged(self, connected):
        if self.debug: print("Detecting Connection State")
        if connected:
            if self.debug: print("Device Detected")
            self.initDataFolders()
            self.screen_connector.changeDeviceConnector(self.device_connector)
            self.updateScreenSizeByPhone()
        else:
            if self.debug: print("No Device Detected")

    def updateScreenSizeByPhone(self):
        if self.device_connector is not None:
            w, h = self.device_connector.adb_get_size()
            self.changeScreenSize(w, h)
            self.screen_connector.changeScreenSize(w, h)
        else:
            if self.debug: print("Device connector is none. initialize it before calling this method!")

    def changeCurrentDataFolder(self, new_folder):
        self.currentDataFolder = new_folder
        self.loadCoords()
        self.dataFolderChanged.emit(new_folder)

    def loadCoords(self):
        if self.debug: print("Loading Coordinates")
        self.buttons = loadJsonData(getCoordFilePath(self.buttons_filename, sizePath = self.currentDataFolder))
        self.movements = loadJsonData(getCoordFilePath(self.movements_filename, sizePath = self.currentDataFolder))

    def setStopRequested(self):
        if self.debug: print("Stop Requested")
        self.stopRequested = True
        self.screen_connector.stopRequested = True
        if self.currentDungeon == 3 or self.currentDungeon == 6 or self.currentDungeon == 10 or self.currentDungeon == 16:
            if self.debug: print("*** Saving Statistics - Game Stopped ***")
            self.statisctics_manager.saveOneGame(self.start_date, self.stat_lvl_start, self.currentLevel)

    def setStartRequested(self):
        if self.debug: print("Start Requested")
        self.stopRequested = False
        self.screen_connector.stopRequested = False
        self.gamePaused.emit()

    def changeScreenSize(self, w, h):
        self.width, self.heigth = w, h
        if self.debug: print("New resolution set: %dx%d" % (self.width, self.heigth))
        self.resolutionChanged.emit(w, h)
        
    def __unused__initConnection(self):
        device = self.device_connector._get_device_id()
        if device is None:
            if self.debug: print("Error: no device discovered. Start adb server before executing this.")
            exit(1)
        if self.debug: print("Usb debugging device: %s" % device)

    def log(self, log: str):
        """
        Logs an important move in the bot game
        """
        if not self.disableLogs:
            self.addLog.emit(log)

    def swipe_points(self, start, stop, s):
        start = self.buttons[start]
        stop = self.buttons[stop]
        if self.debug: print("Swiping between %s and %s in %f" % (start, stop, s))
        self.device_connector.adb_swipe(
            [start[0] * self.width, start[1] * self.heigth, stop[2] * self.width, stop[3] * self.heigth], s)

    def swipe(self, name, s):
        if self.stopRequested:
            exit()
        coord = self.movements[name]
        if self.debug: print("Swiping %s in %f" % (self.print_names_movements[name], s))
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
        if self.debug: print("Tapping on %s at [%d, %d]" % (name, x, y))
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

    def changeCurrentLevel(self, new_lvl):
        self.currentLevel = new_lvl
        self.levelChanged.emit(self.currentLevel)

    def quick_test_functions(self):
        pass

    def start_infinite_play(self):
        while True:
            self.start_one_game()
            self.currentLevel = 0

    def exit_dungeon_uncentered(self):
        if self.debug: print("exit_dungeon_uncentered")
        if self.screen_connector.getFrameState() != "in_game":
            self.reactGamePopups()
        self.log("No Loot Left")
        self.log("Leaveing Dungeon")
        if self.currentDungeon == 3 or self.currentDungeon == 6:
            self.exit_movement_dungeon6()
        elif self.currentDungeon == 7 or self.currentDungeon == 14:
            self.exit_movement_dungeon_7()
        elif self.currentDungeon == 10:
            self.exit_movement_dungeon10()
        elif self.currentDungeon == 16:
            self.exit_movement_dungeon16()
        else:
            self.exit_movement_dungeon_old()
        self.log("Left Dungeon")
        self.wait(0.5) # wait to load to GUI
        self.exit_dungeon_uncentered_simplified()

    def exit_dungeon_uncentered_simplified(self, do_second_check = True):
        if do_second_check:
            if self.debug: print("exit_dungeon_uncentered_simplified_check")
            if self.screen_connector.getFrameState() == "endgame":
                if self.debug: print("Endgame Detected and Return")
                self.exit_dungeon_uncentered_simplified(do_second_check = False)
                return
            elif self.screen_connector.getFrameState() != "in_game":
                if self.debug: print("NOT in_game Detected")
                self.reactGamePopups()
                self.exit_dungeon_uncentered_simplified(do_second_check = False)
                if self.currentDungeon == 3 or self.currentDungeon == 6:
                    self.exit_movement_dungeon6()
                elif self.currentDungeon == 7 or self.currentDungeon == 14:
                    self.exit_movement_dungeon_7()
                elif self.currentDungeon == 10 or self.currentDungeon == 16:
                    self.exit_movement_dungeon10()
                else:
                    self.exit_movement_dungeon_old()
                self.log("Left Dungeon Again")
                self.wait(0.5) # wait to load to GUI
        if self.debug: print("exit_dungeon_uncentered_simplified")
        
    def exit_movement_dungeon_old(self):
        if self.debug: print("exit_dungeon_old 'Improved'")
        self.disableLogs = True
        #self.centerPlayer()
        self.swipe('n', 3)
        self.swipe('ne', .5)
        self.swipe('nw', 3)
        self.swipe('ne', 3)
        self.swipe('nw', 3)
        self.swipe('ne', 3)
        self.swipe('w', .7)

    def exit_movement_dungeon_7(self):
        if self.debug: print("exit_dungeon_7")
        self.disableLogs = True    
        self.swipe('w', .7)
        self.swipe('ne', 1.9)
        self.disableLogs = False

    def exit_movement_dungeon6(self):
        if self.debug: print("exit_dungeon_6")
        self.disableLogs = True
        self.swipe('w', 2)
        self.swipe('ne', 3)
        self.disableLogs = False

    def exit_movement_dungeon10(self): 
        if self.debug: print("exit_dungeon_10")
        self.disableLogs = True
        self.swipe('e', 1.5)
        self.swipe('nw', 3)
        self.disableLogs = False

    def exit_movement_dungeon16(self): 
        if self.debug: print("exit_dungeon_16")
        self.disableLogs = True
        self.swipe('e', 1.2)
        self.swipe('nw', 3)
        self.disableLogs = False
   
    def goTroughDungeon10(self):
        if self.debug: print("Going through dungeon (designed for #10)")
        self.log("Crossing Dungeon 10")
        self.disableLogs = True
        self.swipe('n', .5)
        self.swipe('nw', 2.5)
        self.swipe('ne', 2.5)
        self.swipe('nw', 1.8)
        self.swipe('ne', 1)
        self.swipe('w', .7)
        self.swipe('s', .6)
        self.swipe('e', .35)
        self.swipe('ne', .4)
        self.swipe('n', 2.5)
        self.swipe('s', .3)
        self.swipe('w', .35)
        self.swipe('nw', .4)
        self.swipe('n', 1)
        if self.currentLevel == 18:
            self.swipe('w', .3)
            self.swipe('s', .35)
            self.swipe('ne', .4)
            self.swipe('n', .4)
        self.disableLogs = False

    def goTroughDungeon16(self):
        if self.debug: print("Going through dungeon (designed for #16)")
        self.log("Crossing Dungeon 16")
        self.disableLogs = True
        self.swipe('n', .5)
        self.swipe('nw', 2.5)
        self.swipe('ne', 2.5)
        self.swipe('nw', 1.8)
        self.swipe('ne', 1)
        self.swipe('w', .7)
        if self.currentLevel == 11 or self.currentLevel == 18:
            self.swipe('sw', .6)
            self.swipe('nw', .8)
        self.swipe('se', .65)
        self.swipe('e', .7)
        self.swipe('nw', .55)
        self.swipe('ne', .7)
        self.swipe('w', .3)
        self.swipe('s', .6)
        self.swipe('sw', .3)
        self.swipe('nw', .7)
        if self.currentLevel == 11 or self.currentLevel == 18:
            self.swipe('e', .3)
            self.swipe('n', .3)
            self.swipe('nw', .4)
        self.swipe('ne', .55)
        self.swipe('w', .3)
        self.swipe('n', 1.5)
        self.disableLogs = False

    def goTroughDungeon6(self):
        if self.debug: print("Going through dungeon (designed for #6)")
        self.log("Crossing Dungeon 6")
        self.disableLogs = True
        self.swipe('n', 1.5)
        self.swipe('w', .3)
        self.swipe('n', .6)
        self.swipe('e', .6)
        self.swipe('n', .6)
        self.swipe('w', .6)
        self.swipe('n', 1.5)
        self.swipe('e', .3)
        self.swipe('n', 2)
        self.disableLogs = False

    def goTroughDungeon3(self):
        if self.debug: print("Going through dungeon (designed for #3)")
        self.log("Crossing Dungeon 3")
        self.disableLogs = True
        self.swipe('n', 1.5)
        self.swipe('w', .25)
        self.swipe('n', .5)
        self.swipe('e', .25)
        self.swipe('n', 2)
        self.swipe('w', 1)
        self.swipe('n', .5)
        self.swipe('e', 1)
        self.swipe('n', 1.5)
        self.disableLogs = False

    def goTroughDungeon_old(self):
        if self.debug: print("Going through dungeon old 'Improved'")
        self.log("Crossing Dungeon (Improved)")
        self.disableLogs = True
        self.swipe('n', 3)
        self.swipe('ne', .5)
        self.swipe('nw', 3)
        self.swipe('ne', 3)
        self.swipe('nw', 3)
        self.swipe('ne', 3)
        self.swipe('w', .7)
        self.disableLogs = False

    def goTroughDungeon(self):
        if self.currentDungeon == 3:
            self.goTroughDungeon3()
        elif self.currentDungeon == 6:
            self.goTroughDungeon6()
        elif self.currentDungeon == 10:
            self.goTroughDungeon10()
        elif self.currentDungeon == 16:
            self.goTroughDungeon16()
        else:
            self.goTroughDungeon_old()

    def centerPlayer(self): # still not working correctly always 540px to left.
        px, dir = self.screen_connector.getPlayerDecentering()
        duration = 0.001 * abs(px)- 5
        if px < self.screen_connector.door_width:
            pass
        if dir == 'left':
            self.log("Centered Player <--")
            self.swipe('e', duration)
        elif dir == 'right':
            self.log("Centered Player -->")
            self.swipe('w', duration)
        elif dir == "center":
            pass

    def letPlay(self, _time: int, is_boss = False):
        check_exp_bar = not is_boss
        experience_bar_line = self.screen_connector.getLineExpBar()
        recheck = False
        if self.debug: print("Let-Play. Auto playing...")
        self.log("Searching Dungeon")
        for i in range(_time, 0, -1):
            if i % self.check_seconds == 0 or recheck:
                recheck = False                
                frame = self.screen_connector.getFrame()
                state = self.screen_connector.getFrameState(frame)
                if self.debug: print("Loop Countdown / Kill Timer")
                if self.debug: print(i)
                if self.debug: print("Let Play. Checking screen...")
                if self.debug: print("state: %s" % state)                   
                if state == "in_game":
                    # added movement to increase kill enemy efficency for 10 level chapters
                    if self.currentDungeon == 7 or self.currentDungeon == 14:
                        if self.debug: print("Avoiding Boss")
                        self.log("Avoiding Boss")
                        self.disableLogs = True
                        if self.deadcheck:
                            if self.currentLevel > 5:
                                self.checkIfDead()
                                self.swipe('sw', 1.5)
                                self.checkIfDead()
                                self.swipe('se', 1)
                                self.checkIfDead()
                                self.swipe('e', 0.6)
                                self.swipe('n', 0.5)
                                self.checkIfDead()
                                self.swipe('ne', 1.2)
                                self.checkIfDead()
                                self.swipe('w', 0.4)
                                self.swipe('ne', 1)
                                self.checkIfDead()
                                self.swipe('w', 0.7)
                                self.checkIfDead()
                            else:
                                self.wait(1)
                                self.swipe('sw', 1.5)
                                self.wait(1)
                                self.swipe('se', 1)
                                self.wait(1)
                                self.swipe('e', 0.6)
                                self.swipe('n', 0.5)
                                self.wait(1)
                                self.swipe('ne', 1.2)
                                self.wait(1)
                                self.swipe('w', 0.4)
                                self.swipe('ne', 1)
                                self.wait(1)
                                self.swipe('w', 0.7)
                                self.wait(1)  
                        else:
                            self.wait(1)
                            self.swipe('sw', 1.5)
                            self.wait(1)
                            self.swipe('se', 1)
                            self.wait(1)
                            self.swipe('e', 0.6)
                            self.swipe('n', 0.5)
                            self.wait(1)
                            self.swipe('ne', 1.2)
                            self.wait(1)
                            self.swipe('w', 0.4)
                            self.swipe('ne', 1)
                            self.wait(1)
                            self.swipe('w', 0.7)
                            self.wait(1)
                        self.disableLogs = False
                    # added movement to increase kill enemy efficency for 20 level chapters
                    elif self.currentDungeon == 3 or self.currentDungeon == 6 or self.currentDungeon == 10 or self.currentDungeon == 16:
                        if self.debug: print("Doing patrol")
                        self.log("Doing Patrol")
                        self.disableLogs = True
                        if self.deadcheck:
                            if self.currentLevel > 10:
                                self.checkIfDead()
                                self.swipe('w', 0.35)
                                self.checkIfDead()
                                self.swipe('e', 0.7)
                                self.checkIfDead()
                                self.swipe('w', 0.7)
                                self.checkIfDead()
                                self.swipe('e', 0.7)
                                self.checkIfDead()
                                self.swipe('w', 0.35)
                                self.checkIfDead()
                            else:
                                self.wait(2)
                                self.swipe('w', 0.35)
                                self.wait(2)
                                self.swipe('e', 0.7)
                                self.wait(2)
                                self.swipe('w', 0.7)
                                self.wait(2)
                                self.swipe('e', 0.7)
                                self.wait(2)
                                self.swipe('w', 0.35)
                        else:
                            self.wait(2)
                            self.swipe('w', 0.35)
                            self.wait(2)
                            self.swipe('e', 0.7)
                            self.wait(2)
                            self.swipe('w', 0.7)
                            self.wait(2)
                            self.swipe('e', 0.7)
                            self.wait(2)
                            self.swipe('w', 0.35)
                        self.disableLogs = False
                    # added random escape methods for 30, 50 level chapters
                    else:
                        if i > _time * .8:
                                if self.debug: print("Let-Play. Time < 100%")
                                self.log("Escape route #1")
                                self.disableLogs = True
                                self.swipe('s', 0.6)
                                self.swipe('w', 0.4)
                                self.swipe('nw', 2)
                                self.swipe('ne', 3)
                                self.swipe('s', 0.6)
                                self.swipe('e', 0.4)
                                self.swipe('ne', 2)
                                self.swipe('nw', 3)
                                self.disableLogs = False
                        if _time * .6 < i <= _time * .8:
                                if self.debug: print("Let-Play. Time < 80%")
                                self.log("Escape route #2")
                                self.disableLogs = True
                                self.swipe('s', .5)
                                self.swipe('sw', 2)
                                self.swipe('n', 1)
                                self.swipe('nw', 2)
                                self.swipe('ne', 2)
                                self.swipe('s', .5)
                                self.swipe('se', 2)
                                self.swipe('n', 1)
                                self.swipe('ne', 2)
                                self.swipe('nw', 2)
                                self.disableLogs = False
                        if _time * .4 < i <= _time * .6:
                                if self.debug: print("Let-Play. Time < 60%")
                                self.log("Escape route #3")
                                self.disableLogs = True
                                self.swipe('s', .3)
                                self.swipe('ne', 1)
                                self.swipe('nw', 2)
                                self.swipe('s', .3)
                                self.swipe('nw', 1)
                                self.swipe('ne', 2)
                                self.disableLogs = False
                        if _time * .2 < i <= _time * .4:
                                if self.debug: print("Let-Play. Time < 40%")
                                self.log("Escape route #4")
                                self.disableLogs = True
                                self.swipe('sw', 2)
                                self.swipe('n', 1)
                                self.swipe('ne', 2)
                                self.swipe('se', 2)
                                self.swipe('w', 1)
                                self.swipe('nw', 2)
                                self.swipe('ne', 2)
                                self.disableLogs = False
                        if i <= _time * .2:
                                if self.debug: print("Let-Play. Time < 20%")
                                self.log("Escape route #4")
                                self.disableLogs = True
                                self.swipe('se', 2)
                                self.swipe('n', 1)
                                self.swipe('nw', 2)
                                self.swipe('sw', 2)
                                self.swipe('n', 2)
                                self.swipe('ne', 2)
                                self.swipe('nw', 2)
                                self.disableLogs = False
                    if self.debug: print("Start. Exp & Door Checks")
                    if check_exp_bar and self.screen_connector.checkExpBarHasChanged(experience_bar_line, frame):
                        if self.debug: print("Level ended. Experience gained!")
                        self.log("Gained Experience")
                        return
                    elif self.screen_connector.checkDoorsOpen(frame):
                        if self.debug: print("Door is OPEN #1 <---------######")
                        self.log("Door 1 is Open")
                        return
                    elif self.screen_connector.checkDoorsOpen1(frame):
                        if self.debug: print("Door is OPEN #2 <---------######")
                        self.log("Door 2 is Open")
                        return
                    elif self.screen_connector.checkDoorsOpen2(frame):
                        if self.debug: print("Door is OPEN #3 <---------######")
                        self.log("Door 3 is Open")
                        return
                    else:
                        if self.debug: print("Still playing but level not ended")
                    if self.debug: print("End. Exp & Door Checks")
                else:
                    if self.debug: print("State Checks Start")                    
                    if state == "endgame" or state == "repeat_endgame_question":
                        if self.debug: print("React-Popup. Endgame Detected")
                        if state == "repeat_endgame_question":
                            print("Letplay state: %s" % state)
                            if self.deadcheck or self.battle_pass_advanced:
                                self.pressIfDead()
                            else:
                                print("Turn on 'DeadCheck' to use gems to revive!")
                                self.wait(3)
                                print("Sorry, you most likely died.")
                                self.altEndgameClose()
                        else:
                            print("Sorry, you most likely died.")
                            self.altEndgameClose()
                    elif state == "ability_refresh":
                        if self.debug: print("Cancel Abilty Refresh")
                        self.tap('close_ability_refresh')
                        self.wait(1)
                    elif state == "menu_home" or state == "menu_talents" or state == "menu_events" or state == "menu_equip" or state == "menu_shop":
                        raise Exception('mainscreen')
                    elif state == "crash_desktop_open":
                        raise Exception('crashdesktop')
                    elif state == "select_ability":
                        if self.debug: print("Level ended. New Abilities.")
                        self.log("New Abilities")
                        return
                    elif state == "fortune_wheel" :
                        if self.debug: print("Level ended. Fortune Wheel.")
                        self.log("Fortune Wheel")
                        return
                    elif state == "devil_question":
                        if self.debug: print("Level ended. Devil Arrived.")
                        self.log("Devil Arrived")
                        return
                    elif state == "mistery_vendor":
                        if self.debug: print("Level ended. Mystery Vendor.")
                        self.log("Mystery Vendor")
                        return
                    elif state == "ad_ask":
                        if self.debug: print("Level ended. Ad Ask.")
                        self.log("Ad Ask")
                        return
                    elif state == "angel_heal":
                        if self.debug: print("Level ended. Angel Appeared.")
                        self.log("Angel Arrived")
                        return
                    elif state == "unknown":
                        if self.debug: print("Unknown screen situation detected. Checking again...")
                        if self.screen_connector.getFrameState() == "unknown":
                            self.wait(8) # wait before double check
                            if self.debug: print("Unknown screen situation detected. Checking again x2...")
                            if self.screen_connector.getFrameState() == "unknown":
                                raise Exception('unknown_screen_state')
                            else:
                                recheck = True
                                continue
                        else:
                            recheck = True
                            continue
                    if self.debug: print("State Checks End") 

    def reactGamePopups(self) -> int:
        state = ""
        i = 0
        while state != "in_game":
            if self.stopRequested:
                exit()
            self.wait(1)
            state = self.screen_connector.getFrameState()
            if self.debug: print("state: %s" % state)
            if self.debug: print("React-Popups. Checking screen...")
            if state == "endgame" or state == "repeat_endgame_question":
                if self.debug: print("React-Popup. Endgame Detected")
                if state == "repeat_endgame_question":
                    print("Popups state: %s" % state)
                    if self.deadcheck or self.battle_pass_advanced: 
                        self.pressIfDead()
                    else:
                        print("Turn on 'DeadCheck' to use gems to revive!")
                        self.wait(3)
                        print("Sorry, you most likely died.")
                        self.altEndgameClose()
                else:
                    print("You most likely won out of cycle.")
                    self.altEndgameClose()
            elif state == "ability_refresh":
                if self.debug: print("Cancel Abilty Refresh")
                self.tap('close_ability_refresh')
                self.wait(1)
            elif state == "select_ability":
                self.chooseBestAbility()
            elif state == "fortune_wheel":
                self.tap('wheel_start')
                self.wait(6)
            elif state == "devil_question":
                self.tap('daemon_reject')
                self.wait(2)
            elif state == "ad_ask":
                if self.battle_pass_advanced:
                    self.tap('wheel_start')
                    self.wait(6)
                else:
                    self.tap('wheel_back')
                    self.wait(2)
            elif state == "mistery_vendor":
                if self.battle_pass_advanced:
                    if self.debug: print("Checking for Mystery Vendor Ad")
                    if self.screen_connector.checkFrame("mystery_vendor_ad"):
                        if self.debug: print("Collecting Free Stuff")
                        self.tap('wheel_start')
                        self.wait(6)
                        self.tap('wheel_back')
                        self.wait(2)
                    else:
                        self.tap('wheel_back')
                        self.wait(2)
                else:
                    self.tap('wheel_back')
                    self.wait(2)
            elif state == "special_gift_respin":
                if self.battle_pass_advanced:
                    self.tap('wheel_start')
                    self.wait(6)
                else:
                    self.tap('wheel_back')
                    self.wait(2)
            elif state == "angel_heal":
                if self.healingStrategy == HealingStrategy.SmartHeal:
                    if self.debug: print("Popups. SmartHeal")
                    self.tap('heal_right' if self.smartHealChoice else 'heal_left')
                else:
                    if self.debug: print("Popups. NormalHeal")
                    self.tap('heal_right' if self.healingStrategy == HealingStrategy.AlwaysHeal else 'heal_left')
                self.wait(2)
            elif state == "on_pause":
                self.tap('resume')
                self.wait(2)
            elif state == "time_prize":
                self.tap("collect_time_prize")
                self.wait(5)
                self.tap("resume")
                self.wait(2)
            elif state == "menu_home" or state == "menu_talents" or state == "menu_events" or state == "menu_equip" or state == "menu_shop":
                raise Exception('mainscreen')
            elif state == "crash_desktop_open":
                raise Exception('crashdesktop')
            if i > self.max_loops_popup:
                print("React-Popups. Max loops reached")
                raise Exception('unknown_screen_state')
            i += 1
        return i

    def chooseBestAbility(self):
        abilities = self.screen_connector.getAbilityType()
        try:
            t1 = self.tier_list_abilities[abilities['l']]
            t2 = self.tier_list_abilities[abilities['c']]
            t3 = self.tier_list_abilities[abilities['r']]
            best = ""
            if t1 <= t2 and t1 <= t3:
                to_press = 'ability_left'
                best = abilities['l']
            elif t2 <= t1 and t2 <= t3:
                to_press = 'ability_center'
                best = abilities['c']
            elif t3 <= t2 and t3 <= t1:
                to_press = 'ability_right'
                best = abilities['r']
            if self.debug: print("Found best ability as " + best)
            self.log("Choosing '{}'".format(best))
            self.disableLogs = True
            self.tap(to_press)
            self.disableLogs = False
            self.wait(1) # wait for ability apply
        except Exception as e:
            print("Exception. Unable to correctly choose best ability.")
            self.log("Choosing 'Left Button'")
            self.disableLogs = True
            self.tap('ability_left')
            self.disableLogs = False
            self.wait(1) # wait for ability apply

    def intro_lvl(self):
        if self.debug: print("Getting Start Items")
        self.wait(10) # inital wait for ability wheel to load
        self.reactGamePopups()
        self.disableLogs = True
        self.swipe('n', 3)
        self.disableLogs = False
        self.reactGamePopups()
        self.swipe('n',0.2)
        self.reactGamePopups()
        self.log("Leaving Start Room")
        self.disableLogs = True
        self.swipe('n', 2)
        self.disableLogs = False
        self.log("Entering Dungeon!")
        self.wait(0.5) # for GUI log to load

    def normal_lvl(self):
        if self.debug: print("normal_lvl")
        self.goTroughDungeon()
        self.letPlay(self.playtime)
        self.reactGamePopups()
        self.exit_dungeon_uncentered()

    def heal_lvl(self):
        if self.debug: print("heal_lvl")
        if self.healingStrategy == HealingStrategy.SmartHeal:
            if self.debug: print("Smart Heal Check")
            if self.screen_connector.checkFrame("smart_heal_hp_check"):
                if self.debug: print("HP GREATER than 50%")
                self.smartHealChoice = False
            else:
                print("HP LESS than 50%")
                self.smartHealChoice = True
        self.log("Cenering Self")
        self.disableLogs = True
        self.swipe('s', 2)
        self.swipe('e', 2)
        self.swipe('w', .9)
        self.disableLogs = False
        self.log("Approaching Healer")
        self.disableLogs = True
        self.swipe('n', 1.5)
        self.disableLogs = False
        self.reactGamePopups()
        self.swipe('n', .65)
        self.reactGamePopups()
        if self.debug: print("Exiting Heal")
        self.log("Leaving Healer")
        self.disableLogs = True
        self.swipe('e', 1)
        self.swipe('nw', 2)
        self.disableLogs = False
        self.log("Left Dungeon")
        self.wait(0.5) # for GUI log to load

    def boss_lvl(self):
        if self.debug: print("boss_lvl")
        self.log("Attacking Boss")
        self.disableLogs = True
        self.swipe('n', 0.2)
        self.swipe('n', 0.7)
        self.swipe('e', 1)
        self.swipe('nw', 2)
        if self.currentDungeon == 16:
            if self.currentLevel == 10:
                self.reactGamePopups()
                self.swipe('nw', 1.5)
                self.swipe('ne', 1.5)
            elif self.currentLevel == 15:
                self.swipe('n', .4)
                self.swipe('w', .4)
        self.swipe('ne', 2)
        self.swipe('nw', 1.25)
        self.disableLogs = False
        self.letPlay(self.playtime, is_boss = True)
        self.reactGamePopups()
        if self.currentDungeon == 7 or self.currentDungeon == 14:
            self.disableLogs = True
            self.swipe('w', 0.7)
            self.swipe('e', 0.8)
            self.swipe('w', 0.6)
            self.disableLogs = False
            self.wait(2) # wait for popups to laod
            self.reactGamePopups()
        self.log("Moving to Door")
        self.disableLogs = True
        self.swipe('s', .5)
        self.swipe('w', .3)
        self.swipe('nw', 2.5)
        self.swipe('e', .4)
        self.swipe('n', 1.5)
        self.swipe('e', .65)
        if self.currentDungeon == 7 or self.currentDungeon == 14:
            self.swipe('s', 0.5)
            self.swipe('e', 0.85)
            self.swipe('ne', 0.75)
            self.swipe('nw', 0.7)
            self.swipe('w', 0.55)
            self.wait(2) # wait for popups to laod
            self.reactGamePopups()
            if self.currentLevel == 5 or self.currentLevel == 6:
                self.swipe('s', 0.3)
                self.swipe('ne', 0.6)
                self.swipe('nw', 0.6)
            if self.currentLevel == 8 or self.currentLevel == 9:
                self.swipe('s', 0.3)
                self.swipe('w', 0.3)
                self.swipe('nw', 0.6)
        self.disableLogs = False
        self.exit_dungeon_uncentered()

    def checkIfDead(self):
        if self.debug: print("Started Dead Check")
        if self.screen_connector.checkFrame("you_died_ad"):
            self.pressIfDead()
        if self.debug: print("Completed Dead Checks")

    def pressIfDead(self):
        if self.battle_pass_advanced:
            self.tap("revive_ad")
            print("You revived with Ad.")
            self.wait(.5)
        else:
            self.tap("revive_gems")
            print("You revived with Gems.")
            self.wait(.5)

    def boss_final(self):
        if self.debug: print("boss_final")
        self.log("Final Boss Appeared")
        self.log("Attacking Final Boss")
        if self.currentDungeon == 3 or self.currentDungeon == 6 or self.currentDungeon == 10:
            self.swipe('w', 2)
            i = 0
            while i < self.max_wait:
                self.wait(self.sleep_btw_screens)
                if self.screen_connector.checkBoss3Died():
                    if self.debug: print("boss dead and door open #3")
                    self.log("Boss Dead #1")
                    break
                if self.screen_connector.checkBoss6Died():
                    if self.debug: print("boss dead and door open #6")
                    self.log("Boss Dead #2")
                    break
                if self.screen_connector.checkBoss10Died():
                    if self.debug: print("boss dead and door open #10")
                    self.log("Boss Dead #3")
                    break
                if self.debug: print(i)
                i += 1
            self.reactGamePopups()
            self.log("No Loot Left")
            if self.debug: print("Exiting the Dungeon Final Boss")
            self.log("Leaving Dungeon")
            self.disableLogs = True
            self.swipe('n', 5)
            self.swipe('ne', 3)
            self.disableLogs = False
            self.log("Left Dungeon!")
        else:
            self.disableLogs = True
            self.swipe('n', 0.2)
            self.swipe('n', 0.7)
            self.swipe('e', 1)
            self.swipe('nw', 1.8)
            self.swipe('ne', 1.8)
            self.swipe('nw', 1)
            i = 1
            while i < self.max_wait:
                self.disableLogs = False
                self.log("Searching Dungeon")
                self.disableLogs = True
                if self.deadcheck:
                    self.checkIfDead()
                    self.swipe('w', 0.5)
                    self.checkIfDead()
                    self.swipe('e', 1)
                    self.checkIfDead()
                    self.swipe('w', 0.5)
                else:
                    self.swipe('w', 0.5)
                    self.swipe('e', 1)
                    self.swipe('w', 0.5)
                    self.wait(self.sleep_btw_screens)
                i += 1
            self.disableLogs = False
            self.reactGamePopups()
            self.log("Moving to Door")
            self.disableLogs = True
            self.swipe('s', .5)
            self.swipe('w', .5)
            self.swipe('nw', 3)
            self.swipe('n', 2)
            self.swipe('e', .85)
            if self.currentDungeon == 7 or self.currentDungeon == 14:
                self.swipe('s', 0.5)
                self.swipe('e', 0.8)
                self.swipe('ne', 0.5)
                self.swipe('nw', 0.8)
                self.reactGamePopups()
            self.disableLogs = False
            self.log("No Loot Left")
            if self.debug: print("Exiting the Dungeon Final Boss")
            self.log("Leaving Dungeon")
            self.disableLogs = True
            self.swipe('e', 1)
            self.swipe('nw', 2.5)
            self.disableLogs = False
            self.log("Left Dungeon!")
        i = 0
        self.wait(8) # wait for endgame loot screen to load
        state = self.screen_connector.getFrameState()
        if state == "in_game":
            print("Exception. Still in_game; let's try to escape")
        elif state == "endgame":
            return            
        else:
            print("state: %s" % state)
        while state == "in_game":
            self.disableLogs = True
            if i == 1:
                print("Trying now; escape plan A!")
                self.log("Escape Plan A!")
                self.swipe('s', .6)
                self.swipe('e', .3)
                self.swipe('ne', 1)
            elif i == 2:
                print("Trying now; escape plan B!")
                self.log("Escape Plan B!")
                self.swipe('s', .6)
                self.swipe('w', .3)
                self.swipe('nw', 1)
            elif i == 3:
                print("Trying now; escape plan C!")
                self.log("Escape Plan C!")
                self.swipe('s', .9)
                self.swipe('e', .9)
                self.swipe('nw', 2)
            elif i == 4:
                print("Trying now; escape plan D!")
                self.log("Escape Plan D!")
                self.swipe('s', .9)
                self.swipe('w', .9)
                self.swipe('ne', 2)
            elif i > 5:
                break
            self.swipe('n', 1.5)
            self.swipe('nw', 1.5)
            self.swipe('ne', 1.5)
            self.wait(2) # wait for room transition to complete
            state = self.screen_connector.getFrameState()
            self.disableLogs = False
            i += 1
                    
    def start_one_game(self):
        i = 0
        while i <= self.max_loops_game:
            if self.vipSub == VIPSub.TrueVIP:
                self.vip_priv_rewards = True
            else:
                self.vip_priv_rewards = False
            if self.bpadvSub == BattlepassAdvSub.TrueBPAdv:
                self.battle_pass_advanced = True
            else:
                self.battle_pass_advanced = False
            if self.reviveIfDead == ReviveIfDead.TrueRevive:
                self.deadcheck = True
            else:
                self.deadcheck = False
            state = self.screen_connector.getFrameState()
            print("Start state: %s" % state)
            if state == "menu_talents" or state == "menu_events":
                print("Changing to World Menu")
                self.tap("menu_world_left")
                self.wait(2)
            elif state == "menu_equip" or state == "menu_shop":
                print("Changing to World Menu")
                self.tap("menu_world_right")
                self.wait(2)
            elif state == "crash_desktop_open":
                print("Opening Game Now")
                self.tap("open_game")
                self.wait(90)
            if self.currentLevel > 0:
                if self.screen_connector.checkFrame('menu_home'):
                    if self.debug: print("Home Menu detected... setting to lvl 0 now.")
                    self.currentLevel = 0 # allows to continue playing if at home_menu
                elif self.currentLevel > self.max_level:
                    self.currentLevel = 1 # allows to start playing 20+ levels
                else:
                    self.stat_lvl_start = self.currentLevel
                self.wait(0.5) # for GUI logs to sync                     
            self.levelChanged.emit(self.currentLevel)
            if self.currentLevel > 0:
                self.checkForAds()
            elif self.currentLevel == 0:
                self.checkForEnergy()
            if self.debug: print("Selected Dungeon is %d" % self.currentDungeon)
            print("New game. Starting from level %d" % self.currentLevel)
            try:
                self.start_date = datetime.now()
                self.screen_connector.stopRequested = False
                if self.currentLevel == 0:
                    if state == 'in_game':
                        self.play_one_game()
                    else:
                        self.chooseCave()                        
                else:
                    self.play_one_game()
            except Exception as exc:
                if exc.args[0] == "mainscreen":
                    print("Exception. Main Menu, restarting game now.")
                    self.log("Preparing to rest game")
                elif exc.args[0] == "crashdesktop":
                    print("Exception. Crash Desktop, restarting game now.")
                    self.log("Preparing to rest game")
                elif exc.args[0] == "altendgame":
                    print("Exception. Alt Endgame, restarting game now.")
                    self.log("Preparing to rest game")
                elif exc.args[0] == "unknown_screen_state":
                    state = self.screen_connector.getFrameState()
                    print("state: %s" % state)
                    print("Exception. Unknown State, trying Something.")
                    self.log("Unknown Screens... halp!")
                    #self.tap('level_up_endgame')
                    self.wait(4) #waiting for magic
                else:
                    print("Exception. Unknown problem: %s" % exc)
                    self.log("Unknown Problem... halp!")
                    self.exitEngine()
            if self.currentDungeon == 3 or self.currentDungeon == 6 or self.currentDungeon == 10 or self.currentDungeon == 16:
                if self.debug: print("*** Saving Statistics - Game Finished ***")
                self.statisctics_manager.saveOneGame(self.start_date, self.stat_lvl_start, self.currentLevel)      
            i += 1
            print(">>>>>>>>>>>>>>> Completed Farming Bot Loop <<<<<<<<<<<<<<<")
            print(i)
        if i > self.max_loops_game:
            print("Max Bot Loops Reached. Farming complete!")
            self.log("Farming complete!")
            self.exitEngine()

    def checkForEnergy(self):
        energy_check = True
        while energy_check:
            self.checkForAds()
            state = self.screen_connector.getFrameState()
            if self.debug: print("state: %s" % state)
            if state == 'menu_home':
                if self.debug: print("Going to next step")
            elif state == 'endgame':
                self.pressCloseEndgame()
            elif state == 'in_game':
                break
            elif state != 'in_game':
                break
            print("Checking for Energy")
            if self.screen_connector.checkFrame("least_5_energy"):    
                energy_check = False
                print("Energy is Good")
            else:
                check_farm = True
                check_energy = True
                if self.battle_pass_advanced:
                    print("BPAdv Free Energy Check")
                    self.log("Free Energy Check")
                    self.disableLogs = True
                    self.tap('open_energy_buy')
                    self.wait(8) # wait for load energy store
                    if self.screen_connector.checkFrame("free_ad_energy"):
                        print("xxxxxxxxxxxxxxxxxxxxx Free Ad Energy xxxxxxxxxxxxxxxxxxxxx")
                        self.tap('get_ad_energy')
                        self.disableLogs = False
                        self.wait(6) # wait for load energy bar
                        check_farm = False
                        check_energy = False
                    else:
                        self.tap('close_energy_buy')
                        self.disableLogs = False
                        self.wait(4) # wait for close buy energy        
                if check_farm:
                    print("Monster Farm Energy Check")
                    self.log("Farm Energy Check")
                    self.disableLogs = True
                    self.tap('farm_open')
                    self.wait(6) # wait for farm open
                    frame = self.screen_connector.getFrame()
                    if self.screen_connector.checkFrame("monster_farm_visit", frame) or self.screen_connector.checkFrame("monster_farm_visit_free", frame):
                        print("xxxxxxxxxxxxxxxxxxx Monster Farm Energy xxxxxxxxxxxxxxxxxx")
                        if self.screen_connector.checkFrame("monster_farm_visit_free", frame):
                            self.tap('farm_visit')
                            self.wait(4) # wait for farm load
                        self.tap('farm_visit')
                        self.wait(4) # wait for farm load
                        self.tap('farm_energy_1')
                        self.wait(2) # wait for energy load
                        self.tap('farm_energy_1')
                        self.wait(2) # wait for energy close
                        self.tap('farm_energy_2')
                        self.wait(2) # wait for energy load
                        self.tap('farm_energy_2')
                        self.wait(2) # wait for energy close
                        self.tap('farm_energy_3')
                        self.wait(2) # wait for energy load
                        self.tap('farm_energy_3')
                        self.wait(2) # wait for energy close
                        self.tap('farm_energy_4')
                        self.wait(2) # wait for energy load
                        self.tap('farm_energy_4')
                        self.wait(2) # wait for energy close
                        i = 1
                        while i < 3:
                            frame = self.screen_connector.getFrame()
                            if self.screen_connector.checkFrame("monster_farm_visit_again", frame):
                                print("xxxxxxxxxxxxxxxx Monster Farm Energy Again xxxxxxxxxxxxxxx")
                                self.tap('farm_visit_again')
                                self.wait(4) # wait for farm load
                                self.tap('farm_energy_1')
                                self.wait(2) # wait for energy load
                                self.tap('farm_energy_1')
                                self.wait(2) # wait for energy close
                                self.tap('farm_energy_2')
                                self.wait(2) # wait for energy load
                                self.tap('farm_energy_2')
                                self.wait(2) # wait for energy close
                                self.tap('farm_energy_3')
                                self.wait(2) # wait for energy load
                                self.tap('farm_energy_3')
                                self.wait(2) # wait for energy close
                                self.tap('farm_energy_4')
                                self.wait(2) # wait for energy load
                                self.tap('farm_energy_4')
                                self.wait(2) # wait for energy close
                            i += 1
                        self.wait(2) # wait for energy close
                        self.tap('farm_back')
                        self.wait(4) # wait for farm back
                        check_energy = False
                    self.tap('farm_back')
                    self.wait(6) # wait for menu_home
                    self.disableLogs = False
                if check_energy:
                    print("Energy Strategy Check")
                    self.log("Energy Strategy Check")
                    if self.energyStrategy == EnergyStrategy.AlwaysBuy:
                        self.buy_energy = True
                        self.max_buy_energy = 1
                    elif self.energyStrategy == EnergyStrategy.AlwaysBuy2:
                        self.buy_energy = True
                        self.max_buy_energy = 2
                    elif self.energyStrategy == EnergyStrategy.AlwaysBuy3:
                        self.buy_energy = True
                        self.max_buy_energy = 3
                    elif self.energyStrategy == EnergyStrategy.AlwaysBuy4:
                        self.buy_energy = True
                        self.max_buy_energy = 4
                    else:
                        self.buy_energy = False
                    state = self.screen_connector.getFrameState()
                    if self.debug: print("state: %s" % state)
                    if self.buy_energy and state == 'menu_home':
                        if self.energy_count <= self.max_buy_energy:
                            self.tap('open_energy_buy')
                            self.wait(8) # wait for load energy store
                            self.tap('buy_more_energy')
                            self.wait(6) # wait for load energy bar
                            print("xxxxxxxxxxxxxxxxxxxxxx Bought Energy xxxxxxxxxxxxxxxxxxxxxx")
                            print(self.energy_count)
                            self.energy_count += 1
                        else:
                            print("Max energy buy reached, waiting for 60 minutes")
                            self.log("No Energy")
                            self.noEnergyLeft.emit()
                            self.wait(3605) # wait for time to gain 5 energy
                    elif state == 'in_game':
                        break
                    else:
                        print("No energy, waiting for 60 minutes")
                        self.log("No Energy")
                        self.noEnergyLeft.emit()
                        self.wait(3605) # wait for time to gain 5 energy   

    def checkForAds(self):
        self.log("Checking conditions")
        self.log("Please wait")
        self.log("Checks are running")
        if self.debug: print("Start-Game. Checking screen...")
        state = self.screen_connector.getFrameState()
        print("Ads state: %s" % state)
        ui_changed = False
        frame = self.screen_connector.getFrame()
        print("Checking for Announcement")
        if self.screen_connector.checkFrame("game_announcement", frame):
            print("Closing Announcement")
            self.tap("close_announcement")
            self.wait(4)
            ui_changed = True
        frame = self.screen_connector.getFrame() if ui_changed else frame
        ui_changed = False
        print("Checking for Legendary_Challenge")
        if self.screen_connector.checkFrame("legendary_challenge", frame):
            print("Okay to new Legendary Challenge")
            self.tap("close_legendary_challenge")
            self.wait(4)
            ui_changed = True
        frame = self.screen_connector.getFrame() if ui_changed else frame
        ui_changed = False
        print("Checking for New_Season")
        if self.screen_connector.checkFrame("popup_new_season", frame):
            print("Okay to New Season. Update BPAdv dropdown in GUI to False")
            self.tap("close_new_season")
            self.battle_pass_advanced = False # only works once manully set dropdown in GUI to False
            self.wait(4)
            ui_changed = True
        frame = self.screen_connector.getFrame() if ui_changed else frame
        ui_changed = False
        print("Checking for patrol_reward")
        if self.screen_connector.checkFrame("popup_home_patrol", frame):
            print("Collecting time patrol")
            self.tap("collect_hero_patrol")
            self.wait(6)
            self.tap("collect_hero_patrol")# click again somewhere to close popup with token things
            ui_changed = True
        frame = self.screen_connector.getFrame() if ui_changed else frame
        ui_changed = False
        print("Checking for patrol_close")
        if self.screen_connector.checkFrame("btn_home_time_reward", frame):
            print("Closing patrol_close")
            self.tap("close_hero_patrol")
            self.wait(4)
            ui_changed = True
        if self.vip_priv_rewards:
            frame = self.screen_connector.getFrame() if ui_changed else frame
            ui_changed = False
            print("Checking for vip_reward_1")
            if self.screen_connector.checkFrame("popup_vip_rewards", frame):
                print("Collecting VIP-Privilege Rewards 1")
                self.log("VIP-Privilege Rewards 1")
                self.tap("collect_vip_rewards")
                self.wait(6)
                self.tap("close_vip_rewards")
                self.wait(4)
                ui_changed = True
            frame = self.screen_connector.getFrame() if ui_changed else frame
            ui_changed = False
            print("Checking for vip_reward_2")
            if self.screen_connector.checkFrame("popup_vip_rewards", frame):
                print("Collecting VIP-Privilege Rewards 2")
                self.log("VIP-Privilege Rewards 2")
                self.tap("collect_vip_rewards")
                self.wait(6)
                self.tap("close_vip_rewards")
                self.wait(4)
                ui_changed = True
        frame = self.screen_connector.getFrame() if ui_changed else frame
        ui_changed = False
        print("Checking for need_this")
        if self.screen_connector.checkFrame("popup_need_this", frame):
            print("Rejecting Must Need Ad 0")
            self.tap("close_need_this")
            self.wait(4)
            ui_changed = True
        frame = self.screen_connector.getFrame() if ui_changed else frame
        ui_changed = False
        print("Checking for need_this_1")
        if self.screen_connector.checkFrame("popup_need_this_1", frame):
            print("Rejecting Must Need Ad 1")
            self.tap("close_need_this")
            self.wait(4)
            ui_changed = True
        frame = self.screen_connector.getFrame() if ui_changed else frame
        ui_changed = False
        print("Checking for need_this_2")
        if self.screen_connector.checkFrame("popup_need_this_2", frame):
            print("Rejecting Must Need Ad 2")
            self.tap("close_need_this_2")
            self.wait(4)
            ui_changed = True
        frame = self.screen_connector.getFrame() if ui_changed else frame
        ui_changed = False
        print("Checking for welcome_back")
        if self.screen_connector.checkFrame("popup_welcome_back", frame):
            print("Rejecting Welcome Back Ad")
            self.tap("close_need_this")
            self.wait(4)
            ui_changed = True
        frame = self.screen_connector.getFrame() if ui_changed else frame
        ui_changed = False
        print("Checking for time_prize")
        if self.screen_connector.checkFrame("time_prize", frame):
            print("Collecting time prize")
            self.tap("collect_time_prize")
            self.wait(5)
            self.tap("resume")
            self.wait(2)
            ui_changed = True
        frame = self.screen_connector.getFrame() if ui_changed else frame
        ui_changed = False
        print("Checking for Contine Game")
        if self.screen_connector.checkFrame("crash_continue_yes", frame):
            print("Resuming Previous Game")
            self.tap("continue_yes")
            self.wait(10)
            ui_changed = True

    def chooseCave(self):
        if self.debug: print("Choosing Cave Start")
        self.log("Main Menu")
        self.tap('start')
        self.wait(6) # wait for no_raid button to load
        if self.debug: print("Checking for raid options")
        if not self.screen_connector.checkFrame("quick_raid_option"):
            if self.debug: print("No Quick Raid Option, win 5 times first")
        else:
            if self.debug: print("Normal raid button detected")
            self.tap('start_no_raid')
        self.play_one_game()

    def play_one_game(self):
        # Get level type (T50, T20, ....)
        lvl_TXX = self.chapters_info[str(self.currentDungeon)]
        # Get levels with DungeonLevelType\\
        levels_type = self.levels_info[lvl_TXX.type]
        max_lvl = MaxLevelFromType(lvl_TXX.type)
        if True:
            if self.debug: print("Runing a {} Level Dungeon".format(max_lvl))
            if self.currentLevel < 0 or self.currentLevel > max_lvl:
                if self.debug: print("level out of range: %d" % self.currentLevel)
                self.exitEngine()                
            self.max_level = max_lvl
            while self.currentLevel <= self.max_level:
                if self.debug: print("***********************************")
                print("Level %d: %s" % (self.currentLevel, str(levels_type[self.currentLevel].name)))
                if self.debug: print("***********************************")
                if levels_type[self.currentLevel] == DungeonLevelType.Intro:
                    self.intro_lvl()
                elif levels_type[self.currentLevel] == DungeonLevelType.Normal:
                    self.normal_lvl()
                elif levels_type[self.currentLevel] == DungeonLevelType.Heal:
                    self.heal_lvl()
                elif levels_type[self.currentLevel] == DungeonLevelType.FinalBoss:
                    self.boss_final()
                elif levels_type[self.currentLevel] == DungeonLevelType.Boss:
                    self.boss_lvl()
                self.changeCurrentLevel(self.currentLevel + 1)
            self._manage_exit_from_endgame()

    def _manage_exit_from_endgame(self):
        if self.debug: print("manage_exit_from_endgame")
        self.wait(8) # wait for endgame loot screen to load
        state = self.screen_connector.getFrameState()
        print("End state: %s" % state)
        if state == 'menu_home':
            print("Exit_Endgame. Home Menu Detected.")
            return
        elif state == 'in_game':
            print("Exit_Endgame. You are still in_game; you most likely got stuck!")
            return
        elif state == 'angel_heal':
            print("Exit_Endgame. Maybe you got stuck; or unexpected screen?")
            self.currentLevel = 2
            self.wait(0.5) # wait for GUI load
            return
        elif state == 'endgame':
            print("Exit_Endgame. You won!")
            self.log("You won, Game over!")
            self.gameWon.emit()
            self.pressCloseEndgame()
        elif state != 'endgame':
            print("Exit_Endgame. Maybe you leveled up; or unexpected screen?")
            self.tap('level_up_endgame') # maybe you leveled up trying to get endgame
            self.wait(8) # wait for endgame loot screen to load
        self.pressCloseEndIfEndedFrame()

    def pressCloseEndIfEndedFrame(self):
        if self.debug: print("pressCoseEndIfEndedFrame Check")
        state = self.screen_connector.getFrameState()
        if self.debug: print("state: %s" % state)
        if state == 'endgame':
            print("Exit_Endgame_2. You Won!")
            self.pressCloseEndgame()

    def pressCloseEndgame(self):
        if self.debug: print("Press_Close_End. Going back to main Menu")
        self.tap('close_end')
        self.currentLevel = 0
        self.wait(8) # wait for go back to main menu

    def altEndgameClose(self):
        state = self.screen_connector.getFrameState()
        print("Alt state: %s" % state)
        self.log("You died or won!")
        self.log("Either way, it's over!")
        self.pressCloseEndgame()
        raise Exception('altendgame')

    def exitEngine(self):
        print ("Game Engine Closed")
        if self.currentDungeon == 3 or self.currentDungeon == 6 or self.currentDungeon == 10 or self.currentDungeon == 16:
            if self.debug: print("*** Saving Statistics - Game Killed ***")
            self.statisctics_manager.saveOneGame(self.start_date, self.stat_lvl_start, self.currentLevel)
        exit(1)
