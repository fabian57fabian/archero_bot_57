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


class FrameCheckOption(QWidget):
    def __init__(self, parent: QObject, controller: TouchManagerController, model: TouchManagerModel):
        super(QWidget, self).__init__()
        self.parent = parent
        self.model = model
        self.controller = controller
        self.lay = QVBoxLayout()
        self.lbls = []
        self.lblsColors = []
        self.rBtns = []
        self.initUI({'coordinates': [[0.5, 0.5]], 'values': [[255, 255, 255]], 'around': 5})
        self.initConnectors()

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

    def initUI(self, newData: dict):
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
        self.setLayout(self.lay)
        return
        self.rBtnChangeableSrc.setText("Change")
        self.rBtnChangeableDst.setText("Change")
        if self.controller.selectedCoordinateIndex == 0:
            self.rBtnChangeableSrc.setChecked(True)
        else:
            self.rBtnChangeableDst.setChecked(True)
        self.lay_h1.addWidget(self.lblXsrc)
        self.lay_h1.addWidget(self.lblYsrc)
        self.lay_h1.addWidget(self.rBtnChangeableSrc)

        self.lay_h2.addWidget(self.lblXdst)
        self.lay_h2.addWidget(self.lblYdst)
        self.lay_h2.addWidget(self.rBtnChangeableDst)

        self.lay.addLayout(self.lay_h1)
        self.lay.addWidget(QLabel("to"))
        self.lay.addLayout(self.lay_h2)
        self.setLayout(self.lay)
        self.changeData([[0, 0], [0, 0]])

    def initConnectors(self):
        return
        # for i, rbtn in enumerate(self.rBtns):
        #   self.rbtn.toggled.connect(partial(self.controller.onCoordinateSelected, i))

    def changeData(self, new_data):
        self._clearLayout()
        self.initUI(new_data)
        return
        w, h = self.model.current_image_size
        for i, [lblX, lblY] in self.lbls:
            self.lblXsrc.setText("X: %4d" % (new_data[0][0] * w))
        self.lblYsrc.setText("Y: %4d" % (new_data[0][1] * h))
