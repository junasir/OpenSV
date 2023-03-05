#!/usr/bin/env python3
# -*- coding: utf-8 -*-

r"""
"""

__author__ = "Jiang Jun"

from datetime import datetime
from time import sleep
from PySide2.QtCore import Qt, QThread, Signal
from PySide2.QtGui import QPixmap, QPainter, QCursor
from PySide2 import QtWidgets
from PySide2.QtWidgets import QFileDialog, QMessageBox
from loguru import logger
from JuTestFrame.Ui.ju_new_ui_test import Ju_Ui_Window
from JuLogin.Ui.ju_login_info import Ui_Form as Login_ui
from JuControl.JuMysqlLoginUi import JuMysqlLogin
from ju_cfg import JuConfig

now = (datetime.now()).strftime("%Y-%m-%d %H_%M_%S")
logger.add(JuConfig.LOG_SAVE_PATH + "/runtime_" + str(now) + ".log", retention='10 days')


class Login_In_Thread(QThread):

    def __init__(self, parent):
        super(Login_In_Thread, self).__init__()
        self.parent = parent
        self.list_name = []
        self.list_id = []

    def _init_license(self, flag=False, person_type="", ip=""):
        self.parent.login_show_signal.emit(flag, person_type, ip)
        print(flag, person_type, ip)

    def _load_license(self, flag=False, info="", ip=""):
        self.parent.login_license_input_signal.emit(flag, info, ip)
        print(flag, info)

    def _get_mysql_info(self, flag=False):
        self.parent.online_login.emit(flag)

    def run(self):
        while 1:
            if not self.parent.receive.empty():
                msg = self.parent.receive.get()
                if isinstance(msg, dict) is True and hasattr(self, msg.get("func")) is True:
                    getattr(self, msg.get("func"))(*msg.get("args", ()), **msg.get("kwargs", {}))
            sleep(0.1)

    def closeEvent(self):
        self.terminate()
        self.wait()
        if self.isFinished():
            del self


class Login_in(QtWidgets.QWidget, Login_ui):
    login_show_signal = Signal(bool, str, str)
    login_license_input_signal = Signal(bool, str, str)
    online_login = Signal(bool)

    def __init__(self, receive=None, send=None):
        super(Login_in, self).__init__()
        self.setWindowTitle(JuConfig.PROGRAME_NAME)
        self.receive = receive
        self.send = send
        self.setupUi(self)
        self._init_all()
        self._bind_event()

    def _init_all(self):
        self.btn_application.setText("在线登录")
        self.login_in_thread = Login_In_Thread(self)
        self.login_in_thread.start()
        self.label_icon.setPixmap(QPixmap("./JuResource/img/bac_1.png"))
        self.label_icon.setScaledContents(True)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        with open("./JuResource/ju_login_ui_style.qss", "r", encoding="utf-8") as f:
            style = f.read()
            self.setStyleSheet(style)
        self.btn_close.setStyleSheet("QPushButton{border-image: url(./JuResource/img/close_1.png)}")
        self.btn_min.setStyleSheet("QPushButton{border-image: url(./JuResource/img/min_1.png)}")
        # self.send.put({"func": "_get_mysql_info", "args": ("在线登录",)})
        self.login_show(True, "person_type", "ip")

    def _bind_event(self):
        self.btn_min.clicked.connect(self.min)
        self.btn_close.clicked.connect(self.close)
        self.btn_load.clicked.connect(self.load_license)
        self.btn_application.clicked.connect(self.application_license)
        # self.login_show_signal.connect(self.login_show)
        self.login_license_input_signal.connect(self._load_license_deal)
        self.online_login.connect(self._online_login)

    def login_show(self, flag, person_type, ip):
        print(flag, person_type, ip)
        # self.show()
        if flag is False:
            if person_type == "":
                self.show()
            else:
                self.show()
                # print(person_type)
        elif flag:
            # if person_type == "teacher":
                # self.a = "2"
                # self.socket_receive = Queue()
                # self.socket_send = Queue()
                # ju_socket_manage = Ju_Socket_Manage_Server(receive=self.socket_receive, send=self.socket_send)
                # ju_socket_manage.daemon = True
                # ju_socket_manage.start()
                # q_receive = Thread(target=self.queue_receive, args=(), daemon=True)
                # q_receive.start()
                # self.hide()
                # , socket_receive=self.socket_receive,
                #                                         socket_send=self.socket_send
            self.login_in_thread.closeEvent()
            del self.login_in_thread
            self.close()
            self.ju_ui_main = Ju_Ui_Window(person_type=person_type, deal_receive=self.receive, deal_send=self.send)
            self.ju_ui_main.show()
            # elif person_type == "student":
            #     pass
            # else:
            #     pass
            # print(person_type)
            # pass

    # def queue_receive(self):
    #     while True:
    #         if not self.socket_receive.empty():
    #             msg = self.socket_receive.get(timeout=0.1)
                # logger.debug(msg)

    def _load_license_deal(self, flag, info, ip):
        print(2222)
        print(flag, info)
        if flag is False:
            QMessageBox.information(self, "Error", info, QMessageBox.Yes)
        else:
            self.close()
            self.login_show(flag, info, ip)

    def load_license(self):
        get_filename_path, ok = QFileDialog.getOpenFileName(self,
                                                            "导入license",
                                                            "C:/",
                                                            "License Files (*.license)")

        if get_filename_path != "":
            print("===", get_filename_path)
            self.send.put({"func": "_load_license", "args": (get_filename_path,)})
        pass

    def application_license(self):
        self.ju_mysql_login = JuMysqlLogin()
        self.ju_mysql_login.show()
        self.ju_mysql_login.pushButton_login.clicked.connect(self._mysql_login)

    def _mysql_login(self):
        account = self.ju_mysql_login.lineEdit_account.text()
        password = self.ju_mysql_login.lineEdit_password.text()
        # self.send.put({"func": "_get_mysql_info", "args": (get_filename_path,)})
        print(account, password)

    def _init_license(self):
        self.send.put({"func": "_init_license", "args": ()})

    def _online_login(self, flag):
        self.btn_application.setHidden(flag)
        self._init_license()

    def paintEvent(self, event):
        # 圆角
        pat2 = QPainter(self)
        pat2.setRenderHint(pat2.Antialiasing)  # 抗锯齿
        pat2.setBrush(Qt.white)
        pat2.setPen(Qt.transparent)
        rect = self.rect()
        pat2.drawRoundedRect(rect, 15, 15)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))  # 更改鼠标图标

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos() - self.m_Position)  # 更改窗口位置
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))

    # def keyPressEvent(self, event):
    #     if (event.key() == Qt.Key_Enter) or (event.key() == Qt.Key_Return):
    #         self.login_in()

    def min(self):
        self.showMinimized()
