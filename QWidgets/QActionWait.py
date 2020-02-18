# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'action_wait.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(100, 80)
        Form.setStyleSheet("background-color: rgb(233, 185, 110);")
        self.lblName = QtWidgets.QLabel(Form)
        self.lblName.setGeometry(QtCore.QRect(25, 5, 50, 15))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.lblName.setFont(font)
        self.lblName.setAlignment(QtCore.Qt.AlignCenter)
        self.lblName.setObjectName("lblName")
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(10, 40, 80, 23))
        self.lineEdit.setStyleSheet("background-color: rgb(238, 238, 236);")
        self.lineEdit.setObjectName("lineEdit")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.lblName.setText(_translate("Form", "wait"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

