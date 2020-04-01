# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'action_tap.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QFrame, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt
import enum


class PlayState(enum.Enum):
    Played = 1
    Playing = 2
    ToBePlayed = 3


class QLevelState(QWidget):
    def __init__(self, level_num: int, level_name: str, color: tuple, parent=QWidget):
        super(QWidget, self).__init__()
        self.level_num = level_num
        self.level_name = level_name
        self.level_color = color
        self.parent = parent
        self.lblNumber = QtWidgets.QLabel(self)
        self.lblName = QtWidgets.QLabel(self)
        self.frame = QFrame()
        self.logs = QtWidgets.QPlainTextEdit()
        self.lay = QVBoxLayout()
        self.lblScreenChecks = QtWidgets.QLabel(self)

        self.color_played = (86, 101, 115)
        self.color_playing = (213, 216, 220)
        self.color_not_played = (33, 47, 61)

        self.fgplayed = (255, 255, 255)
        self.fgplaying = (0, 0, 0)

        self.state = PlayState.ToBePlayed

        self.updateStateColor()
        self.currentLogs = []
        self.screensCount = 0
        # self.last_logs = []
        self.setupUi()

    def changeScreenCount(self, newCount: int):
        self.screensCount = newCount
        if self.screensCount == 0:
            self.lblScreenChecks.setText("")
        else:
            self.lblScreenChecks.setText("Total screens: {}".format(self.screensCount))

    def addLog(self, log: str):
        if log == "screen check":
            self.changeScreenCount(self.screensCount + 1)
        else:
            self.currentLogs.append(log)
            self.logs.appendPlainText(log)

    def reset(self):
        self.SetState(PlayState.ToBePlayed)
        self.logs.clear()
        self.changeScreenCount(0)

    def SetState(self, state: PlayState):
        if state == self.state:
            return
        reset = False
        if self.state in [PlayState.Played, PlayState.Playing] and state in [PlayState.ToBePlayed, PlayState.Playing]:
            reset = True
        self.state = state
        self.updateStateColor()
        if reset:
            # self.last_logs = self.currentLogs.copy()
            self.currentLogs = []
            self.logs.setPlainText("")
            self.changeScreenCount(0)
        # elif state == PlayState.Played and len(self.last_logs) > 0:
        #     for l in self.last_logs:
        #         self.addLog(l)

    def updateStateColor(self):
        bgcolor = (255, 255, 255)
        fgcolor = (0, 0, 0)
        if self.state == PlayState.Played:
            bgcolor = self.color_played
            fgcolor = self.fgplayed
        elif self.state == PlayState.Playing:
            bgcolor = self.color_playing
            fgcolor = self.fgplaying
        elif self.state == PlayState.ToBePlayed:
            bgcolor = self.color_not_played
            fgcolor = self.fgplayed
        self.logs.setStyleSheet("color: rgb({}, {}, {})".format(fgcolor[0], fgcolor[1], fgcolor[2]))
        self.lblScreenChecks.setStyleSheet("color: rgb({}, {}, {})".format(fgcolor[0], fgcolor[1], fgcolor[2]))
        self.setStyleSheet(
            "background-color: rgb({}, {}, {}); border-radius: 5px;".format(bgcolor[0], bgcolor[1], bgcolor[2]))

    def color_from_level(self, level_name: str):
        if level_name not in self.levels_colors:
            return 255, 255, 255
        else:
            return self.levels_colors[level_name]

    def setupUi(self):
        self.frame.setFixedSize(80, 80)
        self.frame.setStyleSheet(
            "background-color: rgb({}, {}, {}); border-radius: 5px;".format(self.level_color[0], self.level_color[1],
                                                                            self.level_color[2]))
        self.frame.setGeometry(0, 0, 0, 0)
        fram_lay = QHBoxLayout()

        self.lay.setAlignment(Qt.AlignTop)
        # self.lay.setAlignment(Qt.AlignVCenter)
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        frame_lay = QVBoxLayout()
        font = QtGui.QFont()
        font.setPointSize(20)
        self.lblNumber.setFont(font)
        self.lblNumber.setText(str(self.level_num))
        self.lblNumber.setAlignment(QtCore.Qt.AlignCenter)
        font_name = QtGui.QFont()
        font_name.setPointSize(15)
        self.lblName.setFont(font_name)
        self.lblName.setText(self.level_name)
        self.lblName.setAlignment(QtCore.Qt.AlignCenter)
        frame_lay.addWidget(self.lblNumber)
        frame_lay.addWidget(self.lblName)
        self.frame.setLayout(frame_lay)
        fram_lay.addWidget(self.frame)
        self.lay.addLayout(fram_lay)
        # self.lblName.setGeometry(QtCore.QRect(25, 5, 50, 15))
        # self.lblName.setFont(font)
        # self.lblName.setAlignment(QtCore.Qt.AlignCenter)
        # self.lblName.setObjectName("lblName")
        # self.lblName.setText("Tap")
        self.logs.setReadOnly(True)
        # self.cBoxDirection.setGeometry(QtCore.QRect(10, 40, 80, 23))
        # self.cBoxDirection.setStyleSheet("background-color: rgb(238, 238, 236);")
        # self.cBoxDirection.setObjectName("cBoxDirection")

        # self.lay.addWidget(self.lblName)
        self.lblScreenChecks.setAlignment(Qt.AlignCenter)
        self.lay.addWidget(self.logs)
        self.lay.addWidget(self.lblScreenChecks)

        self.setLayout(self.lay)
        QtCore.QMetaObject.connectSlotsByName(self)
