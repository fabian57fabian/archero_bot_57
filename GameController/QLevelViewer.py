from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QFrame, QLabel, QVBoxLayout, QHBoxLayout, QWidget
from PyQt5 import QtCore, QtGui, QtWidgets
from GameController.GameControllerModel import GameControllerModel,EngineState

class QLevelViewer(QWidget):
    onLevelClicked = pyqtSignal()

    def __init__(self, model: GameControllerModel, level_num=0, level_name=None, parent=QWidget):
        super(QWidget, self).__init__()
        self.model = model
        self.lblNumber = QLabel()
        self.lblName = QLabel()
        self.frame = QFrame()
        self.level_name = level_name
        self.level_num = level_num
        self._setupUI()
        self.changeLevel(level_num, level_name)
        self.isClickable = False
        self.setClickable(self.isClickable)

    def _getColorByLevel(self, level_name: str):
        if level_name == "Intro":
            return (247, 181, 41)
        elif level_name == "Normal":
            return (23, 107, 239)
        elif level_name == "Heal":
            return (23, 156, 82)
        elif level_name == "Boss":
            return (255, 62, 48)
        elif level_name == "Final_B":
            return (127, 0, 0)
        else:
            return (255, 255, 255)

    def _changeLevelColor(self):
        level_color = self._getColorByLevel(self.level_name)
        self.frame.setStyleSheet(
            "background-color: rgb({}, {}, {}); border-radius: 5px;".format(level_color[0], level_color[1],
                                                                            level_color[2]))
    def changeLevel(self, newlevel: int, level_name=None):
        self.level_num = newlevel
        if level_name is not None:
            self.level_name = level_name
        else:
            for i, v in self.model.getLevelsNames().items():
                if i == newlevel:
                    self.level_name = v
                    break
        self.lblName.setText(self.level_name)
        self.lblNumber.setText(str(newlevel))
        self._changeLevelColor()

    def onSelfClicked(self, event):
        self.onLevelClicked.emit()

    def setClickable(self, isClickable: bool):
        self.isClickable = isClickable
        self.updateClickableUi(self.isClickable)

    def updateClickableUi(self, can_click):
        self.lblNumber.blockSignals(not can_click)
        self.lblName.blockSignals(not can_click)
        self.frame.blockSignals(not can_click)
        if can_click:
            self.lblNumber.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
            self.lblName.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
            self.frame.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        else:
            self.lblNumber.setCursor(QCursor(QtCore.Qt.ArrowCursor))
            self.lblName.setCursor(QCursor(QtCore.Qt.ArrowCursor))
            self.frame.setCursor(QCursor(QtCore.Qt.ArrowCursor))

    def _setupUI(self):
        self.frame.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        self.frame.setFixedSize(80, 80)
        self.frame.setGeometry(0, 0, 0, 0)
        self.frame.mousePressEvent = self.onSelfClicked
        font = QtGui.QFont()
        font.setPointSize(15)
        self.lblNumber.setFont(font)
        self.lblNumber.setAlignment(Qt.AlignCenter)
        self.lblNumber.mousePressEvent = self.onSelfClicked
        font_name = QtGui.QFont()
        font_name.setPointSize(15)
        self.lblName.setFont(font_name)
        self.lblName.setAlignment(QtCore.Qt.AlignCenter)
        self.lblName.mousePressEvent = self.onSelfClicked

        frame_lay = QVBoxLayout()
        frame_lay.addWidget(self.lblNumber)
        frame_lay.addWidget(self.lblName)
        self.frame.setLayout(frame_lay)
        fram_lay = QHBoxLayout()
        fram_lay.addWidget(self.frame)
        self.setLayout(fram_lay)

        self.model.engineStatechanged.connect(self.onPlayStateChanged)

    def onPlayStateChanged(self, newState: EngineState):
        self.updateClickableUi(self.isClickable and ( not newState == EngineState.Playing))
