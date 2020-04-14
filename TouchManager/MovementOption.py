from functools import partial

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QHBoxLayout, QBoxLayout, QVBoxLayout, QPushButton, QWidget, QScrollArea, QLabel, \
    QFormLayout, QGridLayout, QRadioButton
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QSize, pyqtSignal, QObject
from PyQt5 import QtWidgets, uic
from QMyWidgets.QLevelState import QLevelState, PlayState
from TouchManager.TouchManagerController import TouchManagerController
from TouchManager.TouchManagerModel import TouchManagerModel


class MovementOption(QWidget):
    def __init__(self, parent: QObject, controller: TouchManagerController, model: TouchManagerModel):
        super(QWidget, self).__init__()
        self.parent = parent
        self.model = model
        self.controller = controller
        self.lay = QVBoxLayout()
        self.lay_h1 = QHBoxLayout()
        self.lblXsrc = QLabel()
        self.lblYsrc = QLabel()
        self.lay_h2 = QHBoxLayout()
        self.lblXdst = QLabel()
        self.lblYdst = QLabel()
        self.rBtnChangeableSrc = QRadioButton()
        self.rBtnChangeableDst = QRadioButton()
        # self.setStyleSheet("background-color: rgb(255,255,255)")
        # TODO: add button or check btn to unlock change
        self.initUI()
        self.initConnectors()

    def initUI(self):
        self.rBtnChangeableSrc.setText("")
        self.rBtnChangeableSrc.setFixedWidth(20)
        self.rBtnChangeableDst.setText("")
        self.rBtnChangeableDst.setFixedWidth(20)
        if self.controller.selectedCoordinateIndex == 0:
            self.rBtnChangeableSrc.setChecked(True)
        else:
            self.rBtnChangeableDst.setChecked(True)
        #self.lay_h1.addWidget(QLabel("Start: "))
        self.lay_h1.addWidget(self.lblXsrc)
        #self.lay_h1.addWidget(self.lblYsrc)
        self.lay_h1.addWidget(self.rBtnChangeableSrc)

        #self.lay_h2.addWidget(QLabel("End  : "))
        self.lay_h2.addWidget(self.lblXdst)
        #self.lay_h2.addWidget(self.lblYdst)
        self.lay_h2.addWidget(self.rBtnChangeableDst)

        self.lay.addLayout(self.lay_h1)
        #self.lay.addWidget(QLabel("to"))
        self.lay.addLayout(self.lay_h2)
        self.setLayout(self.lay)
        self.changeData([[0, 0], [0, 0]])

    def initConnectors(self):
        self.rBtnChangeableSrc.toggled.connect(partial(self.controller.onCoordinateSelected, 0))
        self.rBtnChangeableDst.toggled.connect(partial(self.controller.onCoordinateSelected, 1))

    def changeData(self, new_data):
        w, h = self.controller.current_image_size
        x1,y1 = (new_data[0][0] * w),(new_data[0][1] * h)
        x2,y2 = (new_data[1][0] * w),(new_data[1][1] * h)
        self.lblXsrc.setText("Start: %4d , %4d" % (x1, y1))
        self.lblXdst.setText("Stop: %4d, %4d" % (x2, y2))
        # self.lblXsrc.setText("X: %4d" % (new_data[0][0] * w))
        # self.lblYsrc.setText("Y: %4d" % (new_data[0][1] * h))
        # self.lblXdst.setText("X: %4d" % (new_data[1][0] * w))
        # self.lblYdst.setText("Y: %4d" % (new_data[1][1] * h))
