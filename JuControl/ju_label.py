#!/usr/bin/env python3
# -*- coding: utf-8 -*-

r"""
"""

__author__ = "Jiangjun"

from PySide2.QtCore import Signal
from PySide2.QtWidgets import QLabel


class JuLabel(QLabel):
    mylabelSig = Signal(str)
    mylabelDoubleClickSig = Signal(str)
    mouse_enter_leave = Signal(bool, str)

    def __int__(self, name=None):
        super(JuLabel, self).__init__()

    def mouseDoubleClickEvent(self, e):   # 双击
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
        # print("enterEvent")
