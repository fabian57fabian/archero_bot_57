from functools import partial

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtWidgets import QHBoxLayout, QBoxLayout, QVBoxLayout, QPushButton, QWidget, QScrollArea, QLabel, \
    QFormLayout, QGridLayout, QLineEdit, QInputDialog, QColorDialog
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QSize, pyqtSignal, QObject
from PyQt5 import QtWidgets, uic
from TouchManager.TouchManagerModel import TouchManagerModel
import enum
import os


class ShowAreaState(enum.Enum):
    Buttons = 1
    Movements = 2
    FrameCheck = 3


class TouchManagerController(QObject):
    onCurrentShowAreaChanged = pyqtSignal(ShowAreaState)
    onElementSelectionChanged = pyqtSignal(str)
    onImageSelectionChanged = pyqtSignal(str)

    onImagesChanged = pyqtSignal(dict)
    onButtonsChanged = pyqtSignal(dict)
    onCurrentScreenColorsChanged = pyqtSignal(list)

    onSelectedCoordinateChanged = pyqtSignal(int)

    def __init__(self, model: TouchManagerModel):
        super(QObject, self).__init__()
        self.model = model
        self.dict_selected = ""
        self.image_selected = ""
        self.currentImage: QPixmap = None
        self.current_image_size = [0, 0]
        self.selectedCoordinateIndex = 0
        self.currentCoordinates = [[0, 0]]
        self.currentScreenColors = []
        self.currentAreaType: ShowAreaState = ShowAreaState.Buttons
        self.initConnectors()

    def initConnectors(self):
        self.model.onDictionaryTapsChanged.connect(partial(self.onGeneralDictionaryChanged, ShowAreaState.Buttons))
        self.model.onDictionaryMovementsChanged.connect(
            partial(self.onGeneralDictionaryChanged, ShowAreaState.Movements))
        self.model.onDictionaryFrameChecksChanged.connect(
            partial(self.onGeneralDictionaryChanged, ShowAreaState.FrameCheck))
        self.model.onSourceChanged.connect(self.onImagesFilesChanged)
        self.model.onButtonLocationChanged.connect(self.onCurrentCoordChanged)

    def requestSetCurrentColorToFrameCheckColor(self, index):
        self.model.changeFrameCheckColor(self.dict_selected, index, self._getPixelFromCoord(
            self.model.currentFrameChecks[self.dict_selected]['coordinates'][index]))

    def rquestFrameCheckCoordinateColorManualChange(self, index):
        color = QColorDialog.getColor()
        if color.isValid():
            self.model.changeFrameCheckColor(self.dict_selected, index, color.getRgb())
        else:
            pass  # No color selected

    def _getPixelFromCoord(self, coord):
        # TODO: get argb frmo QPixmap # self.currentImage.pixe
        x, y = coord[0] * self.current_image_size[0], coord[1] * self.current_image_size[1]
        argb = self.currentImage.toImage().pixel(int(x), int(y))
        rgba = QColor(argb).getRgb()
        return rgba

    def _getCurrentImageCoordsColors(self):
        if self.currentAreaType != ShowAreaState.FrameCheck or self.dict_selected == '':
            return []
        colors = []
        for i, coord in enumerate(self.model.currentFrameChecks[self.dict_selected]['coordinates']):
            c = self._getPixelFromCoord(coord)
            colors.append(c)
        return colors

    def requestLoadPixamp(self):
        path = self.getCurrentImageLocation()
        self.currentImage = QPixmap(path)
        self.current_image_size = [self.currentImage.width(), self.currentImage.height()]
        return self.currentImage.copy()

    def requestChangeLineWidth(self, index):
        if 0 <= index < len(self.model.linePermittedSizes):
            self.model.changeCurrentLineWidth(index)

    def requestAddPoint(self):
        name, ok = QInputDialog.getText(QWidget(), "Get name", "Point name:", QLineEdit.Normal, "")
        if ok and name != '':
            if name not in self.dataFromAreaType().keys():
                if self.currentAreaType == ShowAreaState.Buttons:
                    self.model.addElementButton(name)
                elif self.currentAreaType == ShowAreaState.Movements:
                    self.model.addElementMovement(name)
                elif self.currentAreaType == ShowAreaState.FrameCheck:
                    self.model.addElementFrameCheck(name)

    def onGeneralDictionaryChanged(self, areaType: ShowAreaState):
        self.showDifferentElemStateRequested(areaType)
        self.onCurrentDictChanged(self.dataFromAreaType())

    def onCurrentCoordChanged(self, dict_name):
        self.updatecurrentCoordinate()

    def onCurrentDictChanged(self, newDict):
        self.onButtonsChanged.emit(newDict)
        if len(newDict.keys()) > 0:
            self.elementSelectRequets(list(newDict.keys())[0])
        else:
            self.dict_selected = ""

    def onImagesFilesChanged(self, newDict):
        self.onImagesChanged.emit(newDict)
        if len(newDict.keys()) > 0:
            self.imageSelectRequets(list(newDict.keys())[0])
        else:
            self.image_selected = ""

    def showDifferentElemStateRequested(self, new_state: ShowAreaState):
        if self.currentAreaType != new_state:
            self.selectedCoordinateIndex = 0
        self.currentAreaType = new_state
        self.onCurrentShowAreaChanged.emit(new_state)
        first = list(self.dataFromAreaType().keys())[0]
        self.elementSelectRequets(first)

    # def listElementSelected(self, button_name):
    #     self.dict_selected = button_name
    #     self.button_pos_clicked(button_name)

    def dataFromAreaType(self):
        if self.currentAreaType == ShowAreaState.Buttons:
            return self.model.currentDict
        elif self.currentAreaType == ShowAreaState.Movements:
            return self.model.currentMovements
        elif self.currentAreaType == ShowAreaState.FrameCheck:
            return self.model.currentFrameChecks
        else:
            return {}

    def updatecurrentCoordinate(self):
        if self.currentAreaType == ShowAreaState.Buttons:
            self.currentCoordinates = [self.dataFromAreaType()[self.dict_selected].copy()]
        if self.currentAreaType == ShowAreaState.Movements:
            self.currentCoordinates = self.dataFromAreaType()[self.dict_selected].copy()
        if self.currentAreaType == ShowAreaState.FrameCheck:
            self.currentCoordinates = self.dataFromAreaType()[self.dict_selected]['coordinates'].copy()
            self.updatecurrentFrameCheckColors()

    def elementSelectRequets(self, btn_name):
        self.dict_selected = btn_name
        self.updatecurrentCoordinate()
        if self.selectedCoordinateIndex >= len(self.currentCoordinates):
            self.selectedCoordinateIndex = len(self.currentCoordinates) - 1
        self.onElementSelectionChanged.emit(self.dict_selected)

    def updatecurrentFrameCheckColors(self):
        if self.currentAreaType == ShowAreaState.FrameCheck:
            self.currentScreenColors = self._getCurrentImageCoordsColors()
            self.onCurrentScreenColorsChanged.emit(self.currentScreenColors)

    def imageSelectRequets(self, image_name):
        if image_name in self.model.currentFiles:
            self.image_selected = image_name
            self.updatecurrentFrameCheckColors()
            self.onImageSelectionChanged.emit(self.image_selected)

    def nextImageSelectRequest(self):
        index = list(self.model.currentFiles).index(self.image_selected)
        index = 0 if index + 1 == len(self.model.currentFiles) else index + 1
        self.imageSelectRequets(list(self.model.currentFiles)[index])

    def prevImageSelectRequest(self):
        index = list(self.model.currentFiles).index(self.image_selected)
        index = len(self.model.currentFiles) if index - 1 == 0 else index - 1
        self.imageSelectRequets(list(self.model.currentFiles)[index])

    def requestScreenFolderChange(self, new_folder):
        if new_folder != self.model.currentScreensFolder:
            self.model.changeScreensFolder(new_folder)

    def getCurrentImageLocation(self):
        return os.path.join(self.model.currentScreensPath(), self.image_selected)

    def onCoordinateSelected(self, index):
        self.selectedCoordinateIndex = index
        self.onSelectedCoordinateChanged.emit(self.selectedCoordinateIndex)

    def requestChangeCoordinate(self, x1, y1):
        if self.currentAreaType == ShowAreaState.Buttons:
            self.model.changeButtonPosition(self.dict_selected, [x1, y1])
        elif self.currentAreaType == ShowAreaState.Movements:
            self.model.changeMovementPosition(self.dict_selected, [x1, y1], self.selectedCoordinateIndex)
        elif self.currentAreaType == ShowAreaState.FrameCheck:
            self.model.changeFrameCheckPosition(self.dict_selected, [x1, y1], self.selectedCoordinateIndex)

    def requestChangeAround(self, around: int):
        if around >= 0:
            self.model.changeAroundFactor(self.dict_selected, around)
