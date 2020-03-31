from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QHBoxLayout, QBoxLayout, QVBoxLayout, QPushButton, QWidget, QScrollArea, QLabel, \
    QFormLayout, QGridLayout
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QSize
from PyQt5 import QtWidgets, uic
from QWidgets.QLevelState import QLevelState, PlayState


class QDeskArea(QWidget):
    def __init__(self, parent=QWidget):
        super(QWidget, self).__init__()
        self.scroll = QScrollArea()  # Scroll Area which contains the widgets, set as the centralWidget
        self.widget = QWidget()  # Widget that contains the collection of Vertical Box
        self.box = QHBoxLayout()  # The H Box that contains the V Boxes of  labels and buttons
        self.main_layout = QHBoxLayout()
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        self.setStyleSheet("background-color: rgb(43, 43, 43)")
        self.chapersState = []
        self.initUI()

    def build_add_btn(self):
        button = QPushButton(self)
        button.setFixedSize(26, 26)
        button.setText("+")
        button.setStyleSheet("background-color: white; border-radius: 13px;text-align: center")
        return button

    def initUI(self):
        self.setLayout(self.main_layout)
        self.chapersState = []
        for i, v in enumerate(self.getLevelsNames()):
            color = self.getColorByLevel(v)
            object = QLevelState(i, v, color, parent=self)
            self.chapersState.append(object)
            self.box.addWidget(object)
        self.TestLookGood()
        self.widget.setLayout(self.box)

        # Scroll Area Properties
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)
        self.scroll.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.scroll)
        # self.setSizePolicy(
        #    QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding))
        # self.setCentralWidget(self.scroll)

        # self.setGeometry(600, 100, 1000, 900)

    def TestLookGood(self):
        current = 3
        for i, object in enumerate(self.chapersState):
            if i < current:
                object.SetState(PlayState.Played)
                object.addLog("Navigating...")
                object.addLog("Doing a")
                object.addLog("Clicking x,y")
                object.addLog("Leveled up!")
                object.addLog("Exiting")
            if i == current:
                object.SetState(PlayState.Playing)
                object.addLog("Navigating...")
                object.addLog("Doing a")
                object.addLog("Clicking x,y")
            if i > current:
                object.SetState(PlayState.ToBePlayed)

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

    def getLevelsNames(self):
        intro, normal, heal, boss, level_boss = "intro", "normal", "heal", "boss", "final_boss"
        levels_type = [
            intro,
            normal,
            heal,
            normal,
            heal,
            boss,
            normal,
            heal,
            normal,
            heal,
            boss,
            normal,
            heal,
            normal,
            heal,
            boss,
            normal,
            heal,
            normal,
            heal,
            boss,
        ]
        return levels_type
