from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QHBoxLayout, QBoxLayout, QVBoxLayout, QPushButton, QWidget, QScrollArea, QLabel, \
    QFormLayout, QGridLayout
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QSize, pyqtSignal, QObject
from PyQt5 import QtWidgets, uic
from TouchManager.TouchManagerModel import TouchManagerModel
import enum


class ShowAreaState(enum.Enum):
    Buttons = 1
    Movements = 2
    Checkpoints = 3


class TouchManagerController(QObject):
    onCurrentShowAreaChanged = pyqtSignal(ShowAreaState)
    onElementSelectionChanged = pyqtSignal(str)
    onImageSelectionChanged = pyqtSignal(str)

    def __init__(self, model: TouchManagerModel):
        super(QObject, self).__init__()
        self.model = model
        self.dict_selected = ""
        self.image_selected = ""
        self.coordShowerState = ShowAreaState.Buttons
        self.initConnectors()

    def initConnectors(self):
        self.model.onDictionaryTapsChanged.connect(self.onDictionaryTapsChanged)

    def onDictionaryTapsChanged(self):
        self.dict_selected = list(self.model.currentDict.keys())[0]

    def showButtonsRequested(self):
        self.onCurrentShowAreaChanged.emit(ShowAreaState.Buttons)

    def showMovementsRequested(self):
        self.onCurrentShowAreaChanged.emit(ShowAreaState.Movements)

    def showCheckpointsrequested(self):
        self.onCurrentShowAreaChanged.emit(ShowAreaState.Checkpoints)

    # def listElementSelected(self, button_name):
    #     self.dict_selected = button_name
    #     self.button_pos_clicked(button_name)

    def elementSelectRequets(self, btn_name):
        self.dict_selected = btn_name
        self.onElementSelectionChanged.emit(self.dict_selected)

    def imageSelectRequets(self, image_name):
        self.image_selected = image_name
        self.onImageSelectionChanged.emit(self.image_selected)
