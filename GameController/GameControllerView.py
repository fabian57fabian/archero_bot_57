from PyQt5.QtGui import QResizeEvent

from CaveDungeonEngine import HealingStrategy, EnergyStrategy, VIPSub, BattlepassAdvSub, ReviveIfDead
from GameController.GameControllerModel import GameControllerModel, EngineState
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QPushButton, QScrollArea, QLabel, QFormLayout, QMainWindow, QInputDialog, QGridLayout, QWidget, QSpacerItem, QComboBox
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
        self.currentLevelWidget = QLevelViewer(self.model, 0)
        self.widActions = QToolboxActions(self)
        self.size_info_lbl = QLabel("Screen size:\n1x1")
        self.lblDataFolder = QLabel()
        self.lblConnectionStatus = QLabel()
        self.lblCheckConnectionStatus = QLabel()
        self.lblUpdates = QLabel()
        self.controlWidget = QDungeonController(self, controller, model)
        self.content_wid = QDeskArea(self, controller, model)
        self.infoLabel = QLabel()
        self.cBoxhealStrategy = QComboBox()
        self.cBoxhealStrategy.blockSignals(True)
        self.cBoxhealStrategy.addItems(['Always Power','Always Heal','Smart Heal'])
        self.cBoxhealStrategy.blockSignals(False)
        self.lblInfoHealStrategy = QLabel()
        self.updateHealingStrategyChange(self.model.engine.healingStrategy)
        self.cBoxenergyStrategy = QComboBox()
        self.cBoxenergyStrategy.blockSignals(True)
        self.cBoxenergyStrategy.addItems(['Do Not Buy','Buy 1 Time','Buy 2 Times','Buy 3 Times','Buy 4 Times'])
        self.cBoxenergyStrategy.blockSignals(False)
        self.lblInfoEnergyStrategy = QLabel()
        self.updateEnergyStrategyChange(self.model.engine.energyStrategy)
        self.cBoxvipSub = QComboBox()
        self.cBoxvipSub.blockSignals(True)
        self.cBoxvipSub.addItems(['VIP False','VIP True'])
        self.cBoxvipSub.blockSignals(False)
        self.lblInfoVIPSub = QLabel()
        self.updateVIPSubChange(self.model.engine.vipSub)
        self.cBoxbpadvSub = QComboBox()
        self.cBoxbpadvSub.blockSignals(True)
        self.cBoxbpadvSub.addItems(['BPAdv False','BPAdv True'])
        self.cBoxbpadvSub.blockSignals(False)
        self.lblInfoBattlepassAdvSub = QLabel()
        self.updateBattlepassAdvSubChange(self.model.engine.bpadvSub)
        self.cBoxreviveIfDead = QComboBox()
        self.cBoxreviveIfDead.blockSignals(True)
        self.cBoxreviveIfDead.addItems(['Revive False','Revive True'])
        self.cBoxreviveIfDead.blockSignals(False)
        self.lblInfoReviveIfDead = QLabel()
        self.updateReviveIfDeadChange(self.model.engine.reviveIfDead)
        self.initConnectors()

    def initConnectors(self):
        self.model.engine.gameWon.connect(self.onGameWon)
        self.model.engine.gamePaused.connect(self.onGamePaused)
        self.model.engine.noEnergyLeft.connect(self.onNoEnergyLeft)
        self.model.engineStatechanged.connect(self.onEngineStateChanged)
        self.model.connectionStateChanged.connect(self.onConnectionStateChange)
        self.model.checkConnectionStateChanged.connect(self.onCheckConnectionStateChanged)
        self.model.engine.resolutionChanged.connect(self.onScreenDataChanged)
        self.model.engine.dataFolderChanged.connect(self.onScreenDataChanged)
        self.model.engine.levelChanged.connect(self.onLevelChanged)
        self.model.engine.currentDungeonChanged.connect(self.onCurrentDungeonChanged)
        self.model.engine.healingStrategyChanged.connect(self.updateHealingStrategyChange)
        self.cBoxhealStrategy.currentIndexChanged.connect(self.onChangeHealStrategy)
        self.model.engine.energyStrategyChanged.connect(self.updateEnergyStrategyChange)
        self.cBoxenergyStrategy.currentIndexChanged.connect(self.onChangeEnergyStrategy)
        self.model.engine.vipSubChanged.connect(self.updateVIPSubChange)
        self.cBoxvipSub.currentIndexChanged.connect(self.onChangeVIPSub)
        self.model.engine.bpadvSubChanged.connect(self.updateBattlepassAdvSubChange)
        self.cBoxbpadvSub.currentIndexChanged.connect(self.onChangeBattlepassAdvSub)
        self.model.engine.reviveIfDeadChanged.connect(self.updateReviveIfDeadChange)
        self.cBoxreviveIfDead.currentIndexChanged.connect(self.onChangeReviveIfDead)
        self.model.updatesAvailableEvent.connect(self.on_UpdatesAreAvailable)

    def on_UpdatesAreAvailable(self, mess:str):
        self.lblUpdates.setStyleSheet("background-color: #6e6e6e; color: yellow")
        self.lblUpdates.setText(mess)

    def updateHealingStrategyChange(self, strat: HealingStrategy):
        index = 1 if strat == HealingStrategy.AlwaysHeal else 0
        index = 2 if strat == HealingStrategy.SmartHeal else index
        curr = self.cBoxhealStrategy.currentIndex
        if curr != index:
            self.cBoxhealStrategy.blockSignals(True)
            self.cBoxhealStrategy.setCurrentIndex(index)
            self.cBoxhealStrategy.blockSignals(False)

    def updateEnergyStrategyChange(self, strat1: EnergyStrategy):
        index1 = 1 if strat1 == EnergyStrategy.AlwaysBuy else 0
        index1 = 2 if strat1 == EnergyStrategy.AlwaysBuy2 else index1
        index1 = 3 if strat1 == EnergyStrategy.AlwaysBuy3 else index1
        index1 = 4 if strat1 == EnergyStrategy.AlwaysBuy4 else index1
        curr1 = self.cBoxenergyStrategy.currentIndex
        if curr1 != index1:
            self.cBoxenergyStrategy.blockSignals(True)
            self.cBoxenergyStrategy.setCurrentIndex(index1)
            self.cBoxenergyStrategy.blockSignals(False)

    def updateVIPSubChange(self, strat2: VIPSub):
        index2 = 1 if strat2 == VIPSub.TrueVIP else 0
        curr2 = self.cBoxvipSub.currentIndex
        if curr2 != index2:
            self.cBoxvipSub.blockSignals(True)
            self.cBoxvipSub.setCurrentIndex(index2)
            self.cBoxvipSub.blockSignals(False)

    def updateBattlepassAdvSubChange(self, strat3: BattlepassAdvSub):
        index3 = 1 if strat3 == BattlepassAdvSub.TrueBPAdv else 0
        curr3 = self.cBoxbpadvSub.currentIndex
        if curr3 != index3:
            self.cBoxbpadvSub.blockSignals(True)
            self.cBoxbpadvSub.setCurrentIndex(index3)
            self.cBoxbpadvSub.blockSignals(False)

    def updateReviveIfDeadChange(self, strat4: ReviveIfDead):
        index4 = 1 if strat4 == ReviveIfDead.TrueRevive else 0
        curr4 = self.cBoxreviveIfDead.currentIndex
        if curr4 != index4:
            self.cBoxreviveIfDead.blockSignals(True)
            self.cBoxreviveIfDead.setCurrentIndex(index4)
            self.cBoxreviveIfDead.blockSignals(False)

    def onCurrentDungeonChanged(self, new_dungeon: int):
        self.infoLabel.setText("Current dungeon: {}".format(new_dungeon))

    def onChangeHealStrategy(self, new_index):
        strat = HealingStrategy.AlwaysHeal if new_index == 1 else HealingStrategy.AlwaysPowerUp
        strat = HealingStrategy.SmartHeal if new_index == 2 else strat
        self.model.engine.changeHealStrategy(strat)

    def onChangeEnergyStrategy(self, new_index1):
        strat1 = EnergyStrategy.AlwaysBuy if new_index1 == 1 else EnergyStrategy.AlwaysIgnore
        strat1 = EnergyStrategy.AlwaysBuy2 if new_index1 == 2 else strat1
        strat1 = EnergyStrategy.AlwaysBuy3 if new_index1 == 3 else strat1
        strat1 = EnergyStrategy.AlwaysBuy4 if new_index1 == 4 else strat1
        self.model.engine.changeEnergyStrategy(strat1)

    def onChangeVIPSub(self, new_index2):
        strat2 = VIPSub.TrueVIP if new_index2 == 1 else VIPSub.FalseVIP
        self.model.engine.changeVIPSub(strat2)

    def onChangeBattlepassAdvSub(self, new_index3):
        strat3 = BattlepassAdvSub.TrueBPAdv if new_index3 == 1 else BattlepassAdvSub.FalseBPAdv
        self.model.engine.changeBattlepassAdvSub(strat3)

    def onChangeReviveIfDead(self, new_index4):
        strat4 = ReviveIfDead.TrueRevive if new_index4 == 1 else ReviveIfDead.FalseRevive
        self.model.engine.changeReviveIfDead(strat4)

    def onLevelChanged(self, newLevel):
        self.currentLevelWidget.changeLevel(newLevel)

    def onGameWon(self):
        self.infoLabel.setText("Finished all chapters. Win!")

    def onNoEnergyLeft(self):
        self.infoLabel.setText("No energy left. Waiting until refill to play again.")

    def onGamePaused(self):
        self.infoLabel.setText("Engine paused.")

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
            print(">>>>>>>> ########################## <<<<<<<<")
            print(">>>>>>>>  Remember to Open Archero  <<<<<<<<")
            print(">>>>>>>> ########################## <<<<<<<<")
            print("***************** BOT READY ****************") 
            self.infoLabel.setText("Device found! Engine is ready")
            self.lblConnectionStatus.setText("Connected")
            self.lblConnectionStatus.setStyleSheet("color: white")
        else:
            print(">>>>>>>> ########################## <<<<<<<<")
            print(">>>>>>>> Connect Device or Open NOX <<<<<<<<")
            print(">>>>>>>> ########################## <<<<<<<<")
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
        self.lblInfoEnergyStrategy.setText('Energy Strategy:')
        self.toolbarOptions.addWidget(self.lblInfoEnergyStrategy)
        self.toolbarOptions.addWidget(self.cBoxenergyStrategy)
        self.lblInfoVIPSub.setText('VIP Subscription:')
        self.toolbarOptions.addWidget(self.lblInfoVIPSub)
        self.toolbarOptions.addWidget(self.cBoxvipSub)
        self.lblInfoBattlepassAdvSub.setText('BPAdv Subscription:')
        self.toolbarOptions.addWidget(self.lblInfoBattlepassAdvSub)
        self.toolbarOptions.addWidget(self.cBoxbpadvSub)
        self.lblInfoReviveIfDead.setText('Revive If Dead:')
        self.toolbarOptions.addWidget(self.lblInfoReviveIfDead)
        self.toolbarOptions.addWidget(self.cBoxreviveIfDead)
        self.toolbarOptions.addWidget(self.lblUpdates)
        lay_content.addWidget(self.controlWidget)
        lay_content.addWidget(self.infoLabel)
        self.lblInfoHealStrategy.setStyleSheet("background-color: #6e6e6e; color: white")
        self.cBoxhealStrategy.setStyleSheet("background-color: #6e6e6e; color: white")
        self.lblInfoEnergyStrategy.setStyleSheet("background-color: #6e6e6e; color: white")
        self.cBoxenergyStrategy.setStyleSheet("background-color: #6e6e6e; color: white")
        self.lblInfoVIPSub.setStyleSheet("background-color: #6e6e6e; color: white")
        self.cBoxvipSub.setStyleSheet("background-color: #6e6e6e; color: white")
        self.lblInfoBattlepassAdvSub.setStyleSheet("background-color: #6e6e6e; color: white")
        self.cBoxbpadvSub.setStyleSheet("background-color: #6e6e6e; color: white")
        self.lblInfoReviveIfDead.setStyleSheet("background-color: #6e6e6e; color: white")
        self.cBoxreviveIfDead.setStyleSheet("background-color: #6e6e6e; color: white")
        self.controlWidget.setStyleSheet("background-color: #6e6e6e")
        upd_str = "All updated."
        if self.model.updates_available:
            upd_str = "Updates available!"
        self.lblUpdates.setText(upd_str)
        self.lblUpdates.setStyleSheet("background-color: #6e6e6e; color: white")
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
        self.main_layout.addWidget(self.content_wid, 1, 1)
        self.setStyleSheet("background-color: #6e6e6e")
        main_window.setStyleSheet("background-color: #6e6e6e")
        self.setLayout(self.main_layout)
        main_window.setCentralWidget(self)

        self.onScreenDataChanged()  # To initialize
        self.onConnectionStateChange(self.model.connected())  # To initialize
