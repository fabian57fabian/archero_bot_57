from PyQt5 import QtWidgets
from GameController.GameControllerView import GameControllerWindow
from GameController.GameControllerModel import GameControllerModel
from GameController.GameControllerController import GameControllerController

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    model = GameControllerModel()
    controller = GameControllerController(model)
    ui = GameControllerWindow(model, controller)
    model.load_data()
    ui.show()
    sys.exit(app.exec_())
