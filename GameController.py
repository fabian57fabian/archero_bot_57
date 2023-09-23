import os
import logging
from src.Utils import initialize_logging
from src import __version__
import sys
from PyQt5 import QtWidgets
from GameController.GameControllerView import GameControllerWindow
from GameController.GameControllerModel import GameControllerModel
from GameController.GameControllerController import GameControllerController

if __name__ == "__main__":
    lvl = logging.DEBUG # logging.DEBUG
    initialize_logging(lvl)
    logging.info(f"******** ARCHERO BOT v{__version__} STARTED ********")
    logging.info("Stuff is loading, promise it is. Please wait")
    logging.info("")
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    MainWindow.setWindowTitle("Game Controller")
    data_path = os.path.join(os.getcwd(), "datas")
    model = GameControllerModel(data_path)
    controller = GameControllerController(model)
    ui = GameControllerWindow(model, controller)
    ui.setupUi(MainWindow)
    model.load_data()
    model.check_for_updates()
    MainWindow.show()
    result = app.exec_()
    model.requestClose()
    sys.exit(result)
