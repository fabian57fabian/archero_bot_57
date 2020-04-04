import json
import os
from PyQt5.QtCore import pyqtSignal, QObject
from pure_adb_connector import adb_screen, get_device_id
from Utils import loadJsonData, saveJsonData_oneIndent, saveJsonData_twoIndent, readAllSizesFolders, getCoordFilePath


class TouchManagerModel(QObject):
    onSourceChanged = pyqtSignal(dict)
    onDictionaryTapsChanged = pyqtSignal(dict)
    onDictionaryMovementsChanged = pyqtSignal(dict)
    onDictionaryFrameChecksChanged = pyqtSignal(dict)
    onButtonLocationChanged = pyqtSignal(str)
    onImageSelected = pyqtSignal()
    onImageAdded = pyqtSignal(str)
    onPointAdded = pyqtSignal(str)

    def __init__(self):
        super(QObject, self).__init__()
        self.data_pack = 'datas'
        self.coords_folder = 'coords'
        self.screens_folder = "screens"
        self.currentScreensFolder = "1080x2220"
        self.manage_default_currentScreensPath()

        self.buttons_folder = 'buttons.json'
        self.movements_folder = 'movements.json'
        self.static_coords_folder = 'static_coords.json'

        self.ui_color = "cyan"
        self.ui_lines_color_rgb = (0, 255, 0)
        self.ui_lines_color_rgb_selected = (255, 0, 255)
        self.current_image_size = [0, 0]
        self.currentFiles = {}
        self.currentDict = {}
        self.currentMovements = {}
        self.currentFrameChecks = {}
        self.screensFolders = readAllSizesFolders()

    def buildCoordFilePath(self, dict_name: str) -> str:
        return getCoordFilePath(dict_name, sizePath=self.currentScreensFolder)

    def currentScreensPath(self):
        return os.path.join(self.data_pack, self.currentScreensFolder, self.screens_folder)

    def is_device_connected(self):
        return get_device_id() is not None

    def acquire_screen(self, name):
        filename = name + ".png"
        adb_screen(os.path.join(self.currentScreensPath(), filename))
        self.currentFiles = {k: None for k in self.loadImagesFromSource(self.currentScreensPath())}
        self.onImageAdded.emit(filename)

    def add_point(self, point_name):
        self.currentDict[point_name] = [.5, .5]
        self.onPointAdded.emit(point_name)

    def manage_default_currentScreensPath(self):
        if not os.path.exists(self.currentScreensPath()):
            os.makedirs(self.currentScreensPath())

    def getPositions(self, dict_button):
        return self.currentDict[dict_button].copy() if dict_button in self.currentDict else None

    def changeButtonPosition(self, dict_button, new_location):
        if dict_button in self.currentDict:
            self.currentDict[dict_button] = new_location
            self.onButtonLocationChanged.emit(dict_button)

    def changeMovementPosition(self, dict_button, new_location, index):
        if dict_button in self.currentMovements:
            self.currentMovements[dict_button][0 if index == 0 else 1] = new_location
            self.onButtonLocationChanged.emit(dict_button)

    def changeFrameCheckPosition(self, dict_button, new_location, index):
        if dict_button in self.currentFrameChecks:
            self.currentFrameChecks[dict_button]['coordinates'][index] = new_location
            self.onButtonLocationChanged.emit(dict_button)

    def load_data(self):
        self.loadScreens()
        self.loadScreenCheck()
        self.loadMovements()
        self.load_buttons()

    def loadScreens(self):
        self.currentFiles = {k: None for k in self.loadImagesFromSource(self.currentScreensPath())}
        self.onSourceChanged.emit(self.currentFiles)

    def load_buttons(self):
        self.currentDict = loadJsonData(self.buildCoordFilePath(self.buttons_folder))
        self.onDictionaryTapsChanged.emit(self.currentDict)

    def loadMovements(self):
        self.currentMovements = loadJsonData(self.buildCoordFilePath(self.movements_folder))
        self.onDictionaryMovementsChanged.emit(self.currentMovements)

    def loadScreenCheck(self):
        self.currentFrameChecks = loadJsonData(self.buildCoordFilePath(self.static_coords_folder))
        self.onDictionaryFrameChecksChanged.emit(self.currentFrameChecks)

    def changeScreensFolder(self, new_folder):
        if new_folder in self.screensFolders.keys():
            self.currentScreensFolder = new_folder
            self.load_data()

    def loadImagesFromSource(self, img_path):
        return [file for file in sorted(os.listdir(img_path))]  # if file.endswith(".jpg")]

    def save_data(self):
        self.saveJsonDict_oneIndent(self.buildCoordFilePath(self.buttons_folder), self.currentDict)
        self.saveJsonDict_oneIndent(self.buildCoordFilePath(self.movements_folder), self.currentMovements)
        self._saveStaticCoords(self.buildCoordFilePath(self.static_coords_folder), self.currentFrameChecks)
