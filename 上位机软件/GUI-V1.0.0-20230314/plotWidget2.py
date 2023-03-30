# ------------------------------------------------- -----
# -------------------- plotWidget2.py --------------------
# -------------------------------------------------- ----
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

from mainwindow import Ui_mainWindow
from PyQt5 import QtWidgets
import sys
import os
from PyQt5.QtCore import *

class plotWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.canvasFu = FigureCanvas(Figure())
        self.canvasZhong = FigureCanvas(Figure())
        self.canvasChen = FigureCanvas(Figure())

        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvasFu)
        # vertical_layout.addWidget(self.canvasZhong)
        # vertical_layout.addWidget(self.canvasChen)

        self.canvasFu.axes = self.canvas.figure.add_subplot(111)
        self.canvasZhong.axes = self.canvas.figure.add_subplot(111)
        self.canvasChen.axes = self.canvas.figure.add_subplot(111)

        self.setLayout(vertical_layout)

    def plotShow(self):

        t = np.linspace(0, 10, 2000)
        y = np.cos(2 * np.pi * 20 * t)

        self.canvasFu.axes.plot(t, y)
        self.canvasFu.draw()

class MatplotlibWidget(Ui_mainWindow):

    def __init__(self):
        Ui_mainWindow.__init__(self)

    def plotShow(self):

        t = np.linspace(0, 10, 2000)
        y = np.cos(2 * np.pi * 20 * t)

        self.plotWidget.canvasFu.axes.plot(t, y)
        self.plotWidget.canvasFu.draw()



app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_mainWindow()
ui.setupUi(MainWindow)

ui.plotW

MainWindow.show()
sys.exit(app.exec_())