#!/usr/bin/env python3
# -*- coding: utf-8 -*-

r"""
"""

__author__ = "Jiang Jun"

from PySide2 import QtCore
from PySide2.QtWidgets import QDialog, QGridLayout, QLabel
from ju_cfg import JuConfig


class JuAboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        # self.setWindowFlags(Qt.WindowStaysOnTopHint)
        # self.setWindowModality(Qt.ApplicationModal)
        self.setWindowTitle("关于")
        self.resize(300, 200)
        self.setMinimumSize(QtCore.QSize(300, 200))
        self.setMaximumSize(QtCore.QSize(300, 200))
        self.initUI()

    def initUI(self):
        self.label = QLabel(self)
        self.label.setText(f"{JuConfig.WINDOWS_TITLE}\nAuthor  : team2111")
        self._grid = QGridLayout(self)
        self._grid.addWidget(self.label, 2, 0, 1, 2)
