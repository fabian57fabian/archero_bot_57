from PyQt5 import QtWidgets
from GameController.GameControllerView import GameControllerWindow
from GameController.GameControllerModel import GameControllerModel

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    model = GameControllerModel()
    ui = GameControllerWindow(model)
    model.load_data()
    ui.show()
    sys.exit(app.exec_())
