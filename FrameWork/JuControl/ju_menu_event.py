#!/usr/bin/env python3
# -*- coding: utf-8 -*-

r"""
"""

__author__ = "Jiangjun"


from PySide2.QtCore import Signal
from PySide2.QtGui import Qt
from PySide2.QtWidgets import QMenu


class JuMenuEvent(QMenu):
    press_log = Signal(int, int)

    def __init__(self, parent=None):
        super(JuMenuEvent, self).__init__(parent)

    def mousePressEvent(self, e):
        QMenu.mousePressEvent(self, e)
        print(e.x(), e.y())
        btn_press = e.button()
        if btn_press == Qt.RightButton:
            self.press_log.emit(e.x(), e.y())
