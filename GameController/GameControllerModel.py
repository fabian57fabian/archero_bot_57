import os
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSignal, QObject, QThread
from CaveDungeonEngine import CaveEngine

import threading


# import _thread
# from threading import Thread


class GameWorker(QObject):
    levelChanged = pyqtSignal(int)
    addLog = pyqtSignal(str)

    def __init__(self, engine, function):
        super().__init__()
        self.function = function
        self.engine = engine
        self.engine.levelChanged.connect(self.onChangeCurrentLevel)
        self.engine.addLog.connect(self.onAddLogArrived)

    def onAddLogArrived(self, l):
        self.addLog.emit(l)

    def onChangeCurrentLevel(self, i):
        self.levelChanged.emit(i)

    @QtCore.pyqtSlot()
    def run(self):
        self.function()


class GameControllerModel(QObject):
    onLevelChanged = pyqtSignal(int)
    onAddLog = pyqtSignal(str)

    # onDictionaryTapsChanged = pyqtSignal(dict)
    # onButtonLocationChanged = pyqtSignal(str)
    # onImageSelected = pyqtSignal()

    def __init__(self):
        super(QObject, self).__init__()
        # Default data
        self.engine = CaveEngine()
        self.currentLevel = 0
        self.dict_buttons = 'data.py'
        self.ch_images_path = "images/"
        self.ch_image_ext = ".png"
        self.icon_path = "icons"
        self.icons_dataset = self.load_icons()
        self.chapters = ["1. Verdant Prairie",
                         "2. Storm Desert",
                         "3. Abandoned Dungeon",
                         "4. Crystal Mines",
                         "5. Lost Castle",
                         "6. Cave of Bones",
                         "7. Barens of Shadow",
                         "8. Silent Expanse",
                         "9. Frozen Pinnacle",
                         "10. Land of Doom",
                         "11. The Capital",
                         "12. Dungeon of Traps",
                         "13. Lava Land",
                         "14. Eskimo Lands"]
        # self.worker = GameWorker(self.engine, self.engine.start_infinite_play)
        self.initConnectors()

    def initConnectors(self):
        self.engine.levelChanged.connect(self.onChangeCurrentLevel)
        self.engine.addLog.connect(self.onAddLogArrived)

    def onChangeCurrentLevel(self, lvl: int):
        self.currentLevel = lvl
        self.onLevelChanged.emit(lvl)

    def onAddLogArrived(self, log: str):
        self.onAddLog.emit(log)

    def load_data(self):
        pass

    def getLevelsNames(self):
        return self.engine.levels_type

    def load_icons(self):
        icons_dts = {}
        icons_dts['play'] = "Play.png"
        icons_dts['pause'] = "Pause.png"
        icons_dts['skip'] = "End.png"
        icons_dts['stop'] = "Stop.png"
        return icons_dts

    def getChapters(self) -> list:
        return self.chapters

    def getChapterImagePath(self, ch_number: int) -> str:
        return os.path.join(self.ch_images_path, "ch" + str(ch_number) + self.ch_image_ext)

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

    def playDungeon(self):
        self.engine.currentLevel = 6  # .changeCurrentLevel(2)
        # self.worker.run()
        thread1 = threading.Thread(target=self.engine.start_infinite_play)  # , args=(100,))
        thread1.start()
        print("DONEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")
        # try:
        #     _thread.start_new_thread(self.engine.start_infinite_play, (0,))
        # except Exception as e:
        #     print("Error: unable to start thread: %s" % str(e))
