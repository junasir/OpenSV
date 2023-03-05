# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'login.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(450, 400)
        Form.setMinimumSize(QSize(450, 400))
        Form.setMaximumSize(QSize(450, 400))
        Form.setStyleSheet(u"border-radius: 15px;")
        self.widget = QWidget(Form)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(0, 0, 450, 400))

        self.s_widget = QWidget(Form)
        self.s_widget.setObjectName(u"s_widget")
        self.s_widget.setGeometry(QRect(30, 110, 121, 31))

        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(0, 0, 450, 100))
        self.label.setStyleSheet(u"background-color: rgb(255, 255, 255);\nborder-radius: 15px;")
        self.pushButton_ren = QPushButton(self.widget)
        self.pushButton_ren.setObjectName(u"pushButton_ren")
        self.pushButton_ren.setGeometry(QRect(310, 200, 61, 21))
        self.login = QPushButton(self.widget)
        self.login.setObjectName(u"login")
        self.login.setGeometry(QRect(120, 300, 211, 31))
        self.label_password = QLabel(self.widget)
        self.label_password.setObjectName(u"label_password")
        self.label_password.setGeometry(QRect(95, 240, 20, 20))
        self.label_password.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.label_user = QLabel(self.widget)
        self.label_user.setObjectName(u"label_user")
        self.label_user.setGeometry(QRect(95, 200, 20, 20))
        self.label_user.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.user = QLineEdit(self.widget)
        self.user.setObjectName(u"user")
        self.user.setGeometry(QRect(120, 200, 161, 20))
        self.password = QLineEdit(self.widget)
        self.password.setObjectName(u"password")
        self.password.setGeometry(QRect(120, 240, 161, 20))
        self.btn_close = QPushButton(self.widget)
        self.btn_close.setObjectName(u"btn_close")
        self.btn_close.setGeometry(QRect(415, 5, 21, 21))
        self.btn_close.setStyleSheet(u"\nfont: 12pt \"Times New Roman\";")
        self.label_cap = QLabel(self.widget)
        self.label_cap.setObjectName(u"label_cap")
        self.label_cap.setGeometry(QRect(0, 120, 311, 231))
        self.label_cap.setStyleSheet(u"")

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText("")
        self.pushButton_ren.setText(QCoreApplication.translate("Form", u"\u4eba\u8138\u767b\u5f55", None))
        self.login.setText(QCoreApplication.translate("Form", u"\u767b\u5f55", None))
        self.label_password.setText("")
        self.label_user.setText("")
        self.user.setText("")
        self.password.setText("")
        self.btn_close.setText("")
        self.label_cap.setText("")
    # retranslateUi

