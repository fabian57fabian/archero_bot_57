from PyQt5.QtGui import QPainter, QPen, QBrush, QColor
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import Qt, pyqtSignal, QMetaObject
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QMainWindow, \
    QInputDialog, QLineEdit, QComboBox, QWidget, QSpacerItem
from TouchManager.TouchManagerModel import TouchManagerModel
from TouchManager.TouchManagerController import TouchManagerController
from TouchManager.TouchManagerController import ShowAreaState
from TouchManager.CoordinatesSelector import CoordinatesSelector
from TouchManager.SwipableListWidget import SwipableListWidget

from TouchManager.ElementOption import ElementOption


class TouchManagerWindow(QWidget):
    def __init__(self, controller: TouchManagerController, model: TouchManagerModel):
        super(QWidget, self).__init__()
        self.model = model
        self.controller = controller

        self.optionArea = ElementOption(self, self.controller, self.model)
        self.controller.onCurrentShowAreaChanged.connect(self.optionArea.areatypeChanged)
        self.model.onButtonLocationChanged.connect(self.optionArea.onElementChanged)

        self.controller.onImagesChanged.connect(self.source_changed)
        self.controller.onButtonsChanged.connect(self.dict_changed)
        self.model.onButtonLocationChanged.connect(self.buttonLocationChanged)
        self.controller.onSelectedCoordinateChanged.connect(self.update_image_draw)
        # self.imagesLayout = QFormLayout()

        self.areaScroller = SwipableListWidget(self, controller, model)

        self.controller.onElementSelectionChanged.connect(self.areaScroller.onSelectionChanged)
        self.areaScroller.onElementClicked.connect(self.controller.elementSelectRequets)
        self.model.onPointAdded.connect(self.areaScroller.addElement)
        self.controller.onButtonsChanged.connect(self.areaScroller.onDictChanged)
        self.controller.onCurrentShowAreaChanged.connect(self.onShowAreaChanged)

        self.areaDescriptionLbl = QLabel()

        self.screensScroller = SwipableListWidget(self, self.controller, self.model)
        self.model.onImageAdded.connect(self.screensScroller.addElement)
        self.screensScroller.onElementClicked.connect(self.controller.imageSelectRequets)
        self.controller.onImageSelectionChanged.connect(self.screensScroller.onSelectionChanged)
        self.controller.onImagesChanged.connect(self.screensScroller.onDictChanged)

        self.screensPathCbox = QComboBox()
        self.image_label = QtWidgets.QLabel()
        self.photo = QLabel()
        self.next = QPushButton()
        self.prev = QPushButton()
        self.cBoxLineWidth = QComboBox()
        self.export_btn = QPushButton()
        self.screen_btn = QPushButton()
        self.add_point_btn = QPushButton()
        self.lblCurrentUILocation = QLabel()
        self.showAreaController = CoordinatesSelector(self, self.controller, self.model)
        self.files = {}
        self.controller.current_image_size = [0, 0]
        self.current_image_resized = [0, 0]
        self.label_photo_fixed_size = [500, 650]
        self.initConnectors()

    def setupUi(self, main_window: QMainWindow):
        main_window.setObjectName("main_window")
        centralwidget = QtWidgets.QWidget(main_window)
        layout_hor = QHBoxLayout()
        lay_vertical_0 = QVBoxLayout()
        lay_vertical_1 = QVBoxLayout()
        lay_vertical_2 = QVBoxLayout()
        self.screensPathCbox.addItems(k for k, v in self.model.screensFolders.items())
        self.screensPathCbox.setFixedHeight(20)
        self.screensPathCbox.setCurrentText(self.model.currentScreensFolder)
        self.screensPathCbox.currentTextChanged.connect(self.controller.requestScreenFolderChange)
        lay_vertical_0.addWidget(self.screensPathCbox)
        self._setNoLayMargins(lay_vertical_0)
        lay_images_description = QHBoxLayout()
        imagesDescriprionLbl = QLabel("Available screenshots.")
        self.screen_btn.setFixedWidth(80)
        lay_images_description.addWidget(imagesDescriprionLbl)
        lay_images_description.addWidget(self.screen_btn)
        lay_images_description.setContentsMargins(0, 5, 0, 5)

        nav_layout = QHBoxLayout()
        nav_layout.setContentsMargins(0, 5, 0, 5)
        nav_layout.addWidget(self.prev)
        nav_layout.addWidget(self.next)

        lay_vertical_0.addLayout(lay_images_description)
        lay_vertical_0.addWidget(self.screensScroller)
        lay_vertical_0.addLayout(nav_layout)
        lay_vertical_0.addWidget(QLabel())

        self.screen_btn.setText("Get screen")

        self.export_btn.setText("save")
        self.export_btn.setFixedWidth(100)
        lay_top = QHBoxLayout()
        lay_top.setAlignment(Qt.AlignCenter)
        lay_top.addWidget(QLabel("Line size:"))
        lay_top.addWidget(self.cBoxLineWidth)
        self.cBoxLineWidth.addItems([str(e) for e in self.model.linePermittedSizes])
        lay_vertical_1.addLayout(lay_top)
        self.cBoxLineWidth.setCurrentText(str(self.model.currentLineWidth))
        self.cBoxLineWidth.currentIndexChanged.connect(self.controller.requestChangeLineWidth)

        self.photo.setText("")
        self.photo.setAlignment(Qt.AlignCenter)
        self.photo.setFixedWidth(self.label_photo_fixed_size[0])
        self.photo.setFixedHeight(self.label_photo_fixed_size[1])
        lay_vertical_1.addWidget(self.photo)

        self.prev.setText("previous")
        self.prev.clicked.connect(self.controller.prevImageSelectRequest)
        self.next.setText("next")
        self.next.clicked.connect(self.controller.nextImageSelectRequest)

        self.lblCurrentUILocation.setFixedHeight(20)
        self.lblCurrentUILocation.setAlignment(Qt.AlignRight)
        lay_vertical_1.addWidget(self.lblCurrentUILocation)
        right_label = QtWidgets.QLabel(self.model.buttons_folder)
        right_label.setFixedHeight(20)
        right_label.setAlignment(Qt.AlignCenter)
        lay_area_description = QHBoxLayout()
        # self._setNoLayMargins(lay_area_description)
        lay_area_description.addWidget(self.areaDescriptionLbl)
        lay_area_description.addWidget(self.add_point_btn)
        lay_area_description.setContentsMargins(0, 5, 0, 5)
        # TODO: insert back right_label later
        lay_vertical_2.addWidget(self.showAreaController)
        lay_vertical_2.addLayout(lay_area_description)
        lay_vertical_2.addWidget(self.areaScroller)
        self.areaScroller.setContentsMargins(0, 0, 0, 0)
        lay_vertical_2.addWidget(self.optionArea)
        self._setNoLayMargins(lay_vertical_2)

        self.add_point_btn.setText("new")
        self.add_point_btn.setFixedWidth(80)
        hor_lay_export = QHBoxLayout()
        hor_lay_export.addStretch()
        hor_lay_export.addWidget(self.export_btn)
        lay_vertical_2.addLayout(hor_lay_export)
        layout_hor.addLayout(lay_vertical_0)
        layout_hor.addLayout(lay_vertical_1)
        layout_hor.addLayout(lay_vertical_2)
        centralwidget.setLayout(layout_hor)
        main_window.setCentralWidget(centralwidget)

    def _setNoLayMargins(self, _lauout):
        _lauout.setContentsMargins(0, 0, 0, 0)
        _lauout.setSpacing(0)

    def onShowAreaChanged(self, new_state: ShowAreaState):
        if new_state == ShowAreaState.Buttons:
            self.areaDescriptionLbl.setText("List of clickable buttons coordinates.")
            self.add_point_btn.setText("add button")
        elif new_state == ShowAreaState.Movements:
            self.areaDescriptionLbl.setText("List of start->end swipes coordinates.")
            self.add_point_btn.setText("add swipe")
        elif new_state == ShowAreaState.FrameCheck:
            self.areaDescriptionLbl.setText("List of static frame states with coordinates.")
            self.add_point_btn.setText("add frame")
        self.areaScroller.onDictChanged(self.controller.dataFromAreaType())

    def sourceChanged(self, new_image_files):
        self.controller.current_image_size = [0, 0]
        self.current_image_resized = [0, 0]

    def initConnectors(self):
        self.export_btn.clicked.connect(self.model.save_data)
        self.screen_btn.clicked.connect(self.acquire_screen)
        self.add_point_btn.clicked.connect(self.controller.requestAddPoint)
        self.controller.onElementSelectionChanged.connect(self.update_image_draw)
        self.controller.onImageSelectionChanged.connect(self.update_image_draw)
        self.model.onLineWidthChanged.connect(self.onLineWidthChanged)

    def clearWidget(self, widget: QWidget):
        widget.setParent(None)

    def onLineWidthChanged(self, new_width):
        self.update_image_draw()

    def acquire_screen(self):
        if self.model.is_device_connected():
            text, ok = QInputDialog.getText(self, "Get name", "Screenshot name:", QLineEdit.Normal, "")
            if ok and text != '':
                self.model.acquire_screen(text)
        else:
            # TODO: show an error message
            pass

    def change_folder(self, newfolder):
        self.screensPathCbox.setText(newfolder)

    def source_changed(self, current_files):
        self.photo.clear()

    def dict_changed(self):
        self.update_image_draw()

    def buttonLocationChanged(self, button_name):
        # new_location = self.model.getPositions(button_name)
        # no update needed because self.dicts contains QLabels and don't hold info about location. So just update the view
        self.update_image_draw()

    def show_btn_location(self, btn_name):
        self.update_image_draw()

    def update_image_draw(self):
        if self.controller.image_selected != "":
            pixmap = self.controller.currentImage.copy()
            if self.controller.dict_selected != "":
                current_locs = []
                coords = self.controller.currentCoordinates
                if self.controller.currentAreaType == ShowAreaState.FrameCheck:
                    coords = self.controller.currentCoordinates['coordinates']
                for i, loc in enumerate(coords):
                    if loc is not None:
                        location = loc.copy()
                        location[0] *= self.controller.current_image_size[0]
                        location[1] *= self.controller.current_image_size[1]
                        if i == self.controller.selectedCoordinateIndex:
                            current_locs = location
                        else:
                            self.DrawLines(pixmap, location, self.model.ui_lines_color_rgb)
                if len(current_locs) > 0:
                    self.DrawLines(pixmap, current_locs, self.model.ui_lines_color_rgb_selected)
            pixmap = pixmap.scaled(self.photo.width(), self.photo.height(), Qt.KeepAspectRatio)
            self.current_image_resized = [pixmap.width(), pixmap.height()]
            self.photo.setPixmap(pixmap)
            self.photo.mousePressEvent = self.getPixelValue

    def getPixelValue(self, event):
        x1 = (event.pos().x() - (self.label_photo_fixed_size[0] - self.current_image_resized[0]) / 2) / \
             self.current_image_resized[0]
        y1 = (event.pos().y()) / self.current_image_resized[1]
        self.controller.requestChangeCoordinate(x1, y1)

    def DrawLines(self, pixmap, location, color):
        painter = QPainter(pixmap)
        [_x, _y] = location
        [w, h] = self.controller.current_image_size
        # Qt.red
        r, g, b = color
        pen = QPen(QBrush(QColor(r, g, b)), self.model.currentLineWidth, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        painter.setPen(pen)
        painter.drawLine(0, _y, w, _y)
        # vertical line
        painter.drawLine(_x, 0, _x, h)
