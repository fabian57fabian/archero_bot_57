import os
from PyQt5 import QtWidgets
from TouchManager.TouchManagerView import TouchManagerWindow
from TouchManager.TouchManagerModel import TouchManagerModel
from TouchManager.TouchManagerController import TouchManagerController

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    MainWindow.setWindowTitle("Touch Manager")
    data_path = os.path.join(os.getcwd(), "datas")
    model = TouchManagerModel(data_path, connect_archero_now=False)
    controller = TouchManagerController(model)
    ui = TouchManagerWindow(controller, model)
    ui.setupUi(MainWindow)
    model.load_data()
    MainWindow.show()
    sys.exit(app.exec_())
