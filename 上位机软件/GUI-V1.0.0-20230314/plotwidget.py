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

partData = pd.read_csv(open('局部异常.csv',encoding= 'utf-8'),header=None).values

'''
数据的采样率和采样时间
'''
fs = 200
t_ = 10
n = fs*t_
t = np.linspace(0,t_,n)

y1 = np.sin(2*np.pi*0.1*t)+np.sin(2*np.pi*0.05*t)+np.sin(2*np.pi*0.01*t)+np.cos(2*np.pi*0.2*t)
y2 = np.sin(2*np.pi*0.2*t)+np.cos(2*np.pi*0.1*t)
y3 = np.sin(2*np.pi*0.3*t)+np.cos(2*np.pi*0.05*t)
##################################

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
        partData = pd.read_csv(open('局部异常.csv', encoding='utf-8'), header=None).values

        '''
        数据的采样率和采样时间
        '''
        fs = 200
        t_ = 10
        n = fs * t_
        t = np.linspace(0, t_, n)

        y1 = np.sin(2 * np.pi * 0.1 * t) + np.sin(2 * np.pi * 0.05 * t) + np.sin(2 * np.pi * 0.01 * t) + np.cos(
            2 * np.pi * 0.2 * t)
        y2 = np.sin(2 * np.pi * 0.2 * t) + np.cos(2 * np.pi * 0.1 * t)
        y3 = np.sin(2 * np.pi * 0.3 * t) + np.cos(2 * np.pi * 0.05 * t)
        ##################################

        self.canvas.axes1.plot(t, partData[0] + y1)
        self.canvas.axes2.plot(t, partData[1] + y2)
        self.canvas.axes3.plot(t, partData[2] + y3)

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
