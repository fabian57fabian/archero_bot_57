import logging
from Utils import initialize_logging
import sys
from PyQt5 import QtWidgets
from GameController.GameControllerView import GameControllerWindow
from GameController.GameControllerModel import GameControllerModel
from GameController.GameControllerController import GameControllerController

if __name__ == "__main__":
    lvl = logging.INFO # logging.DEBUG
    initialize_logging(lvl)
    logging.info("******************* BOT STARTED ******************")
    logging.info("Stuff is loading, I promise it is. Please wait!")
    logging.info("")
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    MainWindow.setWindowTitle("Game Controller")
    model = GameControllerModel()
    controller = GameControllerController(model)
    ui = GameControllerWindow(model, controller)
    ui.setupUi(MainWindow)
    model.load_data()
    model.check_for_updates()
    MainWindow.show()
    result = app.exec_()
    model.requestClose()
    sys.exit(result)
