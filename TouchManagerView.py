from functools import partial

from PyQt5.QtGui import QPainter, QPen, QBrush, QColor

from TouchManagerModel import TouchManagerModel
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QSize, pyqtSlot, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QPushButton, QScrollArea, QLabel, QFormLayout, QMainWindow
import os


class TouchManagerWindow(object):

    def __init__(self, model: TouchManagerModel):
        self.model = model
        self.model.onSourceChanged.connect(self.source_changed)
        self.model.onDictionaryTapsChanged.connect(self.dict_changed)
        self.model.onButtonLocationChanged.connect(self.buttonLocationChanged)
        self.imagesLayout = QFormLayout()
        self.dictLayout = QFormLayout()
        self.folder_label = QLabel()
        self.image_label = QtWidgets.QLabel()
        self.photo = QLabel()
        self.next = QPushButton()
        self.prev = QPushButton()
        self.export_btn = QPushButton()
        self.size_label = QLabel()
        self.image_selected = ""
        self.dict_selected = ""
        self.files = {}
        self.dicts = {}
        self.current_image_pixmap = []
        self.current_image_size = [0, 0]
        self.current_image_resized = [0, 0]
        self.label_photo_fixed_size = [400, 500]

    def setupUi(self, main_window: QMainWindow):
        main_window.setObjectName("main_window")
        main_window.resize(800, 600)
        main_window.setMaximumWidth(800)
        main_window.setMaximumHeight(600)
        centralwidget = QtWidgets.QWidget(main_window)
        layout_hor = QHBoxLayout()
        lay_vertical_0 = QVBoxLayout()
        # self.folder_label = QtWidgets.QLabel()
        self.folder_label.setAlignment(Qt.AlignCenter)
        self.folder_label.setText(self.model.images_path)
        self.folder_label.setFixedHeight(20)
        lay_vertical_0.addWidget(self.folder_label)

        # Add images layout
        self.imagesLayout.setSpacing(0)
        self.imagesLayout.setContentsMargins(0, 0, 0, 0)
        scroll = QScrollArea()
        scroll.setLayout(self.imagesLayout)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setFixedWidth(200)
        lay_vertical_0.addWidget(scroll)
        lay_vertical_1 = QVBoxLayout()
        self.image_label.setFixedHeight(20)
        self.image_label.setAlignment(Qt.AlignCenter)
        lay_vertical_1.addWidget(self.image_label)

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

        self.size_label.setFixedHeight(20)
        self.size_label.setAlignment(Qt.AlignRight)
        lay_vertical_1.addWidget(self.size_label)
        lay_vertical_2 = QVBoxLayout()
        right_label = QtWidgets.QLabel(self.model.dict_out_name)
        right_label.setFixedHeight(20)
        right_label.setAlignment(Qt.AlignCenter)
        lay_vertical_2.addWidget(right_label)
        # Add dict Layout
        self.dictLayout.setSpacing(0)
        self.dictLayout.setContentsMargins(0, 0, 0, 0)
        scroll_btns = QScrollArea()
        scroll_btns.setLayout(self.dictLayout)
        scroll_btns.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll_btns.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_btns.setFixedWidth(200)
        lay_vertical_2.addWidget(scroll_btns)

        self.export_btn.setText("export")
        lay_vertical_2.addWidget(self.export_btn)
        layout_hor.addLayout(lay_vertical_0)
        layout_hor.addLayout(lay_vertical_1)
        layout_hor.addLayout(lay_vertical_2)

        centralwidget.setLayout(layout_hor)
        main_window.setCentralWidget(centralwidget)
        self.export_btn.clicked.connect(self.model.save_data)

    def change_folder(self, newfolder):
        self.folder_label.setText(newfolder)

    def source_changed(self, current_files):
        self.imagesLayout.deleteLater()
        self.photo.clear()
        self.image_selected = current_files[0]
        for path in current_files:
            button = QtWidgets.QPushButton(path)
            button.clicked.connect(partial(self.image_clicked, path))
            self.files[path] = button
            self.imagesLayout.addRow(self.files[path])
        self.files[self.image_selected].setStyleSheet(
            "QPushButton { background-color : %s; }" % self.model.ui_color)
        self.update_image_draw()

    # This needs to stay in controller
    def image_clicked(self, path):
        self.files[self.image_selected].setStyleSheet("QPushButton { background-color : white; }")
        self.files[path].setStyleSheet("QPushButton { background-color : %s; }" % self.model.ui_color)
        # Removed because of extra labeling
        # self.image_label.setText(path)
        self.image_selected = path
        self.update_image_draw()

    def dict_changed(self):
        current_dict = self.model.currentDict
        self.dictLayout.deleteLater()
        self.dict_selected = list(current_dict.keys())[0]
        for button_pos in current_dict.items():
            # button = QtWidgets.QPushButton("%s, %dx%d" %(button_pos[0], button_pos[1][0],button_pos[1][1]))
            button = QtWidgets.QPushButton(button_pos[0])
            button.clicked.connect(partial(self.button_pos_clicked, button_pos[0]))
            self.dicts[button_pos[0]] = button
            self.dictLayout.addRow(self.dicts[button_pos[0]])
        self.dicts[self.dict_selected].setStyleSheet(
            "QPushButton { background-color : %s; }" % self.model.ui_color)
        self.update_image_draw()

    def buttonLocationChanged(self, button_name):
        # new_location = self.model.getPositions(button_name)
        # no update needed because self.dicts contains QLabels and don't hold info about location. So just update the view
        self.update_image_draw()

    # This needs to stay in controller
    def button_pos_clicked(self, btn_name):
        self.dicts[self.dict_selected].setStyleSheet("QPushButton { background-color : white; }")
        self.dicts[btn_name].setStyleSheet("QPushButton { background-color : %s; }" % self.model.ui_color)
        self.show_btn_location(btn_name)
        pass

    def show_btn_location(self, btn_name):
        self.dict_selected = btn_name
        self.update_image_draw()

    def update_image_draw(self):
        if self.image_selected != "":
            path_complete = os.path.join(self.model.images_path, self.image_selected)
            self.current_image_pixmap = pixmap = QtGui.QPixmap(path_complete)
            self.current_image_size = [pixmap.width(), pixmap.height()]
            if self.dict_selected != "":
                location = self.model.getPositions(self.dict_selected)
                if location is not None:
                    location[0] *= self.current_image_size[0]
                    location[1] *= self.current_image_size[1]
                    self.DrawLines(pixmap, location)
            self.size_label.setText("%dx%d" % (pixmap.width(), pixmap.height()))
            pixmap = pixmap.scaled(self.photo.width(), self.photo.height(), Qt.KeepAspectRatio)
            self.current_image_resized = [pixmap.width(), pixmap.height()]
            self.photo.setPixmap(pixmap)
            self.photo.mousePressEvent = self.getPixelValue

    def getPixelValue(self, event):
        x = (event.pos().x() - (self.label_photo_fixed_size[0] - self.current_image_resized[0]) / 2) / \
            self.current_image_resized[0]
        y = (event.pos().y()) / self.current_image_resized[1]
        if self.dict_selected != "":
            self.model.InvokeChangePosition(self.dict_selected, [x, y])

    def DrawLines(self, pixmap, location):
        painter = QPainter(pixmap)
        [_x, _y] = location
        [w, h] = self.current_image_size
        # Qt.red
        r, g, b = self.model.ui_lines_color_rgb
        pen = QPen(QBrush(QColor(r, g, b)), 10, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        painter.setPen(pen)
        painter.drawLine(0, _y, w, _y)
        # vertical line
        painter.drawLine(_x, 0, _x, h)


"""
    def get_prev_image(self):
        prev = ""
        for i, elem in enumerate(self.files.items()):
            n, _ = elem
            if n == self.selected and prev is not "":
                self.show_image(prev)
                break
            else:
                prev = n

    def get_next_image(self):
        found = False
        for i, elem in enumerate(self.files.items()):
            n, _ = elem
            if found:
                self.show_image(n)
                break
            if n == self.selected:
                found = True
"""
