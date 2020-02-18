from functools import partial

from PyQt5.QtGui import QPainter, QPen, QBrush, QColor

from GameControllerModel import GameControllerModel
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QPushButton, QScrollArea, QLabel, QFormLayout, QMainWindow
import os


class GameControllerWindow(object):

    def __init__(self, model: GameControllerModel):
        self.model = model
        #self.model.onSourceChanged.connect(self.source_changed)

    def setupUi(self, main_window: QMainWindow):
        main_window.setObjectName("main_window")
        main_window.resize(800, 600)
        main_window.setMaximumWidth(800)
        main_window.setMaximumHeight(600)