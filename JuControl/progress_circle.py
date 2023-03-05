#!/usr/bin/env python3
# -*- coding: utf-8 -*-

r"""
"""

__author__ = "Jiang Jun"

import sys

from PySide2 import QtWidgets
from PySide2.QtWidgets import QWidget, QProgressBar
from PySide2.QtCore import Qt, QTimer, Signal
from PySide2.QtGui import QFont, QPainter, QMovie


class ProgressBar(QWidget):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.initUI()

        # self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        # self.setWindowFlags(Qt.WindowStaysOnTopHint)
        # self.setWindowFlags(Qt.SplashScreen | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

    def initUI(self):
        self.resize(350, 30)
        # 载入进度条控件
        self.pgb = QProgressBar(self)
        # self.pgb.move(50, 50)
        self.pgb.resize(350, 30)
        self.pgb.setStyleSheet(
            "QProgressBar { border: 2px solid grey; border-radius: 5px; background-color: #FFFFFF; text-align: center;}QProgressBar::chunk {background:QLinearGradient(x1:0,y1:0,x2:2,y2:0,stop:0 #666699,stop:1  #DB7093); }")
        font = QFont()
        font.setBold(True)
        font.setWeight(30)
        self.pgb.setFont(font)
        # 设置一个值表示进度条的当前进度
        self.pv = 0
        # 申明一个时钟控件
        # 设置进度条的范围
        self.pgb.setMinimum(0)
        self.pgb.setMaximum(100)
        self.pgb.setValue(self.pv)
        ## 设置进度条文字格式
        self.pgb.setFormat('{}  %p%'.format(self.name, self.pgb.value() - self.pgb.minimum()))
        # 加载pushbutton
        self.timer1 = QTimer()
        self.timer1.timeout.connect(self.update_num)
        # self.timer1.start(200)

    def show_(self):
        # print('start')
        self.pv = 0
        self.show()
        self.timer1.start(100)

    def close_(self):
        # print('stop')
        self.close()
        # if self.timer1.isActive():
        self.timer1.stop()
        self.pv = 0

    def update_num(self):
        # print('self.name', self.name, self.pgb.value(), self.pgb.minimum())
        self.pv += 1
        self.pgb.setValue(self.pv)
        self.pgb.setFormat('{}  %p%'.format(self.name, self.pgb.value() - 0))

    def paintEvent(self, event):
        # 圆角
        pat2 = QPainter(self)
        pat2.setRenderHint(pat2.Antialiasing)  # 抗锯齿
        pat2.setBrush(Qt.white)
        pat2.setPen(Qt.transparent)
        rect = self.rect()
        pat2.drawRoundedRect(rect, 15, 15)


class Loading_in(QtWidgets.QWidget):
    Progress_close = Signal()

    def __init__(self):
        super(Loading_in, self).__init__()
        self.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        # self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.movie = QMovie("./loading.gif")
        self.label.setMovie(self.movie)
        self.movie.start()
        self.label.setScaledContents(True)

    def show_(self):
        print(21321)
        self.show()

    def close_(self):
        self.close()
#
#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     mytask = ProgressBar('加载中')
#     mytask.show_()
#     app.exec_()

