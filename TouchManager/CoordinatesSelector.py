from functools import partial

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QHBoxLayout, QBoxLayout, QVBoxLayout, QPushButton, QWidget, QScrollArea, QLabel, \
    QFormLayout, QGridLayout
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QSize, pyqtSignal
from PyQt5 import QtWidgets, uic
from QMyWidgets.QLevelState import QLevelState, PlayState
from TouchManager.TouchManagerController import TouchManagerController
from TouchManager.TouchManagerModel import TouchManagerModel
from TouchManager.TouchManagerController import ShowAreaState


class CoordinatesSelector(QWidget):

    def __init__(self, parent: QWidget, controller: TouchManagerController, model: TouchManagerModel):
        super(QWidget, self).__init__()
        self.model = model
        self.controller = controller
        self.btn_buttons = QPushButton()
        self.btn_movements = QPushButton()
        self.btn_checkpoints = QPushButton()
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        self.last_type_selected = ShowAreaState.Buttons
        self.buttonsHeight = 40
        self.initUI()
        self.initSignals()

    def initUI(self):
        lay = QHBoxLayout()
        # lay.setAlignment(Qt.AlignCenter)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)
        self.btn_buttons.setText("buttons")
        self.btn_movements.setText("movements")
        self.btn_checkpoints.setText("checkpoints")
        self.btn_buttons.isEnabled = True
        self.btn_movements.isEnabled = True
        self.btn_checkpoints.isEnabled = True
        lay.addWidget(self.btn_buttons)
        lay.addWidget(self.btn_movements)
        lay.addWidget(self.btn_checkpoints)
        self.setLayout(lay)

    def initSignals(self):
        self.controller.onCurrentShowAreaChanged.connect(self.onAreaStatechanged)
        self.btn_buttons.clicked.connect(
            partial(self.controller.showDifferentElemStateRequested, ShowAreaState.Buttons))
        self.btn_movements.clicked.connect(
            partial(self.controller.showDifferentElemStateRequested, ShowAreaState.Movements))
        self.btn_checkpoints.clicked.connect(
            partial(self.controller.showDifferentElemStateRequested, ShowAreaState.FrameCheck))

    def _setButtonSelection(self, btn, selected: bool):
        if selected:
            btn.setStyleSheet("background-color: rgb({}, {}, {})".format(self.model.ui_color[0], self.model.ui_color[1],
                                                                         self.model.ui_color[2]))
        else:
            btn.setStyleSheet("QPushButton { background-color : (225,225,225); }")

    def onAreaStatechanged(self, newAreaState: ShowAreaState):
        self._change_btn_byType(self.last_type_selected, False)
        self._change_btn_byType(newAreaState, True)
        self.last_type_selected = newAreaState

    def _change_btn_byType(self, state: ShowAreaState, selected: bool):
        if state == ShowAreaState.Buttons:
            self._setButtonSelection(self.btn_buttons, selected)
        elif state == ShowAreaState.Movements:
            self._setButtonSelection(self.btn_movements, selected)
        elif state == ShowAreaState.FrameCheck:
            self._setButtonSelection(self.btn_checkpoints, selected)
