from CaveDungeonEngine import CaveEngine
import sys


def get_start_lvl_from_args():
    start_lvl = 0
    if len(sys.argv) > 1:
        try:
            arg = sys.argv[1]
            start_lvl = int(arg)
            if start_lvl < 0 or start_lvl > 20:
                print("Given starting level is not a valid start level in [0,20]. Starting from zero")
                start_lvl = 0
        except:
            print("Given starting level is not a valid start level. Starting from zero")
            start_lvl = 0
    return start_lvl


while True:
    answer = input("Do you want to use the interface? (y/n):")
    if answer == 'y' or answer == 'yes':
        from PyQt5 import QtWidgets
        from GameController.GameControllerView import GameControllerWindow
        from GameController.GameControllerModel import GameControllerModel
        from GameController.GameControllerController import GameControllerController

        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        model = GameControllerModel()
        controller = GameControllerController(model)
        ui = GameControllerWindow(model, controller)
        ui.setupUi(MainWindow)
        model.load_data()
        MainWindow.show()
        result = app.exec_()
        model.requestClose()
        sys.exit(result)
    else:
        print(
            "Please use GameController.py interface. This script is disabled.\nOn Windows: double-click on GameController.py\nOn Linux: open the terminal and execute 'python3 GameController.py'")
