import os
import numpy as np
import json
import logging


def get_matrix_diff(mat1, mat2):
    dist = np.mean(np.abs(mat1 - mat2))
    return dist


def initialize_logging(lvl):
    def addLoggingLevel(levelName, levelNum, methodName=None):
        if not methodName:
            methodName = levelName.lower()
        if hasattr(logging, levelName):
            raise AttributeError('{} already defined in logging module'.format(levelName))
        if hasattr(logging, methodName):
            raise AttributeError('{} already defined in logging module'.format(methodName))
        if hasattr(logging.getLoggerClass(), methodName):
            raise AttributeError('{} already defined in logger class'.format(methodName))
        def logForLevel(self, message, *args, **kwargs):
            if self.isEnabledFor(levelNum):
                self._log(levelNum, message, args, **kwargs)
        def logToRoot(message, *args, **kwargs):
            logging.log(levelNum, message, *args, **kwargs)
        logging.addLevelName(levelNum, levelName)
        setattr(logging, levelName, levelNum)
        setattr(logging.getLoggerClass(), methodName, logForLevel)
        setattr(logging, methodName, logToRoot)

    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p', level=lvl)

    addLoggingLevel('TRACE', logging.DEBUG - 5)


def loadJsonData(path: str)->dict:
    data = {}
    with open(path, 'r') as json_file:
        data = json.load(json_file)
    return data

def saveJsonObject(path: str, o: dict):
    with open(path, 'w') as file:
        file.write(json.dumps(o, indent=2))

def writeToFile(path: str, o: str):
    with open(path, 'w') as file:
        file.write(o)

def saveJsonData_oneIndent(path: str, coords: dict):
    indent = 4
    spaces = ''.join([" " for _ in range(indent)])
    with open(path, 'w') as json_file:
        attrs = []
        for attr, val_Attr in coords.items():
            attrs.append('{}"{}": {}'.format(spaces, attr, json.dumps(val_Attr)))
        json_file.write('{\n' + ',\n'.join(attrs) + '\n}')


def saveJsonData_twoIndent(path: str, data: dict):
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


def readAllSizesFolders(datas_dir) -> dict:
    folders = [f for f in os.listdir(datas_dir) if os.path.isdir(os.path.join(datas_dir, f))]
    dataFolders = {}
    for folder in folders:
        try:
            if 'x' in folder:
                splat = folder.split('x')
                if len(splat) >= 2:
                    w, h = int(splat[0]), int(splat[1])
                    dataFolders[folder] = [w, h]
        except Exception as e:
            logging.error("Got error parsing screen folder %s. skipping" % folder)
    return dataFolders


def buildDataFolder(width, height):
    return "{}x{}".format(width, height)


def getCoordFilePath(dict_name: str, size: tuple = (None, None), sizePath: str = "") -> str:
    """
    Given a dictionary filename and a size e.g. (1080, 2220) OR a sizePath e.h. '1080x2220' return complete filename path
    """
    if sizePath == "" and size == (None, None):
        raise Exception("Unable to get path for coordinate %s. No correct size or path given" % dict_name)
    if size[0] != None and size[1] != None:
        sizePath = buildDataFolder(size[0], size[1])
    return os.path.join("datas", sizePath, "coords", dict_name)
