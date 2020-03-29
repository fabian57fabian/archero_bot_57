from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QBoxLayout, QVBoxLayout, QPushButton, QWidget, QInputDialog
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from GameController.GameControllerModel import GameControllerModel


class QDungeonSelector(QWidget):
    def __init__(self, parent: QWidget, model: GameControllerModel):
        super(QWidget, self).__init__()
        self.model = model
        self.lblCurrentDungeon = QLabel()
        self.layoutMainHor = QHBoxLayout()
        self.currentChapter = 1
        self.requested_w, self.requested_h = parent.get_toolbar_size()
        self.initUI()

    def initUI(self):
        # Init currentDungeonWidget
        self.lblCurrentDungeon.setText("")
        self.lblCurrentDungeon.setStyleSheet("background-color: white")
        self.lblCurrentDungeon.setAlignment(Qt.AlignCenter)
        self.lblCurrentDungeon.setFixedWidth(self.requested_w - 10)
        self.lblCurrentDungeon.setFixedHeight(self.requested_h - 10)
        self.changeCurrentChapter(1)
        self.lblCurrentDungeon.mousePressEvent = self.onChapterClick
        self.layoutMainHor.addWidget(self.lblCurrentDungeon)
        self.layoutMainHor.setSpacing(0)
        self.layoutMainHor.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layoutMainHor)
        self.SelectionEnabled = False

    def onChapterClick(self, event):
        if self.SelectionEnabled:
            self.askForChapter()

    def askForChapter(self):
        chapters = self.model.getChapters()
        item, ok = QInputDialog.getItem(self, "Select chapter",
                                        "Chapter:", chapters, self.currentChapter - 1, False)
        if ok and item:
            selected_ch = self.model.getChNumberFromString(item)
            if selected_ch != -1:
                self.changeCurrentChapter(selected_ch)

    def changeCurrentChapter(self, ch_number: int):
        self.lblCurrentDungeon.clear()
        pixmap = QtGui.QPixmap(self.model.getChapterImagePath(ch_number))
        pixmap = pixmap.scaled(self.lblCurrentDungeon.width(), self.lblCurrentDungeon.height(), Qt.KeepAspectRatio)
        self.lblCurrentDungeon.setPixmap(pixmap)
        self.currentChapter = ch_number
