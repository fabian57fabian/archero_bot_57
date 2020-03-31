from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QHBoxLayout, QBoxLayout, QVBoxLayout, QPushButton, QFormLayout, QLabel, QWidget
from PyQt5.QtCore import Qt


class QToolboxActions(QWidget):
    def __init__(self, parent=QWidget):
        super(QWidget, self).__init__()
        self.layoutMainVer = QFormLayout()
        self.infoLbl = QLabel()
        self.actions = []
        self.requested_size, _ = parent.get_toolbar_size()
        self.btnTap = QPushButton("Tap")
        self.btnSwipe = QPushButton("Swipe")
        self.btnScreen = QPushButton("Screen")
        self.active = True
        self.initUI()
        # self.setAttribute(QtCore.Qt.WA_StyledBackground, True)

    def setActive(self, active: bool):
        self.active = active
        self.btnTap.setEnabled(active)
        self.btnSwipe.setEnabled(active)
        self.btnScreen.setEnabled(active)

    def initUI(self):
        w, h = self.requested_size - 10, self.requested_size - 10
        self.btnTap.setStyleSheet("background-color: rgb(233, 185, 110);")
        self.btnTap.setFixedSize(w, h)
        self.btnSwipe.setStyleSheet("background-color: rgb(138, 226, 52);")
        self.btnSwipe.setFixedSize(w, h)
        self.btnScreen.setStyleSheet("background-color: rgb(173, 127, 168);")
        self.btnScreen.setFixedSize(w, h)
        self.infoLbl.setText("Quick\nactions:")
        self.infoLbl.setStyleSheet("background-color: rgba(0,0,0,0%); color: white")
        self.infoLbl.setAlignment(Qt.AlignCenter)
        self.layoutMainVer.addWidget(self.infoLbl)
        self.layoutMainVer.addWidget(self.btnTap)
        self.layoutMainVer.addWidget(self.btnSwipe)
        self.layoutMainVer.addWidget(self.btnScreen)
        # self.layoutMainVer.setVerticalSpacing(10)
        # self.layoutMainVer.setHorizontalSpacing(0)
        self.layoutMainVer.setContentsMargins(0, 5, 0, 0)
        self.setLayout(self.layoutMainVer)
