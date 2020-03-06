# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'run.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(140, 26)
        Form.setStyleSheet("background-color: rgb(138, 226, 52);")
        self.lblName = QtWidgets.QLabel(Form)
        self.lblName.setGeometry(QtCore.QRect(0, 3, 140, 20))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.lblName.setFont(font)
        self.lblName.setAlignment(QtCore.Qt.AlignCenter)
        self.lblName.setObjectName("lblName")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.lblName.setText(_translate("Form", "6. The Cave"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

