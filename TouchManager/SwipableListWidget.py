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


class SwipableListWidget(QWidget):

    def __init__(self, parent: QWidget, controller: TouchManagerController, model: TouchManagerModel):
        super(QWidget, self).__init__()
        self.model = model
        self.controller = controller
        self.main_layout = QGridLayout()
        self.scroller = QScrollArea()
        self.widget = QWidget()
        self.verticalLayout = QFormLayout()
        self.elementsDict = {}
        self.lastElementSelected = ""
        self.setupUI()
        self.initConnectors()

    def setupUI(self):
        self.setLayout(self.main_layout)
        self.widget.setLayout(self.verticalLayout)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.scroller.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroller.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroller.setWidgetResizable(True)
        self.scroller.setWidget(self.widget)
        self.main_layout.addWidget(self.scroller)


    def initConnectors(self):
        self.controller.onElementSelectionChanged.connect(self.onSelectionChanged)
        self.model.onPointAdded.connect(self.addElement)
        self.model.onDictionaryTapsChanged.connect(self.onDictChanged)

    def addElement(self, button_name):
        button = QtWidgets.QPushButton(button_name)
        button.clicked.connect(partial(self.controller.elementSelectRequets, button_name))

        self.elementsDict[button_name] = button
        self.verticalLayout.addRow(self.elementsDict[button_name])

    def onSelectionChanged(self, btn_name):
        if self.lastElementSelected != "":
            self.elementsDict[self.lastElementSelected].setStyleSheet("QPushButton { background-color : white; }")
        self.elementsDict[btn_name].setStyleSheet("QPushButton { background-color : %s; }" % self.model.ui_color)
        self.lastElementSelected = btn_name

    def onDictChanged(self):
        # self.dataLayout.deleteLater()
        for button_pos in self.model.currentDict.items():
            # button = QtWidgets.QPushButton("%s, %dx%d" %(button_pos[0], button_pos[1][0],button_pos[1][1]))
            self.addElement(button_pos[0])
