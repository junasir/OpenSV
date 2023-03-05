#!/usr/bin/env python3
# -*- coding: utf-8 -*-

r"""
"""

__author__ = "Jiangjun"

import sys

from PySide2.QtCore import Signal
from PySide2.QtWidgets import QVBoxLayout, QWidget, QApplication, QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy, \
    QLabel


class JuBottomWidget(QWidget):
    press_log = Signal(int, int)

    def __init__(self, parent=None):
        super(JuBottomWidget, self).__init__(parent)
        self.setFixedHeight(20)
        v = QVBoxLayout(self)
        v.setObjectName("---")
        v.setContentsMargins(0, 0, 0, 0)
        # label = QLabel(self)
        # label.setObjectName("=")
        # label.setFixedHeight(1)
        # label.setStyleSheet(u"background-color:#515151;border: none;")
        # v.addWidget(label)

        h = QHBoxLayout(self)
        h.setSpacing(0)
        h.setObjectName("==")
        h.setContentsMargins(0, 0, 0, 0)
        self.btn1 = JuLabel(self)
        self.btn2 = JuLabel(self)
        self.btn3 = JuLabel(self)
        self.btn1.setText("user")
        self.btn2.setText("test")
        self.btn3.setText("python")
        self.btn3.setToolTip(".........")
        # self.btn1.mouse_enter_leave.connect(self.test)
        # self.btn1 = QPushButton("运行", self)
        # self.btn2 = QPushButton("服务", self)
        self.btn1.setObjectName(u"btn1")
        self.btn2.setObjectName(u"btn2")
        self.btn3.setObjectName(u"btn3")
        # btn1.setStyleSheet(u"border: none;")
        h.addWidget(self.btn1)
        h.addWidget(self.btn2)
        horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        h.addItem(horizontalSpacer)
        h.addWidget(self.btn3)
        v.addLayout(h)


class JuLabel(QLabel):
    mylabelSig = Signal(str)
    mylabelDoubleClickSig = Signal(str)
    mouse_enter_leave = Signal(bool, str)

    def __int__(self, name=None):
        super(JuLabel, self).__init__()

    def mouseDoubleClickEvent(self, e):
        sigContent = self.objectName()
        self.mylabelDoubleClickSig.emit(sigContent)

    def mousePressEvent(self, e):    # 单击
        sigContent = self.objectName()
        self.mylabelSig.emit(sigContent)

    def leaveEvent(self, e):  # 鼠标离开label
        sigContent = self.objectName()
        self.mouse_enter_leave.emit(False, sigContent)
        # print("leaveEvent")

    def enterEvent(self, e):  # 鼠标移入label
        sigContent = self.objectName()
        self.mouse_enter_leave.emit(True, sigContent)
