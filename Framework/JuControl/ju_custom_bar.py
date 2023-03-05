# coding:utf-8
import sys

from PySide2.QtCore import Qt, QSize
from PySide2.QtGui import QColor, QPixmap
from PySide2.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QMainWindow
from JuTestFrame.Ui.ju_test_frame_base import Ju_Ui_Main
from qframelesswindow import TitleBar


class CustomTitleBar(TitleBar):
    """ Custom title bar """

    def __init__(self, parent):
        super().__init__(parent)
        # add title label
        self.titleLabel = QLabel(self)
        self.titleLabel.setStyleSheet("QLabel{font: 13px 'Segoe UI'; margin: 9px;color:#BBBBBB}")
        self.setStyleSheet("QWidget{background-color:#323131;}")
        self.window().windowTitleChanged.connect(self.setTitle)

        # customize the style of title bar button
        self.minBtn.setHoverColor(Qt.white)
        self.minBtn.setHoverBackgroundColor(QColor(0, 100, 182))
        self.minBtn.setPressedColor(Qt.white)
        self.minBtn.setPressedBackgroundColor(QColor(54, 57, 65))

        # use qss to customize title bar button
        self.maxBtn.setStyleSheet("""
            background-color:#323131;
            # TitleBarButton {
            #     
            #     qproperty-hoverColor: white;
            #     qproperty-hoverBackgroundColor: rgb(0, 100, 182);
            #     qproperty-pressedColor: white;
            #     qproperty-pressedBackgroundColor: rgb(54, 57, 65);
            # }
        """)

    def setTitle(self, title):
        self.titleLabel.setText(title)
        self.titleLabel.adjustSize()
