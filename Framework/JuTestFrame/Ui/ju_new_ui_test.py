#!/usr/bin/env python3
# -*- coding: utf-8 -*-

r"""
"""

__author__ = "Jiangjun"

import sys

from PySide2.QtCore import Qt, QSize
from PySide2.QtGui import QColor, QPixmap
from PySide2.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QMainWindow, QMessageBox
from qdarkstyle import load_stylesheet_pyside2

from JuFileOperate.ju_file_reader import JuFileRead
from JuTestFrame.Ui.ju_test_frame_base import Ju_Ui_Main
from qframelesswindow import FramelessWindow
from JuControl.ju_custom_bar import CustomTitleBar
from JuTestFrame.Ui.ju_test_ui_fuc import Ju_Test_Ui_Fuc
from ju_cfg import JuConfig


class Ju_Ui_Window(FramelessWindow):

    def __init__(self, parent=None, deal_receive=None, deal_send=None, person_type=None):
        super().__init__()
        # self.setStyleSheet(JuFileRead.read_file(u"./JuResource/2.qss"))
        self.deal_receive = deal_receive
        self.deal_send = deal_send
        self._widget = QWidget()
        # self._widget.setStyleSheet(JuFileRead.read_file(u"./JuResource/2.qss"))
        # change the default title bar if you like
        self._widget.setStyleSheet(load_stylesheet_pyside2())
        self.title_ui = CustomTitleBar(self)
        self.setTitleBar(self.title_ui)
        self.setMinimumSize(QSize(900, 730))
        self.setWindowTitle(JuConfig.WINDOWS_TITLE)

        self._ui = QMainWindow()
        self._ju_ui = Ju_Ui_Main(parent=self._ui).get_ui()
        self.Ju_Test_Ui_Fuc = Ju_Test_Ui_Fuc(parent=self, deal_receive=self.deal_receive, deal_send=self.deal_send,
                                             person_type=person_type, new_ui_test=self._ju_ui)
        self.widget = QWidget(self)
        self.widget.setObjectName(u"widget")
        # self.widget.setGeometry(QRect(60, 40, 72, 30))
        self.verticalLayout = QVBoxLayout(self.widget, spacing=0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.addWidget(self._ju_ui)
        self.setStyleSheet("border: none;")
        self.titleBar.raise_()

    def resizeEvent(self, e):
        # don't forget to call the resizeEvent() of super class
        super().resizeEvent(e)
        length = min(self.width(), self.height())
        self.title_ui.label.resize(self.width() - 138, 28)
        self.widget.resize(self.width(), self.height() - 28)
        self.widget.move(
            0, 28
        )
        x = self.widget.width() - self._ju_ui._plugin_version.width() - 5
        y = self.widget.height() - self._ju_ui._plugin_version.height() - 30
        self._ju_ui._plugin_version.move(x, y)

    def closeEvent(self, event):
        msgbox = QMessageBox(self._widget)
        msgbox.setText('Are you sure to quit?')
        msgbox.setWindowTitle('Close Message')
        msgbox.setStandardButtons(
            QMessageBox.Save | QMessageBox.Close | QMessageBox.Cancel)
        # msgbox.button(QMessageBox.Yes).setText('Goto Login')
        # msgbox.button(QMessageBox.Yes).setFixedWidth(100)
        msgbox.button(QMessageBox.Save).setFixedWidth(100)
        msgbox.button(QMessageBox.Close).setFixedWidth(100)
        msgbox.button(QMessageBox.Cancel).setFixedWidth(100)
        reply = msgbox.exec_()
        if reply == QMessageBox.Save:
            self.Ju_Test_Ui_Fuc.close_(flag=2)
            self._ju_ui.close()
            self.close()
            # number = self._ui_base.tab_widget_new.count()
            # for i in range(number):
            #     self.close_tab(i)
            # if self.save_file_flag:
            #     self.Project_save()
            # self._ui_base.close()
            event.accept()
        elif reply == QMessageBox.Close:
            self._ju_ui.close()
            self.close()
            self.Ju_Test_Ui_Fuc.close_(flag=1)
            event.accept()
        else:
            event.ignore()


if __name__ == "__main__":
    # enable dpi scale
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    # run app
    app = QApplication(sys.argv)
    demo = Ju_Ui_Window()
    demo.show()
    sys.exit(app.exec_())
