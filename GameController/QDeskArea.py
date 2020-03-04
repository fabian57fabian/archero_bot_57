from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QHBoxLayout, QBoxLayout, QVBoxLayout, QPushButton, QWidget, QScrollArea, QLabel, \
    QFormLayout, QGridLayout
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QSize
from PyQt5 import QtWidgets, uic
from QWidgets.QActionTap import QActionTap
from QWidgets.QActionWalk import QActionWalk
from QWidgets.QActionWait import QActionWait


class QDeskArea(QWidget):
    def __init__(self, parent=QWidget):
        super(QDeskArea, self).__init__()
        self.scroll = QScrollArea()  # Scroll Area which contains the widgets, set as the centralWidget
        self.widget = QWidget()  # Widget that contains the collection of Vertical Box
        self.box = QHBoxLayout()  # The H Box that contains the V Boxes of  labels and buttons
        self.main_layout = QHBoxLayout()
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        self.setStyleSheet("background-color: rgb(43, 43, 43)")
        self.initUI()

    def build_add_btn(self):
        button = QPushButton(self)
        button.setFixedSize(26, 26)
        button.setText("+")
        button.setStyleSheet("background-color: white; border-radius: 13px;text-align: center")
        return button

    def initUI(self):
        self.setLayout(self.main_layout)
        #self.grid_lay.setSpacing(0)
        #self.grid_lay.setContentsMargins(0, 0, 0, 0)
        #self.grid_lay.addLayout(self.main_layout)
        #self.grid_lay.setAlignment(self.main_layout,Qt.AlignCenter)
        first_btn = self.build_add_btn()
        self.box.addWidget(first_btn)
        for i in range(1, 10):
            if i % 3 == 0:
                object = QActionTap(self)
            elif i % 3 == 1:
                object = QActionWait(self)
            else:
                object = QActionWalk(self)
            self.box.addWidget(object)
            btn = self.build_add_btn()
            self.box.addWidget(btn)
        self.widget.setLayout(self.box)

        # Scroll Area Properties
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)
        self.scroll.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.scroll)
        #self.setSizePolicy(
        #    QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding))
        # self.setCentralWidget(self.scroll)

        # self.setGeometry(600, 100, 1000, 900)
