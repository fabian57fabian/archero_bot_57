from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QHBoxLayout, QBoxLayout, QVBoxLayout, QPushButton, QWidget, QScrollArea, QLabel, \
    QFormLayout, QGridLayout
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QSize, pyqtSignal, QObject
from PyQt5 import QtWidgets, uic
from TouchManager.TouchManagerModel import TouchManagerModel
import enum
import os


class ShowAreaState(enum.Enum):
    Buttons = 1
    Movements = 2
    FrameCheck = 3


class TouchManagerController(QObject):
    onCurrentShowAreaChanged = pyqtSignal(ShowAreaState)
    onElementSelectionChanged = pyqtSignal(str)
    onImageSelectionChanged = pyqtSignal(str)

    onImagesChanged = pyqtSignal(dict)
    onButtonsChanged = pyqtSignal(dict)

    def __init__(self, model: TouchManagerModel):
        super(QObject, self).__init__()
        self.model = model
        self.dict_selected = ""
        self.image_selected = ""
        self.currentAreaType: ShowAreaState = ShowAreaState.Buttons
        self.initConnectors()

    def initConnectors(self):
        self.model.onDictionaryTapsChanged.connect(self.onDictionaryTapsChanged)
        self.model.onSourceChanged.connect(self.onImagesFilesChanged)

    def onDictionaryTapsChanged(self, newDict):
        self.onButtonsChanged.emit(newDict)
        if len(newDict.keys()) > 0:
            self.elementSelectRequets(list(newDict.keys())[0])
        else:
            self.dict_selected = ""

    def onImagesFilesChanged(self, newDict):
        self.onImagesChanged.emit(newDict)
        if len(newDict.keys()) > 0:
            self.imageSelectRequets(list(newDict.keys())[0])
        else:
            self.image_selected = ""

    def showDifferentElemStateRequested(self, new_state: ShowAreaState):
        self.currentAreaType = new_state
        self.onCurrentShowAreaChanged.emit(new_state)

    # def listElementSelected(self, button_name):
    #     self.dict_selected = button_name
    #     self.button_pos_clicked(button_name)

    def elementSelectRequets(self, btn_name):
        self.dict_selected = btn_name
        self.onElementSelectionChanged.emit(self.dict_selected)

    def imageSelectRequets(self, image_name):
        if image_name in self.model.currentFiles:
            self.image_selected = image_name
            self.onImageSelectionChanged.emit(self.image_selected)

    def requestScreenFolderChange(self, new_folder):
        if new_folder != self.model.currentScreensFolder:
            self.model.changeScreensFolder(new_folder)

    def getCurrentImageLocation(self):
        return os.path.join(self.model.currentScreensPath(), self.image_selected)
