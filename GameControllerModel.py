import os
from PyQt5.QtCore import pyqtSignal, QObject


class GameControllerModel(QObject):
    # onSourceChanged = pyqtSignal(list)
    # onDictionaryTapsChanged = pyqtSignal(dict)
    # onButtonLocationChanged = pyqtSignal(str)
    # onImageSelected = pyqtSignal()

    def __init__(self):
        super(GameControllerModel, self).__init__()
        # Default data
        self.dict_buttons = 'data.py'

    def load_data(self):
        pass