from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import QCursor
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
        self.lblCurrentDungeon.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.onCurrentChapterChanged(self.model.engine.currentDungeon)
        self.lblCurrentDungeon.mousePressEvent = self.onChapterClick
        self.layoutMainHor.addWidget(self.lblCurrentDungeon)
        self.layoutMainHor.setSpacing(0)
        self.layoutMainHor.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layoutMainHor)

    def initConnectors(self):
        self.model.engine.currentDungeonChanged.connect(self.onCurrentChapterChanged)

    def onChapterClick(self, event):
        ret, new_ch = self.askForChapter()
        if ret:
            self.controller.requestchangeCurrentChapter(new_ch)

    def askForChapter(self):
        chapters = []
        selected_ch = 0
        chapter_index_curr = 0
        chapters_raw = [(k, v.name) for k, v in self.model.engine.chapters_info.items()]
        for ch_num, name in chapters_raw:
            if int(ch_num) in self.model.engine.allowed_chapters:
                ch_view_name = "{}. {}".format(ch_num, name)
                chapters.append(ch_view_name)
                if int(ch_num) == self.model.engine.currentDungeon:
                    selected_ch = ch_view_name
                chapter_index_curr += 1
        dialog = QInputDialog()
        dialog.setStyleSheet("")
        dialog.setComboBoxItems(chapters)
        dialog.setWindowTitle("Select chapter")
        dialog.setLabelText("Chapter:")
        dialog.setTextValue(selected_ch)
        ret = dialog.exec()
        new_ch = -1
        if ret:
            new_ch = int(dialog.textValue().split('.')[0])
        return ret, new_ch

    def onCurrentChapterChanged(self, ch_number: int):
        self.lblCurrentDungeon.clear()
        pixmap = QtGui.QPixmap(self.model.getChapterImagePath(ch_number))
        pixmap = pixmap.scaled(self.lblCurrentDungeon.width(), self.lblCurrentDungeon.height(), Qt.KeepAspectRatio)
        self.lblCurrentDungeon.setPixmap(pixmap)
