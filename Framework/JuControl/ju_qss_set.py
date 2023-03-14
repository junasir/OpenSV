#!/usr/bin/env python3
# cython: language_level=3
# -*- coding: utf-8 -*-

r"""
"""

__author__ = "Jiang Jun"

from PySide2.QtCore import QObject, Qt


class Ju_Qss_Set(QObject):

    def __init__(self, parent=None, ui=None):
        super(Ju_Qss_Set, self).__init__(parent)
        self.parent = parent
        self.ui = ui
        self.font_size()

    def font_size(self):
        self.size = "16px"
        self.size_height = "26px"

    def ju_qss_set_one(self):
        # self.parent.setStyleSheet("QMainWindow::separator{background-color:rgb(251,244,244);width:2px;height:1px;}")
        self.parent.setStyleSheet(
            # 主内容
            "QMainWindow::separator{background-color:#323232;width:1px;height:1px;}"
            # 菜单栏
            "QHeaderView::section{font:" + self.size + ";background:#3C3F41;}"
            "QMenuBar {font-family:Arial;background-color:#3C3F41;"
            "border-radius: 0px;font: " + self.size + ";color: white;border-bottom: 1px solid #515151;}"
            "QMenuBar::item {padding-top:7px;padding-left:10px;padding-right:10px;padding-bottom:7px;}"
            "QMenuBar::item:selected {padding-top:2px;padding-left:2px;padding-right:2px;border-width:2px;"
            "border-radius:4px;border-style:solid;background-color:#4B6EAF;border-color: #4B6EAF;}"
            "QMenu {background-color:#3C3F41;}QMenu::item {font-family:Arial;font:" + self.size + ";color: white;"
            "width:160px;height:" + self.size_height + ";padding-right:50px;}"
            "QMenu::item:selected {font:bold " + self.size + ";background-color: #4B6EAF;border-style:solid;"
                                                             "border-width:3px;"
            "border-radius:4px;padding-left:20px;border-bottom-color:#4B6EAF;border-top-color:#4B6EAF;"
            "border-right-color:#4B6EAF;border-left-color:#4B6EAF;}"
            # tabbar
            "QToolBar {spacing: 6px;background: #3C3F41;border-radius: 0px;}"
            "QToolBar::separator {width: 1px;margin-left: 3px;margin-right: 3px;background-color: gray;}"
            "QToolButton {border: none;border-radius: 5px;background-color: #3C3F41;}"
            "QToolButton:disabled{color: gray;background: rgb(105, 105, 105);}"
            "QToolButton:pressed {background-color: gray;}"
            "QToolButton:hover {background-color: gray;}"
            "QToolTip {border: none;border-radius: 10px;color:#f0f0f0;background-color:#6A6A6A;"
            "text-align: left;font: " + self.size + ";}"
            # "QTabWidget::pane {border-width: 1px;border-radius: 6px;}"
            # "QTabBar::tab {padding-left:4px;padding-right:4px;padding-bottom:2px;padding-top:2px;"
            # "background-color:darkgray;border-style: solid;border-width: 1px;border-top-right-radius:4px;"
            # "border-top-left-radius:4px;border-top-color: rgb(180,180,180);border-left-color: rgb(180,180,180);"
            # "border-right-color: rgb(180,180,180);border-bottom-color: transparent;}"
            # "QTabBar::tab:selected, QTabBar::tab:last:selected,QTabBar::tab:hover"
            # "{background-color:#85D7D1;margin-left: 0px;margin-right: 1px;}"
            # "QTabBar::tab:!selected {margin-top: 1px;margin-right: 1px;background-color:darkgray;}"
            # "QTabBar::tab:disabled {width: 0;color: transparent;padding-left:0px;padding-right:0px;"
            # "padding-bottom:0px;padding-top:0px;border-style: none;border-width: 0px;"
            # "border-top-right-radius:0px;border-top-left-radius:0px;}"
            # "#bottom_widget{background-color:#323131;}"
        )
        self.parent.text_.setStyleSheet(
            u"font-family:Arial;font:" + self.size + ";background-color:#2B2B2B;"
        )
        # self.parent.tab_widget1.setStyleSheet(
        #     "QTabWidget::pane {border-width: 1px;border-radius: 6px;}"
        #     "QTabBar::tab {padding-left:4px;padding-right:4px;padding-bottom:2px;padding-top:2px;"
        #     "background-color:darkgray;border-style: solid;border-width: 1px;border-top-right-radius:4px;"
        #     "border-top-left-radius:4px;border-top-color: rgb(180,180,180);border-left-color: rgb(180,180,180);"
        #     "border-right-color: rgb(180,180,180);border-bottom-color: transparent;}"
        #     "QTabBar::tab:selected, QTabBar::tab:last:selected,QTabBar::tab:hover "
        #     "{background-color:#85D7D1;margin-left: 0px;margin-right: 1px;}"
        #     "QTabBar::tab:!selected {margin-top: 1px;margin-right: 1px;background-color:darkgray;}"
        #     "QTabBar::tab:disabled {width: 0;color: transparent;padding-left:0px;padding-right:0px;"
        #     "padding-bottom:0px;padding-top:0px;border-style: none;border-width: 0px;"
        #     "border-top-right-radius:0px;border-top-left-radius:0px;}"
        # )
        # self.parent.tab_widget1.setStyleSheet(
        #     "QTabWidget::pane {background-color:#2B2B2B;border:none;}"
        #     "QTabBar::tab {height:23px;font: " + self.size + ";width:110%;background-color:#3C3F41;color:#BBBBBB;"
        #     "background-color:#3C3F41;border-style: solid;border-width: 1px;"
        #                                                      "border-top-color: #3C3F41;"
        #                                                      "border-left-color: #3C3F41;"
        #                                                      "border-right-color: #3C3F41;}"
        #     "QTabBar::tab:selected {background-color:#3C3F41;margin-left: 0px;margin-right: 1px;"
        #                                                      "border-bottom-color: #747A80; border-bottom-width: 2px;}"
        #     "QTabBar::tab:last:selected {background-color:#3C3F41;}"
        #     "QTabBar::tab:hover {background-color:#3C3F41;}"
        #     "QTabBar::tab:!selected {background-color:#3C3F41;border-bottom-color: #3C3F41;}"
        #     "QTabBar::tab:disabled {width: 0;color: transparent;padding-left:0px;padding-right:0px;"
        #     "padding-bottom:0px;padding-top:0px;border-style: none;border-width: 0px;border-top-right-radius:0px;"
        #     "border-top-left-radius:0px;}"
        # )
        self.parent.device_widget_.setStyleSheet("QWidget{background: #3C3F41;color:#FFFFFF;}")
        self.parent.bottom_log_show.setStyleSheet("QPlainTextEdit{background: #2B2B2B;"
                                                  "font: " + self.size + ";}"
                                                  "QScrollBar:vertical{background-color:#2B2B2B;width:12px;"
                                                                         "color:#595B5D;}")
        self.parent.bottom_log_show_test.setStyleSheet("QPlainTextEdit{background: #2B2B2B;"
                                                  "font: " + self.size + ";}"
                                                  "QScrollBar:vertical{background-color:#2B2B2B;width:12px;"
                                                  "color:#595B5D;}")
        self.parent.bottom_widget.setStyleSheet(
            u"#bottom_widget{background-color:#3C3F41;}"
        )
        self.parent.tab_widget.setStyleSheet(
            "QTabWidget::pane {background-color:#3C3F41;border:none;}"
            "QTabBar::tab {height:105%;font: " + self.size + ";width:19px;background-color:#3C3F41;color:#FFFFFF;"
            "background-color:#3C3F41;border-style: solid;}"
            "QTabBar::tab:selected {background-color:#2D2F30;margin-left: 0px;margin-right: 1px;}"
            "QTabBar::tab:last:selected {background-color:#3C3F41;}"
            "QTabBar::tab:hover {background-color:#3C3F41;}"
            "QTabBar::tab:!selected {background-color:#3C3F41;color:#A5BABA;}"
            "QTabBar::tab:disabled {width: 0;color: transparent;padding-left:0px;padding-right:0px;"
            "padding-bottom:0px;padding-top:0px;border-style: none;border-width: 0px;border-top-right-radius:0px;"
            "border-top-left-radius:0px;}"
        )
        self.parent.left_widget.setStyleSheet(
            u"#left_widget{background-color:#3C3F41;}"
        )
        self.parent.tab.setStyleSheet(u"border-left:1px solid #323232;")
        self.parent.tab_bottom.btn1.setStyleSheet(
            "background-color:#2D2F30;color:#FFFFFF;margin-left: 15px"
        )
        self.parent.tab_bottom.btn2.setStyleSheet(
            "background-color:#3C3F41;color:#FFFFFF;"
        )
        self.parent.tab_bottom.btn3.setStyleSheet(
            "background-color:#3C3F41;color:#FFFFFF;"
        )
        self.parent.tab_bottom.btn1.setFixedWidth(70)
        self.parent.tab_bottom.btn1.setAlignment(Qt.AlignCenter)
        self.parent.tab_bottom.btn2.setFixedWidth(70)
        self.parent.tab_bottom.btn2.setAlignment(Qt.AlignCenter)
        self.parent.tab_bottom.btn3.setFixedWidth(70)
        self.parent.tab_bottom.btn3.setAlignment(Qt.AlignCenter)
        self.parent.statuBar.setStyleSheet(
            "background-color:#414146;color:#FFFFFF;"
        )
        self.parent.label0.setStyleSheet(
            "color:#FFFFFF;"
        )
        self.parent.tab.setStyleSheet(
            "QTreeWidget{border-left:0.5px solid #323232;color:#E1F0EE;"
            "background-color: #3C3F41;font:" + self.size + ";}"
            "QTreeWidget::item{background: transparent;background-clip: content;}"
            "QTreeView{show-decoration-selected: 1;}"
            "QTreeView::item:hover, QTreeView::branch:hover {background: #0D293E;}"
            "QTreeView::item:selected:active, QTreeView::branch:selected{background: #4B6EAF;}"
            "QTreeView::item:selected:!active,QTreeView::branch:selected:!active {background: #0D293E;color:#E1F0EE}"
            "QTreeView::branch::closed::has-children{image: url(./JuResource/img/tree_open.png);}"
            "QTreeView::branch::open::has-children{image: url(./JuResource/img/tree_close.png);}"
            "QScrollBar:horizontal{background-color:#595B5D;height:12px;}"
            # "QScrollBar::add-page:horizontal,QScrollBar::sub-page:horizontal{background-color:transparent;}"
            # "QScrollBar::handle:horizontal{background:rgba(75,120,154,0.8);border:1px solid rgba(82,130,164,1);}"
        )
        self.parent.tab_widget_new.setStyleSheet(
            "QTabWidget::pane {background-color:#3C3F41;border:none;}"
            "QTabBar::tab {font: " + self.size + ";width: 100%;background-color:#3C3F41;color:#FFFFFF;"
            "background-color:#3C3F41;border-style: solid;}"
            "QTabBar::tab:selected {background-color:#2D2F30;margin-left: 0px;margin-right: 1px;}"
            "QTabBar::tab:hover {background-color:#3C3F41;}"
            "QTabBar::tab:!selected {background-color:#3C3F41;color:#A5BABA;}"
        )
        self.parent.center_widget.setStyleSheet(
            "background-color:#3C3F41;"
        )
        self.parent.btn_device_support.setStyleSheet(
            "QPushButton{border-width: 1px;padding: 4px;background-color: #353739;}"
            "QPushButton:hover{border-width: 1px;padding: 2px;background-color: #485156;}"
            "QPushButton:pressed{border-width: 1px;padding: 2px;background-color: #3C3F41;}"
        )
        self.parent.btn_disconnect_device.setStyleSheet(
            "QPushButton{border-width: 1px;padding: 4px;background-color: #353739;}"
            "QPushButton:hover{border-width: 1px;padding: 2px;background-color: #485156;}"
            "QPushButton:pressed{border-width: 1px;padding: 2px;background-color: #3C3F41;}"
        )
        self.parent.btn_connect_device.setStyleSheet(
            "QPushButton{border-width: 1px;padding: 4px;background-color: #353739;}"
            "QPushButton:hover{border-width: 1px;padding: 2px;background-color: #485156;}"
            "QPushButton:pressed{border-width: 1px;padding: 2px;background-color: #3C3F41;}"
        )
        self.parent.ip_widget.setStyleSheet(
            "QPushButton{border-width: 1px;padding: 4px;background-color: #353739;}"
            "QPushButton:hover{border-width: 1px;padding: 2px;background-color: #485156;}"
            "QPushButton:pressed{border-width: 1px;padding: 2px;background-color: #3C3F41;}"
            "QListWidget {border: 1px solid #6A6A6A;}"
            "QListWidget:disabled{color: gray;background: rgb(105, 105, 105);}"
            "QListWidget::item {margin-bottom: 3px;}"
            "QWidget{color:#f0f0f0;font-family:Arial;font:16px;background-color:#505050;}"
        )
        self.parent.img_show_widget.setStyleSheet(
            "QWidget{color:#ffffff;font-family:Arial;font:16px;background-color:#3C3F41;}"
        )

