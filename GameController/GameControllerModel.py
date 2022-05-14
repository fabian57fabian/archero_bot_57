import os
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSignal, QObject, QThread
from CaveDungeonEngine import CaveEngine
import time
from UsbConnector import UsbConnector
from WorkerThread import WorkerThread
from update_manager import UpdatesManager
import enum

class EngineState(enum.Enum):
    Ready = 1
    Playing = 2
    StopInvoked = 3

class GameControllerModel(QObject):
    engineStatechanged = pyqtSignal(EngineState)
    connectionStateChanged = pyqtSignal(bool)
    checkConnectionStateChanged = pyqtSignal(bool)
    resolutionChanged = pyqtSignal(str)
    dataFolderChanged = pyqtSignal(str)
    updatesAvailableEvent = pyqtSignal(str)

    def __init__(self):
        super(QObject, self).__init__()
        # Default data
        self.updates_available = False
        self.debug = True # set False to stop print debug messages in console
        self.engine = CaveEngine()
        self.engine.device_connector.setFunctionToCallOnConnectionStateChanged(self.onDevConnChanged)
        self.engine.device_connector.setFunctionToCallOnCheckingConnectionStateChanged(self.onDevCheckConnectionChanged)
        self.dict_buttons = 'data.py'
        self.ch_images_path = "ui_chapters/"
        self.ch_image_ext = ".png"
        self.icon_path = "icons"
        self.icons_dataset = self.load_icons()
        self.currentEngineState: EngineState = EngineState.Ready
        self.workerThread: WorkerThread = None
        self.updates_man = UpdatesManager()

    def connected(self):
        return self.engine.device_connector.connected

    def onDevConnChanged(self, connected):
        self.connectionStateChanged.emit(connected)

    def onDevCheckConnectionChanged(self, state):
        self.checkConnectionStateChanged.emit(state)

    def _changeConnectedstate(self, conn: bool):
        self.connectionStateChanged.emit(conn)

    def load_data(self):
        pass

    def check_for_updates(self):
        to_update = self.updates_man.ask_for_updates()
        if to_update:
            self.updates_available = True
            self.updatesAvailableEvent.emit("New updates available!")

    def getLevelsNames(self):
        return self.engine.levels_type

    def load_icons(self):
        icons_dts = {}
        icons_dts['prev'] = "Start.png"
        icons_dts['play'] = "Play.png"
        icons_dts['pause'] = "Pause.png"
        icons_dts['next'] = "End.png"
        icons_dts['stop'] = "Stop.png"
        return icons_dts

    def getChapters(self) -> list:
        return self.chapters

    def getChapterImagePath(self, ch_number: int) -> str:
        path = os.path.join(self.ch_images_path, "ch" + str(ch_number) + self.ch_image_ext)
        if not os.path.exists(path):
            if self.debug: print("Unavailable Dungeon image {}".format(ch_number))
            path = os.path.join(self.ch_images_path, "ch_ERR" + self.ch_image_ext)
        return path

    def changeChapterToPlay(self, new_chapter):
        self.engine.changeChapter(new_chapter)

    def getChNumberFromString(self, ch_str) -> int:
        for i, ch in enumerate(self.chapters):
            if ch == ch_str:
                return i + 1
        return -1

    def getIconPath(self, icon_name):
        if icon_name in self.icons_dataset.keys():
            path = os.path.join(self.icon_path, self.icons_dataset[icon_name])
        else:
            path = os.path.join(self.icon_path, "Error-Delete-Icon.png")
        return path
        
    def setEngineState(self, state: EngineState):
        self.currentEngineState = state
        self.engineStatechanged.emit(state)

    def requestClose(self):
        if self.debug: print("GUI close button selected")
        self.engine.device_connector.stopConnectionCheck()
        if self.currentEngineState == EngineState.Playing:
            if self.debug: print("Stopping engine before closing")
            self._stopEngineUnsafe()
        if self.debug: print("Closing game")
        self.workerThread = None
        self.engine = None
        if self.debug: print("Game closed")        

    def _stopEngineUnsafe(self):
        try:
            if self.debug: print("GameControllerModel Restarting engine!")
            self.engine.setStopRequested()
            self.waitForEngineEnd()
            self.engine.setStartRequested()
            self.workerThread = None
        except Exception as e:
            if self.debug: print("Trying to kill process resulted in: %s" % str(e))

    def waitForEngineEnd(self):
        if self.workerThread is not None:
            if self.debug: print("Waiting for thread to finish")
            self.workerThread.join()
            if self.debug: print("Thread ended")
        else:
            if self.debug: print("No active threads")

    def playDungeon(self):
        if self.debug: print("GUI play button selected")
        if self.workerThread is not None:
            if self.debug: print("Another thread is already running")
            self.stopDungeon()
        else:
            self.workerThread = WorkerThread()
            self.setEngineState(EngineState.Playing)
            self.workerThread.function = self.engine.start_infinite_play
            self.workerThread.start()
            if self.debug: print("Thread started")
            
    def pauseDungeon(self):
        if self.debug: print("GUI pause button selected")
        self._stopEngineUnsafe()
        if self.debug: print("Pause action completed")
    
    def stopDungeon(self):
            if self.debug: print("GUI stop button selected")
            self.pauseDungeon()
            self.setEngineState(EngineState.StopInvoked)
            self.setEngineState(EngineState.Ready)
            self.engine.changeCurrentLevel(0)
            if self.debug: print("Stop action completed")
