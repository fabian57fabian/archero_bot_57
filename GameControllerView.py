from functools import partial

from PyQt5.QtGui import QPainter, QPen, QBrush, QColor

from GameControllerModel import GameControllerModel
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QPushButton, QScrollArea, QLabel, QFormLayout, QMainWindow, \
    QInputDialog
import os
from GameControllerWidgets import QToolboxRun


class GameControllerWindow(QtWidgets.QWidget):

    def __init__(self, model: GameControllerModel):
        super(GameControllerWindow, self).__init__()
        self.model = model
        self.lblCurrentDungeon = QLabel()
        self.widRun = QToolboxRun()
        self.currentChapter = 1
        # self.model.onSourceChanged.connect(self.source_changed)

    def changeCurrentChapter(self, ch_number:int):
        self.lblCurrentDungeon.clear()
        pixmap = QtGui.QPixmap(self.model.getChapterImagePath(ch_number))
        pixmap = pixmap.scaled(self.lblCurrentDungeon.width(), self.lblCurrentDungeon.height(), Qt.KeepAspectRatio)
        self.lblCurrentDungeon.setPixmap(pixmap)
        self.currentChapter = ch_number

    def setupUi(self, main_window: QMainWindow):
        main_window.setObjectName("main_window")
        main_window.resize(800, 600)
        main_window.setMaximumWidth(800)
        main_window.setMaximumHeight(600)
        centralwidget = QtWidgets.QWidget(main_window)
        lay_hor1 = QHBoxLayout()
        lay_vertical = QVBoxLayout()

        # self.cBoxDungeons.setAlignment(Qt.AlignCenter)
        self.lblCurrentDungeon.setText("")
        self.lblCurrentDungeon.setAlignment(Qt.AlignCenter)
        self.lblCurrentDungeon.setFixedWidth(135)
        self.lblCurrentDungeon.setFixedHeight(135)
        self.changeCurrentChapter(1)
        self.lblCurrentDungeon.mousePressEvent = self.onChapterClick
        lay_hor1.addWidget(self.lblCurrentDungeon)

        self.widRun.setFixedHeight(135)
        lay_hor1.addWidget(self.widRun)
        lay_vertical.addLayout(lay_hor1)

        lay_hor2 = QHBoxLayout()
        self.lblInfoMacros = QLabel("macros:")

        centralwidget.setLayout(lay_vertical)
        main_window.setCentralWidget(centralwidget)

    def onChapterClick(self, event):
        self.askForChapter()
        pass

    def askForChapter(self):
        chapters = self.model.getChapters()
        item, ok = QInputDialog.getItem(self, "Select chapter",
                                        "Chapter:", chapters, self.currentChapter-1, False)
        if ok and item:
            selected_ch = self.model.getChNumberFromString(item)
            if selected_ch != -1:
                self.changeCurrentChapter(selected_ch)