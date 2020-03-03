from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QHBoxLayout, QBoxLayout, QVBoxLayout, QPushButton, QFormLayout, QLabel,QWidget
from PyQt5.QtCore import Qt


class QToolboxActions(QtWidgets.QWidget):
    def __init__(self, parent=QWidget):
        super().__init__()
        self.layoutMainVer = QFormLayout()
        self.infoLbl = QLabel()
        self.actions = []
        self.buttons_size = parent.toolbar_w
        self.initUI()
        # self.setAttribute(QtCore.Qt.WA_StyledBackground, True)

    def initUI(self):
        w,h=self.buttons_size-10,self.buttons_size-10
        button_wait = QPushButton("Wait")
        button_wait.setStyleSheet("background-color: rgb(233, 185, 110);")
        button_wait.setFixedSize(w, h)
        button_walk = QPushButton("Walk")
        button_walk.setStyleSheet("background-color: rgb(138, 226, 52);")
        button_walk.setFixedSize(w, h)
        button_tap = QPushButton("Tap")
        button_tap.setStyleSheet("background-color: rgb(173, 127, 168);")
        button_tap.setFixedSize(w, h)
        self.infoLbl.setText("Actions:")
        self.infoLbl.setStyleSheet("background-color: rgba(0,0,0,0%); color: white")
        self.infoLbl.setAlignment(Qt.AlignCenter)
        self.layoutMainVer.addWidget(self.infoLbl)
        self.layoutMainVer.addWidget(button_wait)
        self.layoutMainVer.addWidget(button_walk)
        self.layoutMainVer.addWidget(button_tap)
        #self.layoutMainVer.setVerticalSpacing(10)
        #self.layoutMainVer.setHorizontalSpacing(0)
        self.layoutMainVer.setContentsMargins(0, 5, 0, 0)
        self.setLayout(self.layoutMainVer)
