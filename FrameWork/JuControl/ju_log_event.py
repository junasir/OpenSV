#!/usr/bin/env python3
# -*- coding: utf-8 -*-

r"""
"""

__author__ = "Jiangjun"


from PySide2.QtCore import Signal
from PySide2.QtGui import Qt
from PySide2.QtWidgets import QPlainTextEdit


class LogEdit(QPlainTextEdit):
    press_log = Signal(int, int)

    def __init__(self, parent=None):
        super(LogEdit, self).__init__(parent)

    def mousePressEvent(self, e):
        QPlainTextEdit.mousePressEvent(self, e)
        btn_press = e.button()
        if btn_press == Qt.RightButton:
            self.press_log.emit(e.x(), e.y())
