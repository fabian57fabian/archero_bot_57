from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QBoxLayout, QVBoxLayout, QPushButton, QWidget, QInputDialog
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from GameController.GameControllerModel import GameControllerModel
from GameController.GameControllerController import GameControllerController


class QDungeonSelector(QWidget):
    def __init__(self, parent: QWidget, controller: GameControllerController, model: GameControllerModel):
        super(QWidget, self).__init__()
        self.model = model
        self.controller = controller
        # self.setStyleSheet("background-color: white")
        self.lblCurrentDungeon = QLabel()
        self.layoutMainHor = QHBoxLayout()
        self.currentChapter = self.model.chapters[0]
        self.requested_w, self.requested_h = parent.get_toolbar_size()
        self.initUI()
        self.initConnectors()

    def initUI(self):
        # Init currentDungeonWidget
        self.lblCurrentDungeon.setText("")
        self.lblCurrentDungeon.setStyleSheet("background-color: (225,225,225)")
        self.lblCurrentDungeon.setAlignment(Qt.AlignCenter)
        self.lblCurrentDungeon.setFixedWidth(self.requested_w - 10)
        self.lblCurrentDungeon.setFixedHeight(self.requested_h - 10)
        self.onCurrentChapterChanged(self.model.engine.currentDungeon)
        self.lblCurrentDungeon.mousePressEvent = self.onChapterClick
        self.layoutMainHor.addWidget(self.lblCurrentDungeon)
        self.layoutMainHor.setSpacing(0)
        self.layoutMainHor.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layoutMainHor)
        self.SelectionEnabled = False

    def initConnectors(self):
        self.controller.chapterChanged.connect(self.onCurrentChapterChanged)

    def onChapterClick(self, event):
        if self.SelectionEnabled:
            self.askForChapter()

    def getChapterNumber(self, ch_name):
        # ch = self.model.chapters[target_ch]
        splat = ch_name.split('.')
        return int(splat[0])

    def askForChapter(self):
        chapters = []
        selected_ch = 0
        chapter_index_curr = 0
        for ch in self.model.getChapters():
            ch_num = self.getChapterNumber(ch)
            if ch_num in self.model.allowed_chapters:
                chapters.append(ch)
                if ch_num == self.model.engine.currentDungeon:
                    selected_ch = chapter_index_curr
                chapter_index_curr += 1

        item, ok = QInputDialog.getItem(self, "Select chapter", "Chapter:", chapters, selected_ch, False)
        if ok and item:
            new_ch = self.getChapterNumber(item)
            self.controller.requestchangeCurrentChapter(new_ch)

    def onCurrentChapterChanged(self, ch_number: int):
        self.lblCurrentDungeon.clear()
        pixmap = QtGui.QPixmap(self.model.getChapterImagePath(ch_number))
        pixmap = pixmap.scaled(self.lblCurrentDungeon.width(), self.lblCurrentDungeon.height(), Qt.KeepAspectRatio)
        self.lblCurrentDungeon.setPixmap(pixmap)
        self.currentChapter = self.model.chapters[ch_number]
