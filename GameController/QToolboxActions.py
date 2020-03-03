from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QHBoxLayout, QBoxLayout, QVBoxLayout, QPushButton, QFormLayout,QLabel
from PyQt5.QtCore import Qt

class QToolboxActions(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.layoutMainVer = QFormLayout()
        self.infoLbl = QLabel()
        self.actions = []
        self.initUI()

    def initUI(self):
        # self.layoutMainVer.setDirection(QBoxLayout.TopToBottom)
        self.setStyleSheet("background-color: white;")
        button_wait = QPushButton("Wait")
        button_wait.setStyleSheet("background-color: rgb(233, 185, 110);")
        button_wait.setFixedSize(60, 60)
        button_walk = QPushButton("Walk")
        button_walk.setStyleSheet("background-color: rgb(138, 226, 52);")
        button_walk.setFixedSize(60, 60)
        button_tap = QPushButton("Tap")
        button_tap.setStyleSheet("background-color: rgb(173, 127, 168);")
        button_tap.setFixedSize(60, 60)
        self.infoLbl.setText("Actions:")
        self.infoLbl.setStyleSheet("background-color: rgba(0,0,0,0%); color: white")
        self.infoLbl.setAlignment(Qt.AlignCenter)
        self.layoutMainVer.addWidget(self.infoLbl)
        self.layoutMainVer.addWidget(button_wait)
        self.layoutMainVer.addWidget(button_walk)
        self.layoutMainVer.addWidget(button_tap)
        self.layoutMainVer.setVerticalSpacing(10)
        self.layoutMainVer.setHorizontalSpacing(0)
        self.layoutMainVer.setContentsMargins(0, 5, 0, 0)
        self.setLayout(self.layoutMainVer)
