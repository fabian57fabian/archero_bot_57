from functools import partial

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QSize, pyqtSlot
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget, QScrollArea, QSizePolicy, QFormLayout
import os


class Ui_MainWindow(object):

    def __init__(self, path, btns):
        self.images_path = path
        self.photo = None
        self.export_btn = None
        self.size_label = None
        self.current_coordinates = btns
        self.selected = ""
        self.files = {}
        self.selected_color = "cyan"


    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)

        centralwidget = QtWidgets.QWidget(MainWindow)
        layout_hor = QHBoxLayout()
        lay_vertical_0 = QVBoxLayout()
        folder_label = QtWidgets.QLabel(self.images_path)
        folder_label.setFixedHeight(20)
        lay_vertical_0.addWidget(folder_label)
        # scroll = QScrollArea()
        formLayout = QFormLayout()
        formLayout.setSpacing(0)
        formLayout.setContentsMargins(0, 0, 0, 0)
        # formLayout.setContentsMargins(10, 5, 20, 0)
        first = True
        for path in sorted(os.listdir(self.images_path)):
            if first:
                self.selected = path
                first = False
            button = QtWidgets.QPushButton(path)
            button.clicked.connect(partial(self.show_image, path))
            self.files[path] = button
            formLayout.addRow(self.files[path])
        self.files[self.selected].setStyleSheet(
            "QPushButton { background-color : %s; }" % (self.selected_color))
        scroll = QScrollArea()
        scroll.setLayout(formLayout)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setFixedWidth(200)
        lay_vertical_0.addWidget(scroll)
        lay_vertical_1 = QVBoxLayout()
        main_label = QtWidgets.QLabel(self.selected)
        main_label.setFixedHeight(20)
        main_label.setAlignment(Qt.AlignCenter)
        lay_vertical_1.addWidget(main_label)

        self.photo = QtWidgets.QLabel()
        self.photo.setText("")
        # pixmap = QtGui.QPixmap('screens/samsung_s8+/boss_fight.jpg')
        # pixmap = pixmap.scaled(self.photo.width(), self.photo.height(), Qt.KeepAspectRatio)
        # self.photo.setPixmap(pixmap)
        self.photo.setAlignment(Qt.AlignCenter)
        # self.photo.setScaledContents(True)
        lay_vertical_1.addWidget(self.photo)

        nav_layout = QHBoxLayout()
        prev = QtWidgets.QPushButton()
        prev.setText("<-")
        prev.clicked.connect(self.get_prev_image)
        nav_layout.addWidget(prev)
        next = QtWidgets.QPushButton()
        next.setText("->")
        next.clicked.connect(self.get_next_image)
        nav_layout.addWidget(next)
        lay_vertical_1.addLayout(nav_layout)

        self.size_label = QtWidgets.QLabel()
        self.size_label.setFixedHeight(20)
        self.size_label.setAlignment(Qt.AlignRight)
        lay_vertical_1.addWidget(self.size_label)
        lay_vertical_2 = QVBoxLayout()
        right_label = QtWidgets.QLabel(self.selected)
        right_label.setFixedHeight(20)
        right_label.setAlignment(Qt.AlignRight)
        lay_vertical_2.addWidget(right_label)
        scroll_btns = QScrollArea()
        scroll_btns.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll_btns.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_btns.setFixedWidth(200)
        lay_vertical_2.addWidget(scroll_btns)

        self.export_btn = QtWidgets.QPushButton()
        self.export_btn.setText("export")
        lay_vertical_2.addWidget(self.export_btn)
        layout_hor.addLayout(lay_vertical_0)
        layout_hor.addLayout(lay_vertical_1)
        layout_hor.addLayout(lay_vertical_2)

        self.show_image(self.selected)

        centralwidget.setLayout(layout_hor)
        MainWindow.setCentralWidget(centralwidget)
        self.export_btn.clicked.connect(self.save_data)

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

    def save_data(self):
        with open('data.py', "w") as outfile:
            outfile.write("def getButtons():\n")
            outfile.write("    buttons = {\n")
            for d in self.current_coordinates.items():
                n, xy = d
                outfile.write("        '%s': [%d, %d],\n" % (n, int(xy[0]), int(xy[1])))
            outfile.write("    }")

    def show_image(self, path):
        self.files[self.selected].setStyleSheet("QPushButton { background-color : white; }")
        path_complete = os.path.join(self.images_path, path)
        pixmap = QtGui.QPixmap(path_complete)
        pixmap = pixmap.scaled(self.photo.width(), self.photo.height(), Qt.KeepAspectRatio)
        self.size_label.setText("%dx%d" % (pixmap.width(), pixmap.height()))
        self.photo.setPixmap(pixmap)
        self.files[path].setStyleSheet("QPushButton { background-color : %s; }" % self.selected_color)
        self.selected = path


def load_mockup():
    return "screens/samsung_s8+", {'pause': [20, 20], 'start': [540, 1700]}


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    # this is a mockup for data. next time save a configuration file
    path, buttons = load_mockup()
    ui = Ui_MainWindow(path, buttons)
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
