import csv
import json
import os
from functools import partial

from PyQt5 import QtWidgets
import sys
import datetime
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QFormLayout, QPushButton
import enum


class State(enum.Enum):
    Ready = 0,
    Started = 1


class UtilityTestModel(QObject):
    languageChanged = pyqtSignal(str)
    testStarted = pyqtSignal()

    def __init__(self):
        super(QObject, self).__init__()
        self.State = State.Ready
        self.dateFormat = "%d%m%Y_%H%M%S.%f"
        self.statistics_file = 'utility_test_data.csv'
        self.languages = ['english', 'italiano']
        self.selected_language = 0
        self.titleText = ''
        self.nextBtnText = ''
        self.startBtnText = ''
        self.endingText = ''
        self.questions = []
        self.load_data()

    def _changeQuestions(self, new_questions):
        self.questions = new_questions
        self.qustionsChanged.emit(self.questions)

    def changeLanguage(self, new_language):
        if new_language in self.languages:
            self.selected_language = self.languages.index(new_language)
            self.load_data()

    def load_data(self):
        with open(os.path.join('datas', 'utility_test_datas', 'utility_test_{}.json'.format(self.languages[self.selected_language])), 'r') as f:
            data_dict = json.load(f)
        self.titleText = data_dict['titleText']
        self.questions = data_dict['questions']
        self.startBtnText = data_dict['startBtnText']
        self.nextBtnText = data_dict['nextBtnText']
        self.endingText = data_dict['endingText']
        self.languageChanged.emit(self.languages[self.selected_language])

    def save_tap(self, id):
        try:
            data = [datetime.datetime.now().strftime(self.dateFormat), id]
            with open(self.statistics_file, 'a+', newline='') as write_obj:
                csv_writer = csv.writer(write_obj)
                csv_writer.writerow(data)
            return True
        except Exception as e:
            print("Errors writing statistics: %s" % str(e))
            return False

    def startTest(self):
        self.save_tap(-1)
        self.State = State.Started
        self.testStarted.emit()


class UtilityTestController(QObject):
    currentQuestionChanged = pyqtSignal(str, int)
    testEnded = pyqtSignal()

    def __init__(self, model: UtilityTestModel):
        super(QObject, self).__init__()
        self.model = model
        self.currentQuestionIndex = -1
        self.initConnectors()

    def initConnectors(self):
        self.model.testStarted.connect(self.onTestStarted)

    def onTestStarted(self):
        self.currentQuestionIndex = 0
        self.currentQuestionChanged.emit(self.model.questions[self.currentQuestionIndex], self.currentQuestionIndex)

    def requestChangeSelectedLanguage(self, text):
        if text in self.model.languages:
            self.model.changeLanguage(text)

    def requestStartTest(self):
        if self.model.State != State.Started:
            self.model.startTest()

    def endedCurrentQuestion(self, index):
        self.model.save_tap(index)
        self.currentQuestionIndex += 1
        if self.currentQuestionIndex < len(self.model.questions):
            self.currentQuestionChanged.emit(self.model.questions[self.currentQuestionIndex], self.currentQuestionIndex)
        else:
            self.testEnded.emit()


class UtilityTestUi(QWidget):
    def __init__(self, model: UtilityTestModel, controller: UtilityTestController):
        super(QWidget, self).__init__()
        self.model = model
        self.controller = controller
        self.cBoxLanguage = QComboBox()
        self.main_lay = QVBoxLayout()
        self.layQuestions = QVBoxLayout()
        self.lblTitle = QLabel()
        self.btnStart = QPushButton()
        self.lblEnd = None
        self.lblQuestions = []
        self.btnQuestions = []
        self.initConnectors()

    def setupUI(self, main_window):
        main_window.setObjectName("main_window")
        self.main_lay.setAlignment(Qt.AlignTop)
        main_window.setMinimumSize(640, 480)
        title_lay = QHBoxLayout()
        title_lay.addWidget(QLabel("Utility test"))
        title_lay.addWidget(self.cBoxLanguage)
        self.main_lay.addLayout(title_lay)
        self.main_lay.addWidget(self.lblTitle)
        self.btnStart.setText("Start")
        self.main_lay.addWidget(self.btnStart)
        self.main_lay.addLayout(self.layQuestions)
        self.cBoxLanguage.setMaximumWidth(80)
        self.cBoxLanguage.addItems(self.model.languages)
        # centralwidget.setLayout(self.main_lay)
        wid = QWidget()
        wid.setLayout(self.main_lay)
        main_window.setCentralWidget(wid)

    def initConnectors(self):
        self.model.languageChanged.connect(self.onLanguageChanged)
        self.model.testStarted.connect(self.onTestStarted)
        self.controller.currentQuestionChanged.connect(self.onNewQuestionArrived)
        self.controller.testEnded.connect(self.onTestEnded)
        self.cBoxLanguage.currentTextChanged.connect(self.controller.requestChangeSelectedLanguage)
        self.btnStart.clicked.connect(self.controller.requestStartTest)

    def onLanguageChanged(self, new_language):
        self.btnStart.setText(self.model.startBtnText)
        self.lblTitle.setText(self.model.titleText)
        for i, lblQuestion in enumerate(self.lblQuestions):
            if i < len(self.model.questions):
                lblQuestion.setText(self.model.questions[i])
        for i, btnQuestion in enumerate(self.btnQuestions):
            if i < len(self.model.questions):
                btnQuestion.setText(self.model.nextBtnText)
        if self.lblEnd is not None:
            self.lblEnd.setText(self.model.endingText)

    def onTestStarted(self):
        self.btnStart.setEnabled(False)

    def disableAllPreviousQuestions(self):
        for lbl, btn in zip(self.lblQuestions, self.btnQuestions):
            lbl.setStyleSheet("color: gray;")  # setEnabled(False)
            btn.setEnabled(False)

    def onNewQuestionArrived(self, question, index):
        lbl = QLabel(question)
        btn = QPushButton('Done' if self.model.selected_language == 'english' else 'Finito')
        btn.clicked.connect(partial(self.controller.endedCurrentQuestion, index))
        btn.setMaximumWidth(80)
        self.disableAllPreviousQuestions()
        self.lblQuestions.append(lbl)
        self.btnQuestions.append(btn)
        hor = QHBoxLayout()
        hor.addWidget(lbl)
        hor.addWidget(btn)
        self.layQuestions.addLayout(hor)

    def onTestEnded(self):
        self.disableAllPreviousQuestions()
        self.lblEnd = QLabel(self.model.endingText.format(self.model.statistics_file))
        self.layQuestions.addWidget(self.lblEnd)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    model = UtilityTestModel()
    controller = UtilityTestController(model)
    ui = UtilityTestUi(model, controller)
    ui.setupUI(MainWindow)
    model.load_data()
    MainWindow.show()
    sys.exit(app.exec_())
