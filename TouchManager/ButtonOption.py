from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QHBoxLayout, QBoxLayout, QVBoxLayout, QPushButton, QWidget, QScrollArea, QLabel, \
    QFormLayout, QGridLayout
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QSize, pyqtSignal, QObject
from PyQt5 import QtWidgets, uic
from QMyWidgets.QLevelState import QLevelState, PlayState
from TouchManager.TouchManagerController import TouchManagerController
from TouchManager.TouchManagerModel import TouchManagerModel


class ButtonOption(QWidget):
    def __init__(self, parent: QObject, controller: TouchManagerController, model: TouchManagerModel):
        super(QWidget, self).__init__()
        self.parent = parent
        self.model = model
        self.controller = controller
        self.lay = QHBoxLayout()
        self.lblX = QLabel()
        self.lblY = QLabel()
        #TODO: add button or check btn to unlock change
        self.initUI()

    def initUI(self):
        # self.setMinimumSize(10, 10)
        self.lay.addWidget(self.lblX)
        self.lay.addWidget(self.lblY)
        self.setLayout(self.lay)
        self.changeData((0, 0))

    def changeData(self, new_data):
        x, y = new_data[0] * self.model.current_image_size[0], new_data[1] * self.model.current_image_size[1]
        self.lblX.setText("X: %4d" % x)
        self.lblY.setText("Y: %4d" % y)
