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
        self.bottom_lay = QVBoxLayout()
        self.scroll_wid = QWidget()
        self.scrollable = QScrollArea()
        self.lay = QVBoxLayout()
        self.lbls = []
        self.lblsColors = []
        self.lblImageColors = []
        self.rBtns = []
        self.btnAddCoord = QPushButton()
        self.aroundLbl = QLabel()
        self.cBoxAround = QComboBox()
        self.initMainUI()
        self.initUI({'coordinates': [[0.5, 0.5]], 'values': [[255, 255, 255]], 'around': 5,
                     'currentScreenColors': [[255, 255, 255]]})
        self.initConnectors()

    def initMainUI(self):
        self.setLayout(self.main_lay)
        self.aroundLbl.setText("Around factor:")
        self.cBoxAround.addItems(str(i) for i in range(self.model.MAX_AROUND))
        self.cBoxAround.setFixedHeight(20)
        self.cBoxAround.setMaximumWidth(100)
        self.cBoxAround.currentIndexChanged.connect(self.controller.requestChangeAround)
        self.btnAddCoord.setText("add coordinate")
        self.btnAddCoord.clicked.connect(self.controller.requestFrameCheckCoordAdd)

        self.lay.setAlignment(Qt.AlignTop)
        self.scroll_wid.setLayout(self.lay)
        self.scrollable.setWidgetResizable(True)
        self.scrollable.setWidget(self.scroll_wid)
        self.scrollable.setContentsMargins(0, 0, 0, 0)

        self.main_lay.addWidget(self.scrollable)

        self.bottom_lay.addWidget(self.btnAddCoord)
        h_lay = QHBoxLayout()
        h_lay.addWidget(self.aroundLbl)
        h_lay.addWidget(self.cBoxAround)
        self.bottom_lay.addLayout(h_lay)

        self.main_lay.addLayout(self.bottom_lay)

    def _clearLayout(self):
        self.lbls.clear()
        self.lbls = []
        self.rBtns.clear()
        self.rBtns = []
        self.lblsColors.clear()
        self.lblsColors = []
        self.lblImageColors.clear()
        self.lblImageColors = []
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
        l = len(newData['currentScreenColors'])
        w, h = self.controller.current_image_size
        for i in range(coords_num):
            lay_row = QHBoxLayout()
            coord = newData['coordinates'][i]
            x, y = int((coord[0] * w)), int((coord[1] * h))
            lbl_point = QLabel("%15s" % ("C%d: %4d , %4d" % (i, x, y)))
            lbl_point.setFixedWidth(80)
            lay_row.addWidget(lbl_point)
            # lay_row.addWidget(QLabel("X: %4d" % (coord[0] * w)))
            # lay_row.addWidget(QLabel("Y: %4d" % (coord[1] * h)))
            colors = newData['values'][i]
            lblColor = QLabel("")
            lblColor.setStyleSheet("background-color: rgb({},{},{});".format(colors[0], colors[1], colors[2]))
            lblColor.mousePressEvent = (partial(self.onManualChoose, i))
            lblColor.setToolTip("Target value RGB=(%d, %d, %d)" % (colors[0], colors[1], colors[2]))
            lblColor.setMaximumWidth(40)
            self.lblsColors.append(lblColor)
            btnSet = QPushButton("set->")
            btnSet.setMaximumWidth(45)
            btnSet.clicked.connect(partial(self.controller.requestSetCurrentColorToFrameCheckColor, i))
            lblimgColor = QLabel("")
            lblimgColor.setMaximumWidth(20)
            color_ = newData['currentScreenColors'][i]
            lblimgColor.setStyleSheet("background-color: rgb({},{},{});".format(color_[0], color_[1], color_[2]))
            lblimgColor.setToolTip("Current screenshot RGB=(%d, %d, %d)" % (color_[0], color_[1], color_[2]))
            lblimgColor.setToolTipDuration(20 * 1000)
            self.lblImageColors.append(lblimgColor)
            lay_row.addWidget(lblimgColor)
            lay_row.addWidget(btnSet)
            lay_row.addWidget(lblColor)
            rbtn = QRadioButton()
            self.rBtns.append(rbtn)
            rbtn.setText("")
            rbtn.setFixedWidth(20)
            rbtn.toggled.connect(partial(self.controller.onCoordinateSelected, i))
            lay_row.addWidget(rbtn)
            self.lay.addLayout(lay_row)
        if len(self.rBtns) > 0:
            # this is not working as intended after an update.
            #self.rBtns[self.controller.selectedCoordinateIndex].blockSignals(True)
            #self.rBtns[self.controller.selectedCoordinateIndex].setChecked(True)
            #self.rBtns[self.controller.selectedCoordinateIndex].blockSignals(False)
            pass

    def onManualChoose(self, i, event):
        self.controller.rquestFrameCheckCoordinateColorManualChange(i)

    def updateCurrentColors(self, colors_img):
        num = min(len(colors_img), len(self.lblImageColors))
        for i in range(num):
            color = colors_img[i]
            self.lblImageColors[i].setStyleSheet(
                "background-color: rgb({},{},{});".format(color[0], color[1], color[2]))

    def initConnectors(self):
        self.controller.onCurrentScreenColorsChanged.connect(self.updateCurrentColors)
        return
        # for i, rbtn in enumerate(self.rBtns):
        #   self.rbtn.toggled.connect(partial(self.controller.onCoordinateSelected, i))

    def changeData(self, new_data):
        self._clearLayout()
        self.initUI(new_data)
        if 'around' in new_data:
            if self.cBoxAround.currentIndex != new_data['around']:
                self._setAroundSafe(new_data['around'])

    def deleteLater(self):
        self.controller.onCurrentScreenColorsChanged.disconnect(self.updateCurrentColors)
        super(FrameCheckOption, self).deleteLater()
