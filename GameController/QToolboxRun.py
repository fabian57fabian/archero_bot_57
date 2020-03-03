from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QHBoxLayout, QBoxLayout, QVBoxLayout, QPushButton


class QToolboxRun(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.layoutMainHor = QHBoxLayout()
        self.elements = []
        self.initUI()

    def add_element(self, name):
        button = QPushButton(name)
        button.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding))
        button.setStyleSheet("background-color: #4e4e4e; color: #fafafa; font-size: 15px; border: 1px solid white")
        self.layoutMainHor.addWidget(button)
        self.elements.append([name, button])

    def initUI(self):
        self.setMinimumSize(1, 30)
        self.setMaximumHeight(50)
        for i in range(2):
            self.add_element("dungeon")
        self.layoutMainHor.setDirection(QBoxLayout.LeftToRight)
        self.layoutMainHor.setSpacing(0)
        self.layoutMainHor.setContentsMargins(0, 0, 0, 0)
        #layout_intermediate = QVBoxLayout()
        #wid = QtWidgets.QWidget()
        #wid.setLayout(self.layoutMainHor)
        #layout_intermediate.addWidget()
        self.setLayout(self.layoutMainHor)
