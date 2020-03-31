# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'action_walk.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QFormLayout, QVBoxLayout, QHBoxLayout


class QActionWalk(QWidget):
    def __init__(self, parent=QWidget):
        super(QWidget, self).__init__()
        self.parent = parent
        self.lblName = QtWidgets.QLabel(self)
        self.cBoxDirection = QtWidgets.QComboBox(self)
        self.txtDuration = QtWidgets.QLineEdit(self)
        self.lblInfoDirection = QtWidgets.QLabel(self)
        self.lblInfoDirection_2 = QtWidgets.QLabel(self)
        self.lay = QVBoxLayout()
        self.setupUi()

    def setupUi(self):
        self.setLayout(self.lay)
        #self.lay.setSpacing(0)
        self.lay.setContentsMargins(5, 0, 5, 0)
        self.lay.setAlignment(QtCore.Qt.AlignCenter)
        self.setFixedSize(100, 100)
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        self.setStyleSheet("background-color: rgb(138, 226, 52);")

        self.lblName.setFixedSize(50, 15)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.lblName.setFont(font)
        self.lblName.setAlignment(QtCore.Qt.AlignCenter)
        self.lblName.setObjectName("lblName")
        self.lblName.setText("Walk")
        self.lay.addWidget(self.lblName)

        self.cBoxDirection.setFixedSize(70, 23)
        self.cBoxDirection.setStyleSheet("background-color: rgb(238, 238, 236);")
        self.cBoxDirection.setObjectName("cBoxDirection")

        self.txtDuration.setFixedSize(70, 23)
        self.txtDuration.setStyleSheet("background-color: rgb(238, 238, 236);")
        self.txtDuration.setObjectName("txtDuration")

        self.lblInfoDirection.setFixedSize(16, 16)
        self.lblInfoDirection.setObjectName("lblInfoDirection")
        self.lblInfoDirection.setText("D:")

        self.lblInfoDirection_2.setFixedSize(16, 16)
        self.lblInfoDirection_2.setObjectName("lblInfoDirection_2")
        self.lblInfoDirection_2.setText("T:")


        #wid = QWidget()
        #v_lay = QVBoxLayout()
        #v_lay.setSpacing(0)
        #v_lay.setContentsMargins(0, 0, 0, 0)
        #wid.setLayout(v_lay)


        hor1 = QHBoxLayout()
        hor1.addWidget(self.lblInfoDirection)
        hor1.addWidget(self.cBoxDirection)
        hor1.setSpacing(0)
        hor1.setContentsMargins(0, 0, 0, 0)
        self.lay.addLayout(hor1)

        hor2 = QHBoxLayout()
        hor2.addWidget(self.lblInfoDirection_2)
        hor2.addWidget(self.txtDuration)
        hor2.setSpacing(0)
        hor2.setContentsMargins(0, 0, 0, 0)
        self.lay.addLayout(hor2)

        #self.lay.addWidget(wid)


        QtCore.QMetaObject.connectSlotsByName(self)
