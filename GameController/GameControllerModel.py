import os
import logging
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox
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
        dev_conn = UsbConnector(connect_now=True)
        logging.trace("Initalizing Device Connector")
        dev_conn.connect()
        self.engine = CaveEngine(dev_conn)
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
            QMessageBox.information(None, "Updates available", "A new update is available.\n Update it from https://github.com/fabian57fabian/archero_bot_57")

    def getLevelsNames(self):
        if str(self.engine.currentDungeon) not in self.engine.chapters_info.keys():
            logging.error("ERROR: current dungeon is not in chapters_info! ")
            return {}
        # Get level type (T50, T20, ....)
        lvl_TXX = self.engine.chapters_info[str(self.engine.currentDungeon)]
        # Get levels with DungeonLevelType
        levels_type = self.engine.levels_info[lvl_TXX.type]
        return levels_type

    def load_icons(self):
        icons_dts = {}
        icons_dts['prev'] = "Start.png"
        icons_dts['play'] = "Play.png"
        icons_dts['pause'] = "Pause.png"
        icons_dts['next'] = "End.png"
        icons_dts['stop'] = "Stop.png"
        return icons_dts

    def getChapterImagePath(self, ch_number: int) -> str:
        path = os.path.join(self.ch_images_path, "ch" + str(ch_number) + self.ch_image_ext)
        if not os.path.exists(path):
            logging.warning("Unavailable Dungeon image {}".format(ch_number))
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
        logging.trace("GUI Button. *** CLOSE ***")
        self.engine.device_connector.stopConnectionCheck()
        if self.currentEngineState == EngineState.Playing:
            logging.debug("Stopping engine before closing")
            self._stopEngineUnsafe()
        logging.debug("Closing game")
        self.workerThread = None
        self.engine = None
        logging.debug("Game closed")

    def _stopEngineUnsafe(self):
        try:
            logging.debug("Restarting game engine!")
            self.engine.setPauseRequested()
            self.waitForEngineEnd()
            self.engine.setStartRequested()
            self.workerThread = None
        except Exception as e:
            logging.error("Trying to kill process resulted in: %s" % str(e))

    def _stopEngineUnsafe2(self):
        try:
            logging.debug("Restarting game engine!")
            self.engine.setStopRequested()
            self.waitForEngineEnd()
            self.engine.setStartRequested()
            self.workerThread = None
        except Exception as e:
            logging.error("Trying to kill process resulted in: %s" % str(e))

    def waitForEngineEnd(self):
        if self.workerThread is not None:
            logging.trace("Waiting on thread")
            self.workerThread.join()
            logging.trace("Old thread ended")
        else:
            logging.debug("No active threads")

    def playDungeon(self):
        logging.trace("GUI Button *** PLAY ***")
        if self.workerThread is not None:
            logging.debug("Another thread is already running")
            self.stopDungeon()
        else:
            self.workerThread = WorkerThread()
            self.setEngineState(EngineState.Playing)
            self.workerThread.function = self.engine.start_infinite_play
            self.workerThread.start()
            logging.debug("New thread started")
            
    def pauseDungeon(self):
        logging.trace("GUI Button *** PAUSE ***")
        self._stopEngineUnsafe()
        logging.debug("Pause action completed")
    
    def stopDungeon(self):
            logging.trace("GUI Button *** STOP ***")
            self._stopEngineUnsafe2()
            self.setEngineState(EngineState.StopInvoked)
            self.setEngineState(EngineState.Ready)
            self.engine.changeCurrentLevel(0)
            logging.debug("Stop action completed")
