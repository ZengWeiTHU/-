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

##################################
def getTNumberAndRate(Signal):
    '''
    函数功能：
        求给定脉象信号的准周期T对应的数据点长度TNumber，采样率为200Hz
    输入：
        一段脉象信号向量
    输出：
        1.脉象信号的准周期长度T对应的数据点长度TNumber，int类型
        2.脉象信号的脉率，单位是次数/每分钟，int类型
    '''
    import numpy as np
    from scipy.fftpack import fft

    fs = 200
    Power = abs(fft(Signal))
    Power = Power[0:100]
    loc = np.where(Power == max(Power))[0][0]
    zhuPin = loc / 10  # 主频
    T = 1 / zhuPin
    TNumber = int(round(T * fs))  # 四舍五入
    Rate = int(round(60 * zhuPin))
    return TNumber, Rate


def getRateArray(threePressureSignal):
    '''
    函数功能：
        利用getTNumberAndRate函数计算三压力脉象图的脉率
    输入：
        threePressureSignal：一个三压力脉象图数据，array数据类型
        threePressureSignal[0]:浮压力下脉象信号数据
        threePressureSignal[1]:中压力下脉象信号数据
        threePressureSignal[2]:沉压力下脉象信号数据
    输出：
        1.rateArray:依次由浮取、中取、沉取脉象信号波形的脉率组成的向量
        2.该三压力脉象图的平均脉率
    '''
    fuSignal = threePressureSignal[0]
    zhongSignal = threePressureSignal[1]
    chenSignal = threePressureSignal[2]

    _, rate1 = getTNumberAndRate(fuSignal)
    _, rate2 = getTNumberAndRate(zhongSignal)
    _, rate3 = getTNumberAndRate(chenSignal)

    rateArray = np.array([rate1, rate2, rate3])

    return rateArray, np.mean(rateArray)


def RMS(Signal):
    '''
    函数功能：
        计算给定信号向量的均分根幅度值
    输入：
        一段脉象信号向量
    输出：
        该信号的均方根幅度值
    '''
    import numpy as np

    return np.sqrt(sum([i ** 2 for i in Signal]) / len(Signal))


def getRMSArray(threePressureSignal):
    '''
    函数功能：
        利用RMS函数计算一个三压力脉象数据的均方根幅度趋势向量，以及脉象强度（平均均方根幅度值）
    输入：
        threePressureSignal：一个三压力脉象图数据，array数据类型
        threePressureSignal[0]:浮压力下脉象信号数据
        threePressureSignal[1]:中压力下脉象信号数据
        threePressureSignal[2]:沉压力下脉象信号数据
    输出：
        1.一个array向量，依次包含浮、中、沉取下脉象的均方根幅度值
        2.该三压力脉象图的平均均方根幅度值，代表脉象强度
    '''
    fuSignal = threePressureSignal[0]
    zhongSignal = threePressureSignal[1]
    chenSignal = threePressureSignal[2]

    RMSArray = []
    RMSArray.append(RMS(fuSignal))
    RMSArray.append(RMS(zhongSignal))
    RMSArray.append(RMS(chenSignal))

    return np.array(RMSArray), np.mean(RMSArray)


def classFuOrChen(RMSArray):
    '''
    函数功能：
        通过计算三压力脉象图的均方根幅度值趋势图两端的斜率方向来判断脉象是否是是浮脉、沉脉，还是都不是

    输入：
        RMSArray:一个array向量，依次包含浮、中、沉取下脉象的均方根幅度值
    输出：
        输出为-1,0,1值
        -1:浮脉
        1:沉脉
        0:既不是浮脉也不是沉脉
    '''

    k1 = RMSArray[1] - RMSArray[0]
    k2 = RMSArray[2] - RMSArray[1]
    k = [k1, k2]
    return np.sign(np.sum(np.sign(k)))


def printFuOrChen(RMSArray):
    '''
    函数功能：
        利用RMSArray调用classFuOrChen函数打印判断结果
    输入：
        RMSArray:一个array向量，依次包含浮、中、沉取下脉象的均方根幅度值
    输出：
        无
    '''
    if classFuOrChen(RMSArray) == -1:
        print('浮脉')
        return '浮脉'
    elif classFuOrChen(RMSArray) == 1:
        print('沉脉')
        return '沉脉'
    else:
        print('即不是浮脉也不是沉脉')
        return 0


def classXuOrShi(threePressureSignal, LowerBound=1.0, UpperBound=1.2):
    '''
    函数功能：
        用于判断一个三压力脉象图是实脉还是虚脉
    输入：
        1.threePressureSignal：三压力脉象图向量，依次包含浮取、中取、沉取脉象信号向量；
        2.LowerBound：人为设置的虚脉的脉象强度上限；
        3.UpperBound：人为设置的实脉的脉象强度下限；脉象强度在LowerBound与UpperBound之间为正常脉；
    输出：
        实脉还是虚脉的判断
    '''
    RMSArray, Power = getRMSArray(threePressureSignal)

    if Power < LowerBound:
        return '虚脉'
    elif Power > UpperBound:
        return '实脉'
    else:
        return '平脉'


def TCMPulseRecognition(threePressureSignal, LowerBound=1.0, UpperBound=1.2):
    '''
    函数功能：
        用于判断一个三压力脉象图是迟脉、数脉、浮脉、沉脉、虚脉、实脉、平脉中的哪一种
    输入：
        1.threePressureSignal：三压力脉象图向量，依次包含浮取、中取、沉取脉象信号向量；
        2.LowerBound：人为设置的虚脉的脉象强度上限；
        3.UpperBound：人为设置的实脉的脉象强度下限；脉象强度在LowerBound与UpperBound之间为正常脉；
    输出：
        迟脉、数脉、浮脉、沉脉、虚脉、实脉、平脉中的一种
    '''

    rateArray, rate = getRateArray(threePressureSignal)
    RMSArray, Power = getRMSArray(threePressureSignal)

    if rate <= 70:
        return '迟脉'
    elif rate >= 90:
        return '数脉'
    else:
        if classFuOrChen(RMSArray) == -1:
            return '浮脉'
        elif classFuOrChen(RMSArray) == 1:
            return '沉脉'
        else:
            return classXuOrShi(threePressureSignal, LowerBound=1.0, UpperBound=1.2)


def getResult(PulseData):
    classResult = np.array([0, 0, 0, 0, 0, 0, 0])

    result = TCMPulseRecognition(PulseData, LowerBound=1.0, UpperBound=1.2)
    if result == '迟脉':
        classResult[0] = 1
    elif result == '数脉':
        classResult[1] = 1
    elif result == '浮脉':
        classResult[2] = 1
    elif result == '沉脉':
        classResult[3] = 1
    elif result == '虚脉':
        classResult[4] = 1
    elif result == '实脉':
        classResult[5] = 1
    else:
        classResult[6] = 1

    return classResult
##################################

class plotWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.canvas = FigureCanvas(Figure(tight_layout=True))

        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)

        #############################
        plotData = pd.read_csv(open('chen.csv',encoding= 'utf-8'),header=None).values

        '''
        数据的采样率和采样时间
        '''
        fs = 200
        t_ = 10
        n = fs * t_
        t = np.linspace(0, t_, n)

        ##################################

        self.canvas.axes1 = self.canvas.figure.subplot2grid((5,3),(0,0),rowspan = 2, colspan = 2)
        self.canvas.axes1.plot(t,plotData[0] + 20, label='浮取脉象')
        self.canvas.axes1.plot(t, plotData[1] + 10, label='中取脉象')
        self.canvas.axes1.plot(t, plotData[2] + 0, label='沉取脉象')
        self.canvas.axes1.legend(loc=1)

        self.canvas.axes2 = self.canvas.figure.subplot2grid((5,3),(0,2),rowspan = 2)


        self.canvas.axes3 = self.canvas.figure.subplot2grid((5,3),(2,0),rowspan = 2, colspan = 2)



        self.canvas.axes4 = self.canvas.figure.subplot2grid((5,3),(2,2),rowspan = 2)



        self.canvas.axes5 = self.canvas.figure.subplot2grid((5,3),(4,0),colspan = 3)



        self.canvas.draw()

        self.setLayout(vertical_layout)
