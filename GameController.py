from PyQt5 import QtWidgets
from GameController.GameControllerView import GameControllerWindow
from GameController.GameControllerModel import GameControllerModel
from GameController.GameControllerController import GameControllerController

if __name__ == "__main__":
    import sys

    print("******************* BOT STARTED ******************")
    print("Stuff is loading, I promise it is. Please wait!")
    print("")
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
