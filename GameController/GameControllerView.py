from PyQt5.QtGui import QResizeEvent

from GameController.GameControllerModel import GameControllerModel, EngineState
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QPushButton, QScrollArea, QLabel, QFormLayout, QMainWindow, \
    QInputDialog, QGridLayout, QWidget, QSpacerItem
import os
from GameController.QToolboxActions import QToolboxActions
from GameController.QToolboxRun import QToolboxRun
from GameController.QDungeonSelector import QDungeonSelector
from GameController.QDeskArea import QDeskArea
from GameController.QDungeonControl import QDungeonController
from GameController.GameControllerController import GameControllerController


class GameControllerWindow(QWidget):
    def __init__(self, model: GameControllerModel, controller: GameControllerController):
        super(QWidget, self).__init__()
        self.toolbar_w = 70
        self.toolbar_h = 70
        self.model = model
        self.main_layout = QGridLayout()
        self.toolbarOptions = QVBoxLayout()
        self.dungeonSelector = QDungeonSelector(self, model)
        # self.widRun = QToolboxRun(self)
        self.widActions = QToolboxActions(self)
        self.lblScreenW = QLabel()
        self.lblScreenH = QLabel()
        self.lblDataFolder = QLabel()
        self.lblConnectionStatus = QLabel()
        self.controlWidget = QDungeonController(self, controller, model)
        self.content_wid = QDeskArea(self, controller, model)  # QtWidgets.QWidget()
        self.infoLabel = QLabel()
        self.setupUi()
        self.initConnectors()
        self.onScreenDataChanged()  # To initialize
        self.onConnectionStateChange(self.model.connected)  # To initialize

        # self.model.onSourceChanged.connect(self.source_changed)

    def initConnectors(self):
        self.model.engineStatechanged.connect(self.onEngineStateChanged)
        self.model.connectionStateChanged.connect(self.onConnectionStateChange)
        self.model.engine.resolutionChanged.connect(self.onScreenDataChanged)
        self.model.engine.dataFolderChanged.connect(self.onScreenDataChanged)

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
            self.lblConnectionStatus.setText("Connected")
            self.lblConnectionStatus.setStyleSheet("color: white")
        else:
            self.lblConnectionStatus.setText("Not connecetd!")
            self.lblConnectionStatus.setStyleSheet("color: red")

    def onScreenDataChanged(self):
        self.lblScreenW.setText("W: {}".format(self.model.engine.width))
        self.lblScreenH.setText("H: {}".format(self.model.engine.heigth))
        self.lblDataFolder.setText("{}".format(self.model.engine.currentDataFolder))

    def setupUi(self):
        self.setObjectName("main_window")
        self.resize(800, 600)
        self.setMinimumWidth(640)
        self.setMinimumHeight(480)
        # self.lblScreenSize.setText("Your screen is:\nwidthxheight")
        # centralwidget = QtWidgets.QWidget(main_window)
        # centralwidget.setStyleSheet("background-color: #6e6e6e")
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        # self.setVerticalSpacing(10)
        # self.setHorizontalSpacing(0)
        self.main_layout.setColumnStretch(0, 0)
        self.main_layout.setRowStretch(0, 0)
        self.main_layout.setColumnStretch(1, 200)
        self.main_layout.setRowStretch(1, 200)
        self.setLayout(self.main_layout)

        self.main_layout.addWidget(self.dungeonSelector, 0, 0)
        lay_content = QVBoxLayout()
        # self.toolbarOptions.addWidget(QLabel("Resolution:"))
        self.toolbarOptions.addWidget(self.lblScreenW)
        self.toolbarOptions.addWidget(self.lblScreenH)
        # self.toolbarOptions.addWidget(QLabel("Data folder:"))
        # self.toolbarOptions.addWidget(self.lblDataFolder)
        # self.toolbarOptions.addWidget(QLabel("Connection:"))
        self.toolbarOptions.addWidget(self.lblConnectionStatus)

        lay_content.addWidget(self.controlWidget)
        lay_content.addWidget(self.infoLabel)
        self.controlWidget.setStyleSheet("background-color: #6e6e6e")
        self.lblScreenW.setStyleSheet("background-color: #6e6e6e; color: white")
        self.lblScreenH.setStyleSheet("background-color: #6e6e6e; color: white")
        self.lblConnectionStatus.setStyleSheet("background-color: #6e6e6e; color: white")
        self.lblDataFolder.setStyleSheet("background-color: #6e6e6e; color: white")
        # self.lblConnectionStatus.setAlignment(Qt.AlignCenter)
        # self.lblConnectionStatus.setAlignment(Qt.AlignRight)
        self.infoLabel.setStyleSheet("background-color: #6e6e6e; color: white")
        self.infoLabel.setAlignment(Qt.AlignCenter)
        self.main_layout.addLayout(lay_content, 0, 1)

        self.widActions.setFixedWidth(self.toolbar_w)
        self.main_layout.addLayout(self.toolbarOptions, 1, 0)
        self.toolbarOptions.setAlignment(Qt.AlignTop)
        self.toolbarOptions.setContentsMargins(5, 5, 0, 0)
        self.toolbarOptions.setSpacing(10)

        self.content_wid.setSizePolicy(
            QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding))
        # self.content_wid.setStyleSheet("background-color: rgb(43, 43, 43)")
        self.main_layout.addWidget(self.content_wid)
        self.setStyleSheet("background-color: #6e6e6e")

        # self.setCentralWidget(centralwidget)
        # centralwidget.setLayout(self.main_layout)
