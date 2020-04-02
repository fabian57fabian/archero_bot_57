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

    def __init__(self, model: TouchManagerModel):
        super(QObject, self).__init__()
        self.model = model
        self.coordShowerState = ShowAreaState.Buttons

    def showButtonsRequested(self):
        self.onCurrentShowAreaChanged.emit(ShowAreaState.Buttons)

    def showMovementsRequested(self):
        self.onCurrentShowAreaChanged.emit(ShowAreaState.Movements)

    def showCheckpointsrequested(self):
        self.onCurrentShowAreaChanged.emit(ShowAreaState.Checkpoints)
