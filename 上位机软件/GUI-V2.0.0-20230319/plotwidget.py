# ------------------------------------------------- -----
# -------------------- mplwidget.py --------------------
# -------------------------------------------------- ----
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

###############################
import os
import csv
import copy
import numpy as np
import pandas as pd
from scipy import signal
from scipy.fftpack import fft,ifft
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'SimHei'
plt.rcParams['axes.unicode_minus'] = False


def getFileName(Path):
    csvFiles = []
    for dirname, _, filenames in os.walk(Path):
        for filename in filenames:
            fullPath = os.path.join(dirname, filename)
            if filename.endswith("csv"):
                csvFiles.append(fullPath)

    return csvFiles

class plotWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.canvas = FigureCanvas(Figure(tight_layout=True))

        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)

        self.canvas.axes1 = self.canvas.figure.add_subplot(311)
        self.canvas.axes2 = self.canvas.figure.add_subplot(312)
        self.canvas.axes3 = self.canvas.figure.add_subplot(313)

        #############################
        Path = 'csv1'
        fileNames = getFileName(Path)
        fu = pd.read_csv(open(fileNames[0], encoding='utf-8'), header=None)[0].values
        zhong = pd.read_csv(open(fileNames[1], encoding='utf-8'), header=None)[0].values
        chen = pd.read_csv(open(fileNames[2], encoding='utf-8'), header=None)[0].values

        fu = -fu[1000:3000]
        zhong = -zhong[1000:3000]
        chen = -chen[4000:6000]

        T = 10
        t = np.linspace(0, T, T * 200)
        ##################################

        self.canvas.axes1.plot(t, fu)
        self.canvas.axes2.plot(t, zhong)
        self.canvas.axes3.plot(t, chen)

        self.canvas.axes1.set_title('浮取脉象', fontsize=20)
        self.canvas.axes2.set_title('中取脉象', fontsize=20)
        self.canvas.axes3.set_title('沉取脉象', fontsize=20)

        self.canvas.axes1.set_xlabel('时间/秒', fontsize=10)
        self.canvas.axes1.set_ylabel('幅度值', fontsize=10)

        self.canvas.axes2.set_xlabel('时间/秒', fontsize=10)
        self.canvas.axes2.set_ylabel('幅度值', fontsize=10)

        self.canvas.axes3.set_xlabel('时间/秒', fontsize=10)
        self.canvas.axes3.set_ylabel('幅度值', fontsize=10)

        self.canvas.axes1.grid()
        self.canvas.axes2.grid()
        self.canvas.axes3.grid()

        self.canvas.draw()

        self.setLayout(vertical_layout)
