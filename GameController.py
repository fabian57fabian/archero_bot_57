from PyQt5 import QtWidgets
from GameControllerView import GameControllerWindow
from GameControllerModel import GameControllerModel

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    # this is a mockup for data. next time save a configuration file
    model = GameControllerModel()
    ui = GameControllerWindow(model)
    ui.setupUi(MainWindow)
    model.load_data()
    MainWindow.show()
    sys.exit(app.exec_())
