from functools import partial

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QHBoxLayout, QBoxLayout, QVBoxLayout, QPushButton, QWidget, QScrollArea, QLabel, \
    QFormLayout, QGridLayout, QRadioButton, QComboBox, QSpacerItem
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QSize, pyqtSignal, QObject
from PyQt5 import QtWidgets, uic
from QMyWidgets.QLevelState import QLevelState, PlayState
from TouchManager.TouchManagerController import TouchManagerController
from TouchManager.TouchManagerModel import TouchManagerModel


class FrameCheckOption(QWidget):
    def __init__(self, parent: QObject, controller: TouchManagerController, model: TouchManagerModel):
        super(QWidget, self).__init__()
        self.parent = parent
        self.model = model
        self.controller = controller
        self.main_lay = QVBoxLayout()
        self.lay = QVBoxLayout()
        self.lbls = []
        self.lblsColors = []
        self.rBtns = []
        self.aroundLbl = QLabel()
        self.cBoxAround = QComboBox()
        self.initMainUI()
        self.initUI({'coordinates': [[0.5, 0.5]], 'values': [[255, 255, 255]], 'around': 5})
        self.initConnectors()

    def initMainUI(self):
        self.aroundLbl.setText("Around factor:")
        self.cBoxAround.addItems(str(i) for i in range(self.model.MAX_AROUND))
        self.cBoxAround.setFixedHeight(20)
        self.cBoxAround.setMaximumWidth(100)
        self.cBoxAround.currentIndexChanged.connect(self.controller.requestChangeAround)
        self.main_lay.addLayout(self.lay)
        h_lay = QHBoxLayout()
        h_lay.addWidget(self.aroundLbl)
        h_lay.addWidget(self.cBoxAround)
        self.main_lay.addLayout(h_lay)
        self.setLayout(self.main_lay)

    def _clearLayout(self):
        self.lbls.clear()
        self.lbls = []
        self.rBtns.clear()
        self.rBtns = []
        self.lblsColors.clear()
        self.lblsColors = []
        for i in reversed(range(self.lay.count())):
            row_lay = self.lay.takeAt(i)
            for j in reversed(range(row_lay.count())):
                row_lay.itemAt(j).widget().setParent(None)
            row_lay.setParent(None)

    def _setAroundSafe(self, around):
        self.cBoxAround.blockSignals(True)
        self.cBoxAround.setCurrentIndex(around)
        self.cBoxAround.blockSignals(False)

    def initUI(self, newData: dict):
        if 'around' in newData:
            self._setAroundSafe(newData['around'])
        coords_num = len(newData['coordinates'])
        w, h = self.model.current_image_size
        for i in range(coords_num):
            lay_row = QHBoxLayout()
            coord = newData['coordinates'][i]
            lay_row.addWidget(QLabel("X: %4d" % (coord[0] * w)))
            lay_row.addWidget(QLabel("Y: %4d" % (coord[1] * h)))
            colors = newData['values'][i]
            lblColor = QLabel("    ")
            lblColor.setStyleSheet("background-color: rgb({},{},{});".format(colors[0], colors[1], colors[2]))
            self.lblsColors.append(lblColor)
            lay_row.addWidget(lblColor)
            rbtn = QRadioButton()
            self.rBtns.append(rbtn)
            rbtn.toggled.connect(partial(self.controller.onCoordinateSelected, i))
            lay_row.addWidget(rbtn)
            self.lay.addLayout(lay_row)
        if len(self.rBtns) > 0:
            self.rBtns[self.controller.selectedCoordinateIndex].setChecked(True)

    def initConnectors(self):
        return
        # for i, rbtn in enumerate(self.rBtns):
        #   self.rbtn.toggled.connect(partial(self.controller.onCoordinateSelected, i))

    def changeData(self, new_data):
        self._clearLayout()
        self.initUI(new_data)
        if 'around' in new_data:
            if self.cBoxAround.currentIndex != new_data['around']:
                self._setAroundSafe(new_data['around'])
