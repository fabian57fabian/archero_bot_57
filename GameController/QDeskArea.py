from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QHBoxLayout, QBoxLayout, QVBoxLayout, QPushButton, QWidget, QScrollArea, QLabel, \
    QFormLayout, QGridLayout
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QSize
from PyQt5 import QtWidgets, uic
from QMyWidgets.QLevelState import QLevelState, PlayState
from GameController.GameControllerController import GameControllerController
from GameController.GameControllerModel import GameControllerModel


class QDeskArea(QWidget):
    def __init__(self, parent: QWidget, controller: GameControllerController, model: GameControllerModel):
        super(QWidget, self).__init__()
        self.model = model
        self.controller = controller
        self.scroll = QScrollArea()  # Scroll Area which contains the widgets, set as the centralWidget
        self.widget = QWidget()  # Widget that contains the collection of Vertical Box
        self.box = QHBoxLayout()  # The H Box that contains the V Boxes of  labels and buttons
        self.main_layout = QHBoxLayout()
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        self.setStyleSheet("background-color: rgb(43, 43, 43)")
        self.chapersState = []
        self.initUI()
        self.initconnectors()

    def initconnectors(self):
        self.model.onLevelChanged.connect(self.levelChanged)

    def levelChanged(self, new_level):
        for i, levelState in enumerate(self.chapersState):
            if i < new_level:
                levelState.SetState(PlayState.Played)
            elif i == new_level:
                levelState.SetState(PlayState.Playing)
            else:
                levelState.SetState(PlayState.ToBePlayed)

    def build_add_btn(self):
        button = QPushButton(self)
        button.setFixedSize(26, 26)
        button.setText("+")
        button.setStyleSheet("background-color: white; border-radius: 13px;text-align: center")
        return button

    def resetCurrentDungeon(self):
        for levelState in self.chapersState:
            levelState.reset()

    def initUI(self):
        self.setLayout(self.main_layout)
        self.chapersState = []
        for i, v in self.model.getLevelsNames().items():
            color = self.getColorByLevel(v)
            object = QLevelState(i, v, color, parent=self)
            self.chapersState.append(object)
            self.box.addWidget(object)
        # self.insertMockupData()
        self.widget.setLayout(self.box)

        # Scroll Area Properties
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)
        self.scroll.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.scroll)

    def getColorByLevel(self, level_name):
        if level_name == "intro":
            return (247, 181, 41)
        elif level_name == "normal":
            return (23, 107, 239)
        elif level_name == "heal":
            return (23, 156, 82)
        elif level_name == "boss":
            return (255, 62, 48)
        elif level_name == "final_boss":
            return (127, 0, 0)
        else:
            return (255, 255, 255)
