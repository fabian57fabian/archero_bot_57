from functools import partial

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QHBoxLayout, QBoxLayout, QVBoxLayout, QPushButton, QWidget, QScrollArea, QLabel, \
    QFormLayout, QGridLayout, QGroupBox
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QSize, pyqtSignal
from PyQt5 import QtWidgets, uic
from QMyWidgets.QLevelState import QLevelState, PlayState
from TouchManager.TouchManagerController import TouchManagerController
from TouchManager.TouchManagerModel import TouchManagerModel
from TouchManager.TouchManagerController import ShowAreaState
from TouchManager.ButtonOption import ButtonOption
from TouchManager.MovementOption import MovementOption
from TouchManager.FrameCheckOption import FrameCheckOption


class ElementOption(QWidget):
    def __init__(self, parent: QWidget, controller: TouchManagerController, model: TouchManagerModel):
        super(QWidget, self).__init__()
        self.model = model
        self.controller = controller
        self.main_lay = QVBoxLayout()
        # self.layItems = QHBoxLayout()
        #self.lblName = QLabel()
        self.wid: QWidget = ButtonOption(self, controller, model)
        #self.descriptionTxt = QtWidgets.QPlainTextEdit()
        # self.elements = {}
        self.currentType: ShowAreaState = ShowAreaState.Buttons
        self.setupUI()
        self.initControllers()
        self.areatypeChanged(self.controller.currentAreaType)

    def reset(self):
        self.lblInfoDesc.clear()
        #self.lblName.setText("")

    def setupUI(self):
        self.main_lay.setAlignment(Qt.AlignTop)
        #self.lblName.setMaximumHeight(20)
        #self.lblName.setAlignment(Qt.AlignTop)
        #self.descriptionTxt.setMaximumHeight(60)
        #self.descriptionTxt.setReadOnly(True)
        self.main_lay.setContentsMargins(0, 0, 0, 0)
        self.setFixedHeight(150)
        # self.layItems.addWidget(self.wid)
        #self.main_lay.addWidget(self.lblName)
        self.main_lay.addWidget(self.wid)
        #self.main_lay.addWidget(self.descriptionTxt)

        self.setLayout(self.main_lay)

    def initControllers(self):
        self.controller.onCurrentShowAreaChanged.connect(self.areatypeChanged)
        self.controller.onElementSelectionChanged.connect(self.onElementChanged)

    def onElementChanged(self, new_item):
        #self.lblName.setText(new_item + ":")
        self.wid.changeData(self.controller.currentCoordinates)

    def areatypeChanged(self, new_type: ShowAreaState):
        self.clearLayout()
        if new_type == ShowAreaState.Buttons:
            self.wid = ButtonOption(self.main_lay, self.controller, self.model)
            self.main_lay.insertWidget(0, self.wid)
        elif new_type == ShowAreaState.Movements:
            self.wid = MovementOption(self.main_lay, self.controller, self.model)
            self.main_lay.insertWidget(0, self.wid)
        elif new_type == ShowAreaState.FrameCheck:
            self.wid = FrameCheckOption(self.main_lay, self.controller, self.model)
            self.main_lay.insertWidget(0, self.wid)

    def clearLayout(self):
        self.wid.setParent(None)
