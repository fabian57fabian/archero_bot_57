from PyQt5.QtGui import QResizeEvent

from CaveDungeonEngine import HealingStrategy
from GameController.GameControllerModel import GameControllerModel, EngineState
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QPushButton, QScrollArea, QLabel, QFormLayout, QMainWindow, \
    QInputDialog, QGridLayout, QWidget, QSpacerItem, QComboBox
import os
from GameController.QToolboxActions import QToolboxActions
from GameController.QToolboxRun import QToolboxRun
from GameController.QDeskArea import QDeskArea
from GameController.QDungeonControl import QDungeonController
from GameController.GameControllerController import GameControllerController
from GameController.QLevelViewer import QLevelViewer
from GameController.QDungeonSelector import QDungeonSelector


class GameControllerWindow(QWidget):
    def __init__(self, model: GameControllerModel, controller: GameControllerController):
        super(QWidget, self).__init__()
        self.toolbar_w = 80
        self.toolbar_h = 80
        self.model = model
        self.controller = controller
        self.main_layout = QGridLayout()
        self.toolbarOptions = QVBoxLayout()
        self.dungeonSelector = QDungeonSelector(self, controller, model)
        # self.widRun = QToolboxRun(self)
        self.currentLevelWidget = QLevelViewer(self.model, 0)
        self.widActions = QToolboxActions(self)
        self.size_info_lbl = QLabel("Screen size:\n1x1")
        self.lblDataFolder = QLabel()
        self.lblConnectionStatus = QLabel()
        self.lblCheckConnectionStatus = QLabel()
        self.controlWidget = QDungeonController(self, controller, model)
        self.content_wid = QDeskArea(self, controller, model)  # QtWidgets.QWidget()
        self.infoLabel = QLabel()
        self.cBoxhealStrategy = QComboBox()
        self.cBoxhealStrategy.blockSignals(True)
        self.cBoxhealStrategy.addItems(['Always power','Always heal'])
        self.cBoxhealStrategy.blockSignals(False)
        self.lblInfoHealStrategy = QLabel()
        # self.setupUi()
        self.updateHealingStrategyChange(self.model.engine.healingStrategy)
        self.initConnectors()
        # self.model.onSourceChanged.connect(self.source_changed)

    def initConnectors(self):
        self.model.engine.gameWon.connect(self.onGameWon)
        self.model.engine.noEnergyLeft.connect(self.onNoEnergyLeft)
        self.model.engineStatechanged.connect(self.onEngineStateChanged)
        self.model.connectionStateChanged.connect(self.onConnectionStateChange)
        self.model.checkConnectionStateChanged.connect(self.onCheckConnectionStateChanged)
        self.model.engine.resolutionChanged.connect(self.onScreenDataChanged)
        self.model.engine.dataFolderChanged.connect(self.onScreenDataChanged)
        self.model.engine.levelChanged.connect(self.onLevelChanged)
        self.model.engine.healingStrategyChanged.connect(self.updateHealingStrategyChange)
        self.model.engine.currentDungeonChanged.connect(self.onCurrentDungeonChanged)
        self.cBoxhealStrategy.currentIndexChanged.connect(self.onChangeHealStrategy)

    def updateHealingStrategyChange(self, strat: HealingStrategy):
        #['Always power','Always heal']
        index = 1 if strat == HealingStrategy.AlwaysHeal else 0
        curr = self.cBoxhealStrategy.currentIndex
        if curr != index:
            self.cBoxhealStrategy.blockSignals(True)
            self.cBoxhealStrategy.setCurrentIndex(index)
            self.cBoxhealStrategy.blockSignals(False)

    def onCurrentDungeonChanged(self, new_dungeon: int):
        self.infoLabel.setText("Current dungeon: {}".format(new_dungeon))

    def onChangeHealStrategy(self, new_index):
        strat = HealingStrategy.AlwaysHeal if new_index == 1 else HealingStrategy.AlwaysPowerUp
        self.model.engine.changeHealStrategy(strat)

    def onLevelChanged(self, newLevel):
        self.currentLevelWidget.changeLevel(newLevel)

    def onGameWon(self):
        self.infoLabel.setText("Finished 20 chapters. Win!")

    def onNoEnergyLeft(self):
        self.infoLabel.setText("No energy left. Waiting until refill to play again.")

    def onEngineStateChanged(self, state: EngineState):
        if state == EngineState.Playing:
            self.infoLabel.setText("Engine started playing")
        elif state == EngineState.StopInvoked:
            self.infoLabel.setText("Engine stopping. Wait a second....")
        elif state == EngineState.Ready:
            self.infoLabel.setText("Engine is ready")

    def get_toolbar_size(self):
        return self.toolbar_w, self.toolbar_h

    def onConnectionStateChange(self, connected: bool):
        if connected:
            self.infoLabel.setText("Device found! Engine is ready")
            self.lblConnectionStatus.setText("Connected")
            self.lblConnectionStatus.setStyleSheet("color: white")
        else:
            self.infoLabel.setText("Waiting for a device to be connected")
            self.lblConnectionStatus.setText("NO device!")
            self.lblConnectionStatus.setStyleSheet("background-color: red;color:white")

    def onCheckConnectionStateChanged(self, checking: bool):
        self.lblCheckConnectionStatus.setText('connecting..' if checking else '')

    def onScreenDataChanged(self):
        self.size_info_lbl.setText("Device size:\n{}x{}".format(self.model.engine.width, self.model.engine.heigth))
        self.lblDataFolder.setText("{}".format(self.model.engine.currentDataFolder))

    def setupUi(self, main_window: QMainWindow):
        main_window.setObjectName("game_controller_window")
        self.setObjectName("main_window")
        self.resize(450, 620)
        self.setMinimumWidth(620)
        self.setMinimumHeight(450)
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setColumnStretch(0, 0)
        self.main_layout.setRowStretch(0, 0)
        self.main_layout.setColumnStretch(1, 200)
        self.main_layout.setRowStretch(1, 200)
        self.setLayout(self.main_layout)

        self.main_layout.addWidget(self.dungeonSelector, 0, 0)
        lay_content = QVBoxLayout()
        self.toolbarOptions.addWidget(self.size_info_lbl)
        self.toolbarOptions.addWidget(self.lblConnectionStatus)
        self.toolbarOptions.addWidget(self.lblCheckConnectionStatus)

        self.lblInfoHealStrategy.setText('Healing Strategy:')
        self.toolbarOptions.addWidget(self.lblInfoHealStrategy)
        self.toolbarOptions.addWidget(self.cBoxhealStrategy)

        lay_content.addWidget(self.controlWidget)
        lay_content.addWidget(self.infoLabel)
        self.lblInfoHealStrategy.setStyleSheet("background-color: #6e6e6e; color: white")
        self.cBoxhealStrategy.setStyleSheet("background-color: #6e6e6e; color: white")
        self.controlWidget.setStyleSheet("background-color: #6e6e6e")
        self.size_info_lbl.setStyleSheet("background-color: #6e6e6e; color: white")
        self.lblConnectionStatus.setStyleSheet("background-color: #6e6e6e; color: white")
        self.lblCheckConnectionStatus.setStyleSheet("color: white")
        self.lblCheckConnectionStatus.setText('Starting...')
        self.lblDataFolder.setStyleSheet("background-color: #6e6e6e; color: white")
        self.infoLabel.setStyleSheet("background-color: #6e6e6e; color: white")

        self.size_info_lbl.setAlignment(Qt.AlignCenter)
        self.infoLabel.setAlignment(Qt.AlignCenter)
        self.lblConnectionStatus.setAlignment(Qt.AlignCenter)
        self.lblCheckConnectionStatus.setAlignment(Qt.AlignCenter)
        lay_header = QHBoxLayout()
        lay_header.addLayout(lay_content, 20)
        lay_header.addWidget(self.currentLevelWidget, 1)
        self.main_layout.addLayout(lay_header, 0, 1)
        self.widActions.setFixedWidth(self.toolbar_w)
        self.main_layout.addLayout(self.toolbarOptions, 1, 0)
        self.toolbarOptions.setAlignment(Qt.AlignTop)
        self.toolbarOptions.setContentsMargins(5, 5, 5, 0)
        self.toolbarOptions.setSpacing(10)

        self.content_wid.setSizePolicy(
            QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding))
        # self.content_wid.setStyleSheet("background-color: rgb(43, 43, 43)")
        self.main_layout.addWidget(self.content_wid, 1, 1)
        self.setStyleSheet("background-color: #6e6e6e")
        main_window.setStyleSheet("background-color: #6e6e6e")
        self.setLayout(self.main_layout)
        main_window.setCentralWidget(self)

        self.onScreenDataChanged()  # To initialize
        self.onConnectionStateChange(self.model.connected())  # To initialize
        # self.setCentralWidget(centralwidget)
        # centralwidget.setLayout(self.main_layout)
