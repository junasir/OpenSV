# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'login_info.ui'
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
        QFontDatabase.addApplicationFont('./JuResource/font/PuHuiTi-Medium.ttf')
        QFontDatabase.addApplicationFont('./JuResource/font/PuHuiTi-Bold.ttf')
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(380, 500)
        Form.setMinimumSize(QSize(380, 500))
        Form.setMaximumSize(QSize(380, 500))
        self.btn_close = QPushButton(Form)
        self.btn_close.setObjectName(u"btn_close")
        self.btn_close.setGeometry(QRect(340, 10, 21, 21))
        self.btn_close.setStyleSheet(u"\nfont: 12pt \"Times New Roman\";")
        self.btn_min = QPushButton(Form)
        self.btn_min.setObjectName(u"btn_min")
        self.btn_min.setGeometry(QRect(310, 10, 21, 21))
        self.btn_min.setStyleSheet(u"\nfont: 12pt \"Times New Roman\";")
        self.label_icon = QLabel(Form)
        self.label_icon.setObjectName(u"label_icon")
        self.label_icon.setGeometry(QRect(100, 90, 180, 70))
        self.label_icon.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(90, 160, 201, 31))
        self.label_2.setStyleSheet(u"font: 10pt \"Alibaba PuHuiTi M\";\ncolor: rgb(71, 71, 71);")
        self.label_2.setAlignment(Qt.AlignCenter)
        self.label_2.setWordWrap(True)
        self.btn_load = QPushButton(Form)
        self.btn_load.setObjectName(u"btn_load")
        self.btn_load.setGeometry(QRect(80, 280, 220, 40))
        self.btn_load.setStyleSheet("font: 10pt \"Alibaba PuHuiTi M\";")
        self.btn_application = QPushButton(Form)
        self.btn_application.setObjectName(u"btn_application")
        self.btn_application.setGeometry(QRect(80, 350, 220, 40))
        self.btn_application.setStyleSheet("font: 10pt \"Alibaba PuHuiTi M\";")
        self.label_3 = QLabel(Form)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(20, 430, 340, 61))
        self.label_3.setStyleSheet(u"font: 10pt \"Alibaba PuHuiTi M\";\ncolor: rgb(71, 71, 71);")
        self.label_3.setAlignment(Qt.AlignBottom | Qt.AlignLeading | Qt.AlignLeft)
        self.label_3.setWordWrap(True)
        self.label_3.setMargin(0)
        self.label_4 = QLabel(Form)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(90, 10, 201, 25))
        self.label_4.setStyleSheet("font: 10pt \"Alibaba PuHuiTi M\";\ncolor: rgb(71, 71, 71);")
        self.label_4.setAlignment(Qt.AlignCenter)
        self.label_4.setWordWrap(True)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)

    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.btn_close.setText("")
        self.btn_min.setText("")
        self.label_icon.setText("")
        self.label_2.setText(QCoreApplication.translate("Form", u"manage_platform", None))
        self.btn_load.setText(QCoreApplication.translate("Form", u"\u5bfc\u5165license", None))
        self.btn_application.setText(QCoreApplication.translate("Form", u"\u7533\u8bf7license", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"Designer by team2111. \nThe final right of interpretation belongs to team2111.",None))
        self.label_4.setText(QCoreApplication.translate("Form", u"manage_platform", None))
    # retranslateUi
