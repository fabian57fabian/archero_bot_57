from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QHBoxLayout, QBoxLayout, QVBoxLayout, QPushButton, QWidget
from PyQt5 import QtCore


class QToolboxRun(QWidget):
    def __init__(self, parent=QWidget):
        super(QWidget, self).__init__()
        self.layoutMainHor = QHBoxLayout()
        self.elements = []
        self.requested_size, _ = parent.get_toolbar_size()
        self.initUI()
        # self.setAttribute(QtCore.Qt.WA_StyledBackground, True)

    def add_element(self, name):
        button = QPushButton(name)
        button.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding))
        button.setStyleSheet("background-color: #4e4e4e; color: #fafafa; font-size: 15px; border: 1px solid white")
        self.layoutMainHor.addWidget(button)
        self.elements.append([name, button])

    def initUI(self):
        self.setMinimumSize(1, 30)
        self.setMaximumHeight(self.requested_size)
        for i in range(1):
            self.add_element("6. The cave")
        self.layoutMainHor.setDirection(QBoxLayout.LeftToRight)
        self.setContentsMargins(0, 0, 0, 0)
        self.layoutMainHor.setSpacing(0)
        self.layoutMainHor.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layoutMainHor)
