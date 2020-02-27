from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QHBoxLayout, QBoxLayout, QPushButton


class QToolboxRun(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.layoutMainHor = QHBoxLayout()
        self.initUI()

    def initUI(self):
        self.setMinimumSize(1, 30)
        self.setMaximumHeight(50)
        for i in range(5):
            button = QPushButton("dungeon")
            button.setFixedHeight(50)
            button.setFixedWidth(60)
            self.layoutMainHor.addWidget(button)
            button2 = QPushButton("+")
            button2.setFixedHeight(30)
            button2.setFixedWidth(30)
            self.layoutMainHor.addWidget(button2)
        self.layoutMainHor.setDirection(QBoxLayout.LeftToRight)
        self.layoutMainHor.setSpacing(0)
        self.layoutMainHor.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layoutMainHor)