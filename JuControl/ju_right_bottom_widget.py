# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'righet_bottom_uicwvYZS.ui'
##
## Created by: Qt User Interface Compiler version 5.14.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################
from threading import Thread
from time import sleep

from PySide2.QtCore import (QCoreApplication, QMetaObject, QObject,
                            QRect, QSize, Qt, Signal)
from PySide2.QtGui import (QFontDatabase, QPixmap)
from PySide2.QtWidgets import *
from win32api import GetMonitorInfo, MonitorFromPoint
from ju_cfg import JuConfig


class Ju_Right_Bottom(QWidget):
    close_signal = Signal()

    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        QFontDatabase.addApplicationFont('./JuResource/font/PuHuiTi-Medium.ttf')
        widget = QWidget(self)
        self._ui = Ui_Form(parent=widget).get_ui()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SplashScreen)
        monitor_info = GetMonitorInfo(MonitorFromPoint((0, 0)))
        monitor_height = monitor_info["Work"][-1]
        monitor_width = monitor_info["Work"][-2]
        x = monitor_width - self._ui.width()
        y = monitor_height - self._ui.height()
        self.move(x, y)
        # self._ui_qss()
        self.close_signal.connect(self.win_close)
        self._ui.pushButton.clicked.connect(self.win_close)

    def _ui_qss(self, mode=None):
        self._ui.pushButton.setText("X")
        if mode == 1:
            self._ui.pushButton.setStyleSheet("QPushButton{background-color: #323131;height:30px;width:30px;"
                                              "color:#BBBBBB;}"
                                              "QPushButton:hover{background-color: red;color:white;}")
            self._ui.widget_2.setStyleSheet("background:#323131;border:none;")
            self._ui.label.setText(JuConfig.WINDOWS_TITLE)
            self._ui.label_img.setText(JuConfig.WINDOWS_TITLE)
            self._ui.label_img.setPixmap(QPixmap("./JuResource/img/info.png"))  # 我的图片格式为png.与代码在同一目录下

            self._ui.label_img.setScaledContents(True)  # 图片大小与label适应，否则图片可能显示不全
            self._ui.label.setStyleSheet(u"font: 10pt \"Alibaba PuHuiTi M\";color:#BBBBBB;")
            self._ui.setStyleSheet("background:#3C3F41;border:none;")
            self._ui.label_info_title.setText("通知")
            self._ui.label_info_title.setStyleSheet(u"font: 16pt \"Alibaba PuHuiTi M\";color:#E1EAF0;")
            self._ui.label_info.setStyleSheet(u"font: 13pt \"Alibaba PuHuiTi M\";color:#E1EAF0;")

    def info_show(self, text=None, timeout=None, qss_mode=1):
        self._ui_qss(mode=qss_mode)
        self.show()
        if len(text) == 0:
            return
        else:
            text = "        " + text
        if timeout is not None and type(timeout) is int:
            time_out_sleep = Thread(target=self.timeout_sleep, args=(timeout,))
            time_out_sleep.start()
        self._ui.label_info.setText(text)

    def timeout_sleep(self, timeout):
        sleep(timeout)
        self.close_signal.emit()

    def win_close(self):
        self.close()


class Ui_Form(QObject):
    def __init__(self, parent=None):
        super().__init__()
        # Test = parent
        self._ui = self.setupUi(parent)
        # print(self._ui.pushButton.text())

    def get_ui(self):
        return self._ui

    def setupUi(self, Form):
        if Form.objectName():
            Form.setObjectName(u"Form")
        # Form.setWindowFlags(Qt.FramelessWindowHint)
        Form.resize(300, 200)
        Form.setContentsMargins(0, 0, 0, 0)
        Form.setMinimumSize(QSize(300, 200))
        Form.setMaximumSize(QSize(300, 200))
        Form.verticalLayout = QVBoxLayout(Form)
        Form.verticalLayout.setObjectName(u"verticalLayout")
        Form.widget_2 = QWidget(Form)
        Form.widget_2.setObjectName(u"widget_2")
        Form.widget_2.setMaximumSize(QSize(16777215, 30))
        Form.horizontalLayout = QHBoxLayout(Form.widget_2)
        Form.horizontalLayout.setObjectName(u"horizontalLayout")
        Form.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        Form.label_3 = QLabel(Form.widget_2)
        Form.label_3.setObjectName(u"label_3")
        Form.label_3.setMinimumSize(QSize(5, 0))

        Form.horizontalLayout.addWidget(Form.label_3)
        Form.label = QLabel(Form.widget_2)
        Form.label.setObjectName(u"label")
        Form.horizontalLayout.addWidget(Form.label)
        Form.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        Form.horizontalLayout.addItem(Form.horizontalSpacer)
        Form.pushButton = QPushButton(Form.widget_2)
        Form.pushButton.setObjectName(u"pushButton")
        Form.pushButton.setFixedWidth(30)
        Form.horizontalLayout.addWidget(Form.pushButton)
        Form.verticalLayout.addWidget(Form.widget_2)
        Form.widget = QWidget(Form)
        Form.widget.setObjectName(u"widget")

        Form.label_info_title = QLabel(Form.widget)
        Form.label_info_title.setObjectName(u"label_info_title")
        Form.label_info_title.setGeometry(QRect(50, 10, 181, 25))
        Form.label_info = QTextEdit(Form.widget)
        Form.label_info.setObjectName(u"label_info")
        Form.label_info.setGeometry(QRect(20, 40, 251, 101))
        Form.label_info.setReadOnly(True)

        # Form.label_info.setWordWrap(True)
        # Form.label_info.setAlignment(Qt.AlignTop | Qt.AlignLeading | Qt.AlignLeft)
        # Form.label_info.setMargin(0)
        Form.label_img = QLabel(Form.widget)
        Form.label_img.setObjectName(u"label_img")
        Form.label_img.setGeometry(QRect(20, 10, 25, 25))

        Form.verticalLayout.addWidget(Form.widget)
        Form.verticalLayout.setContentsMargins(0, 0, 0, 0)
        Form = self.retranslateUi(Form)
        QMetaObject.connectSlotsByName(Form)
        return Form

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        # Form.label.setText(QCoreApplication.translate("Form", u"TextLabel", None))
        # Form.pushButton.setText(QCoreApplication.translate("Form", u"PushButton", None))
        return Form
    # retranslateUi
#
# if __name__ == '__main__':
#     app = QApplication(argv)
#     # app.setStyleSheet(load_stylesheet_pyside2())
#     MainWindow = Ju_Right_Bottom()
#     # MainWindow = Ju_Test_Ui_New()
#     app.setWindowIcon(QIcon("./JuResource/img/icon.ico"))
#     a = "22211aa啊啊啊啊啊啊啊啊啊啊啊啊啊啊"
#     MainWindow.info_show(text=a, timeout=5)
#     # MainWindow.show()
#     exit(app.exec_())