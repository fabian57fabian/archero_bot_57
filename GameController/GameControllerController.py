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
        self.controllerStates = {'prev': False, 'play': True, 'pause': False, 'next': True, 'stop': False}
        self.model.engine.levelChanged.connect(self.adjustNewLevelUI)

    def adjustNewLevelUI(self, new_level):
        self.controllerStates['prev'] = new_level != 0
        self.controllerStates['next'] = new_level != self.model.engine.MAX_LEVEL
        self.onChangeEnableStatesButtons.emit(self.controllerStates)

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

    def prevRequested(self):
        if self.model.engine.currentLevel > 0:
            self.model.engine.changeCurrentLevel(self.model.engine.currentLevel - 1)

    def nextRequested(self):
        if self.model.engine.currentLevel <= self.model.engine.MAX_LEVEL:
            self.model.engine.changeCurrentLevel(self.model.engine.currentLevel + 1)

    def stopRequested(self):
        self.controllerStates['play'] = False
        self.controllerStates['pause'] = False
        self.controllerStates['stop'] = False
        self.controllerStates['skip'] = False
        self.onChangeEnableStatesButtons.emit(self.controllerStates)
