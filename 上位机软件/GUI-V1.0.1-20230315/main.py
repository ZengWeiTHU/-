from mainwindow import Ui_mainWindow
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
import sys
import os
from PyQt5.QtGui import QPixmap

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_mainWindow()
    ui.setupUi(MainWindow)

    pixmap = QPixmap('chen.png')  # 按指定路径找到图片
    ui.label.setPixmap(pixmap)
    ui.label.setScaledContents (True)

    MainWindow.show()
    sys.exit(app.exec_())