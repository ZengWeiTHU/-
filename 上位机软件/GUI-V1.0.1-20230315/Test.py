import sys
from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QLabel, QApplication)
from PyQt5.QtGui import QPixmap


class Example (QWidget):
    def __init__(self):
        super ().__init__()
        self.initUI ()

    def initUI(self):
        lbl = QLabel(self)
        pixmap = QPixmap('chen.png')  # 按指定路径找到图片
        lbl.setPixmap(pixmap)  # 在label上显示图片
        lbl.setScaledContents (True)  # 让图片自适应label大小
        hbox.addWidget(lbl)

        self.setLayout(hbox)
        self.move (300, 200)
        self.setWindowTitle ('pic')
        self.show ()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example ()
    sys.exit (app.exec_())
