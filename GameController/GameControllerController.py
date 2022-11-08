import logging
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QHBoxLayout, QBoxLayout, QVBoxLayout, QPushButton, QWidget, QScrollArea, QLabel, \
    QFormLayout, QGridLayout
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QSize, pyqtSignal, QObject
from PyQt5 import QtWidgets, uic
from GameController.GameControllerModel import GameControllerModel, EngineState

class GameControllerController(QObject):
    onChangeEnableStatesButtons = pyqtSignal(dict)

    def __init__(self, model: GameControllerModel):
        super(QObject, self).__init__()
        self.model = model
        # Set intial states
        self.controllerStates = {'prev': True, 'play': self.model.connected(), 'pause': False, 'next': True,
                                 'stop': False}
        self.model.engine.levelChanged.connect(self.onLevelChanged)
        self.model.connectionStateChanged.connect(self.onConnectionChanged)

    def onConnectionChanged(self, conn):
        if conn and not self.controllerStates['play'] and self.model.currentEngineState != EngineState.Playing:
            self.controllerStates['play'] = True
            self.onChangeEnableStatesButtons.emit(self.controllerStates)
        if not conn and self.controllerStates['play']:
            self.controllerStates['play'] = False
            self.onChangeEnableStatesButtons.emit(self.controllerStates)

    def onLevelChanged(self, new_level):
        if self.controllerStates['play']:
            self.controllerStates['prev'] = new_level != 0
            self.controllerStates['next'] = new_level != self.model.engine.max_level
            self.onChangeEnableStatesButtons.emit(self.controllerStates)

    def playRequested(self):
        self.controllerStates['play'] = False
        self.controllerStates['pause'] = True
        self.controllerStates['stop'] = False
        self.controllerStates['prev'] = False
        self.controllerStates['next'] = False
        self.onChangeEnableStatesButtons.emit(self.controllerStates)
        self.model.playDungeon()

    def pauseRequested(self):
        if self.model.connected():
            self.controllerStates['play'] = True
        self.controllerStates['pause'] = False
        self.controllerStates['stop'] = True
        self.controllerStates['prev'] = False
        self.controllerStates['next'] = False
        self.onChangeEnableStatesButtons.emit(self.controllerStates)
        self.model.pauseDungeon()

    def changeLevelRequested(self, newLevel: int):
        if not self.model.currentEngineState == EngineState.Playing:
            if 0 <= newLevel <= self.model.engine.max_level:
                self.model.engine.changeCurrentLevel(newLevel)
        else:
            pass

    def prevRequested(self):
        if self.model.engine.currentLevel > 0:
            self.changeLevelRequested(self.model.engine.currentLevel - 1)

    def nextRequested(self):
        if self.model.engine.currentLevel <= self.model.engine.max_level:
            self.changeLevelRequested(self.model.engine.currentLevel + 1)

    def stopRequested(self):
        if self.model.connected():
            self.controllerStates['play'] = True
        self.controllerStates['pause'] = False
        self.controllerStates['stop'] = False
        self.controllerStates['prev'] = True
        self.controllerStates['next'] = True
        self.onChangeEnableStatesButtons.emit(self.controllerStates)
        self.model.stopDungeon()

    def requestchangeCurrentChapter(self, new_chapter):
        if new_chapter in self.model.engine.allowed_chapters:
            self.model.changeChapterToPlay(new_chapter)
