# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'action_tap.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QWidget, QFormLayout, QFrame, QVBoxLayout


class QActionTap(QWidget):
    def __init__(self, parent=QWidget):
        super(QActionTap, self).__init__(parent)
        self.parent = parent
        self.lblName = QtWidgets.QLabel()
        self.cBoxDirection = QtWidgets.QComboBox()
        self.lay = QVBoxLayout()
        self.setupUi()

    def setupUi(self):
        self.setFixedSize(100, 60)
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        self.setStyleSheet("background-color: rgb(173, 127, 168);")
        self.lblName.setGeometry(QtCore.QRect(25, 5, 50, 15))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.lblName.setFont(font)
        self.lblName.setAlignment(QtCore.Qt.AlignCenter)
        self.lblName.setObjectName("lblName")
        self.lblName.setText("Tap")
        self.cBoxDirection.setGeometry(QtCore.QRect(10, 40, 80, 23))
        self.cBoxDirection.setStyleSheet("background-color: rgb(238, 238, 236);")
        self.cBoxDirection.setObjectName("cBoxDirection")

        self.lay.addWidget(self.lblName)
        self.lay.addWidget(self.cBoxDirection)

        self.setLayout(self.lay)
        QtCore.QMetaObject.connectSlotsByName(self)
