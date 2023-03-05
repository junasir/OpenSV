#!/usr/bin/env python3
# -*- coding: utf-8 -*-

r"""
"""
__author__ = "Jiang Jun"

from sys import argv, exit, path
import os
CURRENT_FILE_PATH = os.path.dirname(__file__).replace("\\", "/")
if os.path.exists(CURRENT_FILE_PATH + "/JuWidget"):
    path.append(CURRENT_FILE_PATH + "/JuWidget")
from PySide2 import QtCore
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import *
from JuLogin.Ui.ju_login_ui import Login_in
from multiprocessing import Queue, freeze_support
from JuQueue.ju_queue_manage import Ju_Process_Manage


if __name__ == '__main__':
    freeze_support()
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(argv)
    # app.setStyleSheet(load_stylesheet_pyside2())
    consumer_receive = Queue()
    producer_send = Queue()
    p = Ju_Process_Manage(receive=producer_send, send=consumer_receive)
    p.daemon = True
    p.start()
    MainWindow = Login_in(receive=consumer_receive, send=producer_send)
    app.setWindowIcon(QIcon("./JuResource/img/icon.ico"))
    exit(app.exec_())
