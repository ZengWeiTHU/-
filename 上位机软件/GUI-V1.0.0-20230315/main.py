from mainwindow import Ui_mainWindow
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
import sys
import os


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_mainWindow()
    ui.setupUi(MainWindow)

    MainWindow.show()
    sys.exit(app.exec_())