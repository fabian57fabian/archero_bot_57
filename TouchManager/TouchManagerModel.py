import json
import os
from PyQt5.QtCore import pyqtSignal, QObject
from pure_adb_connector import adb_screen, get_device_id


class TouchManagerModel(QObject):
    onSourceChanged = pyqtSignal(dict)
    onDictionaryTapsChanged = pyqtSignal(dict)
    onDictionaryMovementsChanged = pyqtSignal(dict)
    onDictionaryFrameChecksChanged = pyqtSignal(dict)
    onButtonLocationChanged = pyqtSignal(str)
    onImageSelected = pyqtSignal()
    onImageAdded = pyqtSignal(str)
    onPointAdded = pyqtSignal(str)

    def __init__(self):
        super(QObject, self).__init__()
        # Default path for screens
        self.screens_folder = "screens"
        self.currentScreensFolder = "1080x2220"
        self.manage_default_currentScreensPath()
        self.data_pack = 'datas'
        self.dict_out_name = 'data.py'
        self.dict_movements_out_name = 'movements.json'
        self.dict_framechecks_out_name = 'static_coords.json'
        self.dict_path = "data.py"
        self.ui_color = "cyan"
        self.ui_lines_color_rgb = (0, 255, 0)
        self.ui_lines_color_rgb_selected = (255, 0, 255)
        self.current_image_size = [0, 0]
        self.currentFiles = {}
        self.currentDict = {}
        self.currentMovements = {}
        self.currentFrameChecks = {}
        self.screensFolders = {}
        self.loadScreenshotsFolders()

    def currentScreensPath(self):
        return os.path.join(self.screens_folder, self.currentScreensFolder)

    def loadScreenshotsFolders(self):
        self.screensFolders = {}
        for folder in os.listdir(self.screens_folder):
            try:
                if 'x' in folder:
                    splat = folder.split('x')
                    if len(splat) >= 2:
                        w, h = int(splat[0]), int(splat[1])
                        self.screensFolders[folder] = [w, h]
            except Exception as e:
                print("Got error parsing screen folder %s. skipping" % folder)

    def loadCurrentImage(self):
        path = ""
        return path

    def is_device_connected(self):
        return get_device_id() is not None

    def acquire_screen(self, name):
        filename = name + ".png"
        adb_screen(os.path.join(self.currentScreensPath(), filename))
        self.currentFiles = {k: None for k in self.loadImagesFromSource(self.currentScreensPath())}
        self.onImageAdded.emit(filename)

    def add_point(self, point_name):
        self.currentDict[point_name] = [.5, .5]
        self.onPointAdded.emit(point_name)

    def manage_default_currentScreensPath(self):
        if not os.path.exists(self.currentScreensPath()):
            os.makedirs(self.currentScreensPath())

    def getPositions(self, dict_button):
        return self.currentDict[dict_button].copy() if dict_button in self.currentDict else None

    def InvokeChangePosition(self, dict_button, new_location):
        if dict_button in self.currentDict:
            self.currentDict[dict_button] = new_location
            self.onButtonLocationChanged.emit(dict_button)

    def load_data(self):
        self.loadScreens()
        self.load_buttons()
        self.loadMovements()
        self.loadScreenCheck()

    def loadScreens(self):
        self.currentFiles = {k: None for k in self.loadImagesFromSource(self.currentScreensPath())}
        self.onSourceChanged.emit(self.currentFiles)

    def load_buttons(self):
        self.currentDict = self.loadDictionaryFromSource(self.dict_out_name)
        self.onDictionaryTapsChanged.emit(self.currentDict)

    def loadMovements(self):
        self.currentMovements = self.loadJsonData(self.dict_movements_out_name)
        self.onDictionaryMovementsChanged.emit(self.currentMovements)

    def loadScreenCheck(self):
        self.currentFrameChecks = self.loadJsonData(self.dict_framechecks_out_name)
        self.onDictionaryFrameChecksChanged.emit(self.currentFrameChecks)

    def loadJsonData(self, filePath: str):
        data = {}
        with open(os.path.join(self.data_pack, filePath), 'r') as json_file:
            data = json.load(json_file)
        return data

    def changeScreensFolder(self, new_folder):
        if new_folder in self.screensFolders.keys():
            self.currentScreensFolder = new_folder
            self.loadScreens()

    def loadImagesFromSource(self, img_path):
        return [file for file in sorted(os.listdir(img_path))]  # if file.endswith(".jpg")]

    def loadDictionaryFromSource(self, dict_path):
        method = self.import_method(self.data_pack, dict_path, "getButtons")
        return method()

    def import_method(self, folder, file, name):
        """
        loads a method from file (.py) inside a folder
        :param folder:
        :param file:
        :param name:
        :return:
        """
        module = folder + "." + file[:-3]
        module = __import__(module, fromlist=[name])
        return getattr(module, name)

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
        self.write_dict_file(os.path.join(self.data_pack, self.dict_out_name), self.currentDict)
        self.saveJsonSimple(os.path.join(self.data_pack, self.dict_movements_out_name), self.currentMovements)
        self._saveStaticCoords(os.path.join(self.data_pack, self.dict_movements_out_name), self.currentFrameChecks)

    # TODO: Inported from game_screen_connector. Consider to move in a utils folder
    def _saveStaticCoords(self, path, data: dict):
        indent = 4
        spaces = ''.join([" " for _ in range(indent)])
        with open(path, 'w') as json_file:
            # json_file.write("{\n")
            main_attrs = []
            for coord, value in data.items():
                attrs = []
                for attr, val_Attr in value.items():
                    attrs.append('{}"{}": {}'.format(spaces + spaces, attr, json.dumps(val_Attr)))
                formatted_attrs = ',\n'.join(attrs)
                main_attrs.append(
                    '{}"{}":{}{}'.format(spaces, coord, '{\n', formatted_attrs + '\n' + spaces + '}'))
            json_file.write('{\n' + ',\n'.join(main_attrs) + '\n}')
            # json_file.write("}")
        print("Static coords saved")

    def saveJsonSimple(self, path, data: dict):
        with open(path, 'w') as fp:
            json.dump(data, fp)
