from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtWidgets, QtGui, QtCore


class QDarkButton(QPushButton):
    buttonClicked = pyqtSignal()

    def __init__(self):
        QPushButton.__init__(self)
        self.setStyleSheet("background-color: (225,225,225); border-radius: 2px;text-align: center")
        self.pressedColor = 'gray'  # '(52, 52, 52)'
        self.changeSheetFunction = self.setStyleSheet
        self.isEnabledFunction = self.isEnabled
        self.size = 50
        self.changeSize(self.size)
        self.clicked.connect(self.button_clicked)

    def changeEnableState(self, active):
        self.setEnabled(active)
        if active:
            self.changeSheetFunction("background-color: (225,225,225); border-radius: 2px;text-align: center")
        else:
            self.changeSheetFunction(
                "background-color: {}; border-radius: 2px;text-align: center".format(self.pressedColor))

    def changeSize(self, size: int):
        self.size = size
        self.setFixedWidth(self.size)
        self.setFixedHeight(self.size)

    def setIconPath(self, path: str):
        self.setIcon(QtGui.QIcon(path))

    def enterEvent(self, event):
        if self.isEnabledFunction():
            self.changeSheetFunction("background-color: gray; border-radius: 2px;text-align: center")

    def leaveEvent(self, event):
        if self.isEnabledFunction():
            self.changeSheetFunction("background-color: (225,225,225); border-radius: 2px;text-align: center")

    @QtCore.pyqtSlot()
    def button_clicked(self):
        self.changeSheetFunction(
            "background-color: {}; border-radius: 2px;text-align: center".format(self.pressedColor))
        self.buttonClicked.emit()
