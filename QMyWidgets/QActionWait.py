# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'action_wait.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QFormLayout, QVBoxLayout


class QActionWait(QWidget):
    def __init__(self, parent=QWidget):
        super(QWidget, self).__init__()
        self.lblName = QtWidgets.QLabel()
        self.lineEdit = QtWidgets.QLineEdit()
        self.lay = QVBoxLayout()
        self.setupUi()

    def setupUi(self):
        self.setLayout(self.lay)
        self.setFixedSize(100, 90)
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        self.setStyleSheet("background-color: rgb(233, 185, 110);")
        self.lblName.setGeometry(QtCore.QRect(25, 5, 50, 15))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.lblName.setFont(font)
        self.lblName.setAlignment(QtCore.Qt.AlignCenter)
        self.lblName.setObjectName("lblName")
        self.lblName.setText("Wait")
        self.lineEdit.setGeometry(QtCore.QRect(10, 40, 80, 23))
        self.lineEdit.setStyleSheet("background-color: rgb(238, 238, 236);")
        self.lineEdit.setObjectName("lineEdit")

        self.lay.addWidget(self.lblName)
        self.lay.addWidget(self.lineEdit)

        QtCore.QMetaObject.connectSlotsByName(self)
