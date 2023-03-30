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


def getTnum(Signal):
    XPower = abs(fft(Signal))
    XPower = XPower[0:100]
    loc = np.where(XPower == max(XPower))[0][0]
    zhuPin = loc / 10
    T = 1 / zhuPin
    fs = 200
    Tnum = int(round(T * fs))
    return Tnum


def getMaxMin(signal, x):
    maxLoc = int(np.where(signal == max(x))[0][0])
    minLoc = int(np.where(signal == min(x))[0][0])

    return max(x), min(x), maxLoc, minLoc


def getPeakAndTrough(Signal, alpha=0.8):
    X = Signal

    MAX = []
    MIN = []
    MAXLOC = []
    MINLOC = []

    # alpha = 2/3

    Tnum = getTnum(X)
    halfT = int(Tnum / 2)
    a = 0
    b = int((alpha) * Tnum)
    for i in range(int(np.ceil(len(X) / Tnum))):
        x = X[a:b]
        Max, Min, maxLoc, minLoc = getMaxMin(X, x)
        MAX.append(Max)
        MIN.append(Min)
        MAXLOC.append(maxLoc)
        MINLOC.append(minLoc)

        a = maxLoc + halfT
        b = a + int((alpha) * Tnum)

    return MAXLOC, MAX, MINLOC, MIN


def chaZhi(threeX, threeY, length):
    '''
    二阶B样条插值
    '''
    from scipy.interpolate import interp1d

    xx = np.linspace(min(threeX), max(threeX), length)
    f = interp1d(threeX, threeY, kind='quadratic')
    return f(xx)

class plotWidget4(QWidget):
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
        partSignal = partData[0]
        '''
        数据的采样率和采样时间
        '''
        fs = 200
        t_ = 10
        n = fs * t_
        t = np.linspace(0, t_, n)

        MAXLOC, MAX, MINLOC, MIN = getPeakAndTrough(partSignal, alpha=0.8)

        '''
        右下支
        '''

        i = 3
        threeX = [MAXLOC[i - 1], MAXLOC[i - 1] + abs(MAXLOC[i - 1] - MINLOC[i]) * 3 / 4, MINLOC[i], ]
        threeY = [MAX[i - 1], (MAX[i - 1] + np.median(MIN)) * 1 / 2, np.median(MIN), ]
        length = MINLOC[i] - MAXLOC[i - 1]

        chaZhiResult = chaZhi(threeX, threeY, length)

        '''

        左上支
        '''

        i = 3
        threeX_2 = [MINLOC[i], MINLOC[i] + abs(MINLOC[i] - MAXLOC[i + 1]) * 1 / 4, MAXLOC[i + 1]]
        threeY_2 = [np.median(MIN), (MAX[i + 1] + np.median(MIN)) * 1 / 2, MAX[i + 1]]
        length_2 = MAXLOC[i + 1] - MINLOC[i]

        chaZhiResult_2 = chaZhi(threeX_2, threeY_2, length_2)

        import copy
        X = copy.deepcopy(partSignal)
        X[MAXLOC[2]:MINLOC[3]] = chaZhiResult
        X[MINLOC[3]:MAXLOC[4]] = chaZhiResult_2
        ##################################

        self.canvas.axes1.plot(t, X,label='浮取脉象',c='c')
        self.canvas.axes2.plot(t, partData[1],label='中取脉象',c='c')
        self.canvas.axes3.plot(t, partData[2],label='沉取脉象',c='c')

        MAXLOC, MAX, MINLOC, MIN = getPeakAndTrough(X, alpha=0.9)
        self.canvas.axes1.scatter(t[MAXLOC], MAX,c='r')
        self.canvas.axes1.scatter(t[MINLOC], MIN)
        MAXLOC, MAX, MINLOC, MIN = getPeakAndTrough(partData[1], alpha=0.8)
        self.canvas.axes2.scatter(t[MAXLOC], MAX,c='r')
        self.canvas.axes2.scatter(t[MINLOC], MIN)
        MAXLOC, MAX, MINLOC, MIN = getPeakAndTrough(partData[2], alpha=0.8)
        self.canvas.axes3.scatter(t[MAXLOC], MAX,c='r')
        self.canvas.axes3.scatter(t[MINLOC], MIN)


        self.canvas.axes1.legend(loc=1)
        self.canvas.axes2.legend(loc=1)
        self.canvas.axes3.legend(loc=1)

        self.canvas.draw()

        self.setLayout(vertical_layout)
