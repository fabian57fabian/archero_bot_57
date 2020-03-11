import os
from PyQt5.QtCore import pyqtSignal, QObject
from adb_connector import adb_screen, get_device_id


class TouchManagerModel(QObject):
    onSourceChanged = pyqtSignal(list)
    onDictionaryTapsChanged = pyqtSignal(dict)
    onButtonLocationChanged = pyqtSignal(str)
    onImageSelected = pyqtSignal()
    onImageAdded = pyqtSignal(str)
    onPointAdded = pyqtSignal(str)

    def __init__(self):
        super(TouchManagerModel, self).__init__()
        # Default path for screens
        self.images_path = "screens/samsung_s8+"
        self.manage_default_images_path()
        self.dict_out_name = 'data.py'
        self.dict_path = "../default_dict.py"
        self.manage_default_dict_path()
        self.ui_color = "cyan"
        self.ui_lines_color_rgb = (255, 0, 255)
        self.currentFiles = []
        self.currentDict = {}

    def is_device_connected(self):
        return get_device_id() is not None

    def acquire_screen(self, name):
        filename = name + ".png"
        adb_screen(os.path.join(self.images_path, filename))
        self.currentFiles = self.loadImagesFromSource(self.images_path)
        self.onImageAdded.emit(filename)

    def add_point(self, point_name):
        self.currentDict[point_name] = [.5, .5]
        self.onPointAdded.emit(point_name)

    def manage_default_images_path(self):
        if not os.path.exists(self.images_path):
            os.makedirs(self.images_path)

    def manage_default_dict_path(self):
        if not os.path.exists(self.dict_path):
            self.write_dict_file(self.dict_path, {'pause': [20 / 1080, 20 / 2220],
                                                  'start': [540 / 1080.0, 1700 / 2220.0],
                                                  'collect': [330 / 1080.0, 1490 / 2220.0],
                                                  'ability_left': [210 / 1080.0, 1500 / 2220.0],
                                                  'ability_center': [540 / 1080.0, 1500 / 2220.0],
                                                  'ability_right': [870 / 1080.0, 1500 / 2220.0],
                                                  'spin_wheel_back': [85 / 1080.0, 2140 / 2220.0],
                                                  'lucky_wheel_start': [540 / 1080.0, 1675 / 2220.0],
                                                  'ability_daemon_reject': [175 / 1080.0, 1790 / 2220.0],
                                                  'click_neutral_away': [998 / 1080.0, 2102 / 2220.0],
                                                  'lock_swap_unlock': [0.501235, 0.504569],
                                                  'lock_swap_unlock_up': [0.501235, 0.354569],
                                                  'close_end': [540 / 1080, 1993 / 2220], })

    def getPositions(self, dict_button):
        return self.currentDict[dict_button].copy() if dict_button in self.currentDict else None

    def InvokeChangePosition(self, dict_button, new_location):
        if dict_button in self.currentDict:
            self.currentDict[dict_button] = new_location
            self.onButtonLocationChanged.emit(dict_button)

    def load_data(self):
        self.currentFiles = self.loadImagesFromSource(self.images_path)
        self.onSourceChanged.emit(self.currentFiles)
        self.currentDict = self.loadDictionaryFromSource(self.dict_path)
        self.onDictionaryTapsChanged.emit(self.currentDict)

    def loadImagesFromSource(self, img_path):
        return [file for file in sorted(os.listdir(self.images_path))]  # if file.endswith(".jpg")]

    def loadDictionaryFromSource(self, dict_path):
        from default_dict import getButtons
        return getButtons()

    def write_dict_file(self, path, dict_data):
        with open(path, "w") as outfile:
            outfile.write("def getButtons():\n")
            outfile.write("    buttons = {\n")
            for d in dict_data.items():
                n, xy = d
                outfile.write("        '%s': [%f, %f],\n" % (n, xy[0], xy[1]))
            outfile.write("    }\n")
            outfile.write("    return buttons")

    def save_data(self):
        self.write_dict_file(self.dict_out_name, self.currentDict)
