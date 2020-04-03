from PyQt5.QtGui import QPainter, QPen, QBrush, QColor
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QMainWindow, \
    QInputDialog, QLineEdit, QComboBox, QWidget
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
        self.export_btn = QPushButton()
        self.screen_btn = QPushButton()
        self.add_point_btn = QPushButton()
        self.lblCurrentUILocation = QLabel()
        self.showAreaController = CoordinatesSelector(self, self.controller, self.model)
        self.files = {}
        self.current_image_pixmap = []
        self.model.current_image_size = [0, 0]
        self.current_image_resized = [0, 0]
        self.label_photo_fixed_size = [400, 500]
        self.initConnectors()

    def setupUi(self, main_window: QMainWindow):
        main_window.setObjectName("main_window")
        # main_window.resize(800, 600)
        # main_window.setMaximumWidth(800)
        # main_window.setMaximumHeight(600)
        centralwidget = QtWidgets.QWidget(main_window)
        layout_hor = QHBoxLayout()
        lay_vertical_0 = QVBoxLayout()
        # self.screensPathCbox = QtWidgets.QLabel()
        # self.screensPathCbox.setAlignment(Qt.AlignCenter)
        self.screensPathCbox.addItems(k for k, v in self.model.screensFolders.items())
        self.screensPathCbox.setFixedHeight(20)
        self.screensPathCbox.currentTextChanged.connect(self.controller.requestScreenFolderChange)
        lay_vertical_0.addWidget(self.screensPathCbox)

        lay_vertical_0.addWidget(self.screensScroller)

        self.screen_btn.setText("Get screen")
        lay_vertical_0.addWidget(self.screen_btn)

        lay_vertical_1 = QVBoxLayout()
        self.export_btn.setText("export")
        lay_vertical_1.addWidget(self.export_btn)

        # self.photo = QtWidgets.QLabel()
        self.photo.setText("")
        self.photo.setAlignment(Qt.AlignCenter)
        self.photo.setFixedWidth(self.label_photo_fixed_size[0])
        self.photo.setFixedHeight(self.label_photo_fixed_size[1])
        lay_vertical_1.addWidget(self.photo)

        nav_layout = QHBoxLayout()
        self.prev.setText("<-")
        # self.prev.clicked.connect(self.get_prev_image)
        nav_layout.addWidget(self.prev)

        self.next.setText("->")
        # [self.next.clicked.connect(self.get_next_image)
        nav_layout.addWidget(self.next)
        lay_vertical_1.addLayout(nav_layout)

        self.lblCurrentUILocation.setFixedHeight(20)
        self.lblCurrentUILocation.setAlignment(Qt.AlignRight)
        lay_vertical_1.addWidget(self.lblCurrentUILocation)
        lay_vertical_2 = QVBoxLayout()
        right_label = QtWidgets.QLabel(self.model.dict_out_name)
        right_label.setFixedHeight(20)
        right_label.setAlignment(Qt.AlignCenter)
        # TODO: insert back right_label later
        lay_vertical_2.addWidget(self.showAreaController)
        lay_vertical_2.addWidget(self.areaScroller)
        lay_vertical_2.addWidget(self.optionArea)
        lay_vertical_2.setContentsMargins(0, 0, 0, 0)
        self.add_point_btn.setText("Add point")
        lay_vertical_2.addWidget(self.add_point_btn)
        layout_hor.addLayout(lay_vertical_0)
        layout_hor.addLayout(lay_vertical_1)
        layout_hor.addLayout(lay_vertical_2)

        centralwidget.setLayout(layout_hor)
        main_window.setCentralWidget(centralwidget)

    def onShowAreaChanged(self, new_state: ShowAreaState):
        self.areaScroller.onDictChanged(self.controller.dataFromAreaType())

    def sourceChanged(self, new_image_files):
        self.current_image_pixmap = []
        self.model.current_image_size = [0, 0]
        self.current_image_resized = [0, 0]

    def initConnectors(self):
        self.export_btn.clicked.connect(self.model.save_data)
        self.screen_btn.clicked.connect(self.acquire_screen)
        self.add_point_btn.clicked.connect(self.add_point)
        self.controller.onElementSelectionChanged.connect(self.update_image_draw)
        self.controller.onImageSelectionChanged.connect(self.update_image_draw)

    def clearWidget(self, widget: QWidget):
        widget.setParent(None)

    def acquire_screen(self):
        if self.model.is_device_connected():
            text, ok = QInputDialog.getText(self, "Get name", "Screenshot name:", QLineEdit.Normal, "")
            if ok and text != '':
                self.model.acquire_screen(text)
        else:
            # TODO: show an error message
            pass

    def add_point(self):
        text, ok = QInputDialog.getText(self, "Get name", "Point name:", QLineEdit.Normal, "")
        if ok and text != '':
            if text not in self.model.currentDict:
                self.model.add_point(text)
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
            self.current_image_pixmap = pixmap = QtGui.QPixmap(self.controller.getCurrentImageLocation())
            self.model.current_image_size = [pixmap.width(), pixmap.height()]
            if self.controller.dict_selected != "":
                # location = self.model.getPositions(self.controller.dict_selected)
                current_locs = []
                for i, loc in enumerate(self.controller.currentCoordinates):
                    if loc is not None:
                        location = loc.copy()
                        location[0] *= self.model.current_image_size[0]
                        location[1] *= self.model.current_image_size[1]
                        # self.size_label.setText("%d,%d" % (location[0], location[1]))
                        if i == self.controller.selectedCoordinateIndex:
                            current_locs = location
                        else:
                            self.DrawLines(pixmap, location, self.model.ui_lines_color_rgb)
                if len(current_locs) > 0:
                    self.DrawLines(pixmap, current_locs, self.model.ui_lines_color_rgb_selected)
            # self.size_label.setText("%dx%d" % (pixmap.width(), pixmap.height()))
            pixmap = pixmap.scaled(self.photo.width(), self.photo.height(), Qt.KeepAspectRatio)
            self.current_image_resized = [pixmap.width(), pixmap.height()]
            self.photo.setPixmap(pixmap)
            self.photo.mousePressEvent = self.getPixelValue

    def getPixelValue(self, event):
        x1 = (event.pos().x() - (self.label_photo_fixed_size[0] - self.current_image_resized[0]) / 2) / \
             self.current_image_resized[0]
        y1 = (event.pos().y()) / self.current_image_resized[1]
        if self.controller.dict_selected != "":
            self.model.InvokeChangePosition(self.controller.dict_selected, [x1, y1])

    def DrawLines(self, pixmap, location, color):
        painter = QPainter(pixmap)
        [_x, _y] = location
        [w, h] = self.model.current_image_size
        # Qt.red
        r, g, b = color
        pen = QPen(QBrush(QColor(r, g, b)), 10, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        painter.setPen(pen)
        painter.drawLine(0, _y, w, _y)
        # vertical line
        painter.drawLine(_x, 0, _x, h)
