from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QHBoxLayout, QBoxLayout, QVBoxLayout, QPushButton, QWidget, QScrollArea, QLabel, \
    QFormLayout, QGridLayout
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QSize, pyqtSignal, QObject
from PyQt5 import QtWidgets, uic
from QMyWidgets.QLevelState import QLevelState, PlayState
from GameController.GameControllerModel import GameControllerModel


class GameControllerController(QObject):
    onChangeEnableStatesButtons = pyqtSignal(dict)

    def __init__(self, model: GameControllerModel):
        super(QObject, self).__init__()
        self.model = model
        # Set intial states
        self.controllerStates = {'play': True, 'pause': False, 'skip': False, 'stop': False}

    def playRequested(self):
        self.controllerStates['play'] = False
        self.controllerStates['pause'] = False
        self.controllerStates['stop'] = False
        self.controllerStates['skip'] = False
        self.onChangeEnableStatesButtons.emit(self.controllerStates)
        self.model.playDungeon()

    def pauseRequested(self):
        self.controllerStates['play'] = False
        self.controllerStates['pause'] = False
        self.controllerStates['stop'] = False
        self.controllerStates['skip'] = False
        self.onChangeEnableStatesButtons.emit(self.controllerStates)

    def skipRequested(self):
        pass

    def stopRequested(self):
        self.controllerStates['play'] = False
        self.controllerStates['pause'] = False
        self.controllerStates['stop'] = False
        self.controllerStates['skip'] = False
        self.onChangeEnableStatesButtons.emit(self.controllerStates)
