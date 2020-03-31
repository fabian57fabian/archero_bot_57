from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QHBoxLayout, QBoxLayout, QVBoxLayout, QPushButton, QWidget, QScrollArea, QLabel, \
    QFormLayout, QGridLayout
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QSize, pyqtSignal, QObject
from PyQt5 import QtWidgets, uic
from QMyWidgets.QLevelState import QLevelState, PlayState
from GameController.GameControllerModel import GameControllerModel


class GameControllerController(QObject):
    onChangeEnableStatesButtons = pyqtSignal(list)

    def __init__(self, model: GameControllerModel):
        super(QObject, self).__init__()
        self.model = model

    def playRequested(self):
        self.onChangeEnableStatesButtons.emit([('play', False),('pause', True), ('stop', False)])

    def pauseRequested(self):
        self.onChangeEnableStatesButtons.emit([('pause', False), ('play', True), ('stop', True)])

    def skipRequested(self):
        pass

    def stopRequested(self):
        self.onChangeEnableStatesButtons.emit([('pause', False), ('play', True), ('stop', True)])
