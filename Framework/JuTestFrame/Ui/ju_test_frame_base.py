#!/usr/bin/env python3
# -*- coding: utf-8 -*-

r"""
"""

__author__ = "Jiangjun"

import sys
import time
from threading import Thread

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtWidgets import QSizePolicy

from JuControl.ju_device_info_tree import JuDevcieInfoWidget
from JuControl.ju_log_event import LogEdit
# # from JuControl.ju_qss_set import Ju_Qss_Set
# from JuControl.ju_qss_set import Ju_Qss_Set
from JuControl.ju_update_notification import JuUpdateNotification
from JuControl.ju_widget import JuQTreeWidget
from JuControl.ju_bottom_widget import JuBottomWidget


class Ju_Ui_Main(QObject):

    def __init__(self, parent=None, ui=None, name=None, person_type=None, deal_receive=None, deal_send=None,
                 socket_receive=None, socket_send=None, *args, **kwargs):
        super(Ju_Ui_Main, self).__init__(parent)
        self.parent = parent
        self.parent.setMinimumSize(QSize(900, 700))
        self._init_ui(Test=self.parent)
        self.bind_objectname(Test=self.parent)
        # q_receive1 = Thread(target=self.test_, args=())
        # q_receive1.start()
        # self._ui = ui
        # self.parent.setStyleSheet(
        #     # 主内容
        #     "QMainWindow::separator{background-color:#323232;width:1px;height:1px;}")
        # self.qss = Ju_Qss_Set(parent=self.parent)
        # self.qss.ju_qss_set_one()
        # self.setStyleSheet("QMainWindow::separator{background-color:#323232;width:1px;height:1px;}")
        # with open("../../JuResource/2.qss", "r", encoding="utf-8") as f:
        #     style = f.read()
        #     self.setStyleSheet(style)

    def get_ui(self):
        return self.parent

    def bind_objectname(self, Test=None):
        Test.tab_widget.setObjectName(u"tab_widget")
        Test.bottom_log_show.setObjectName(u"bottom_log_show")
        Test.bottom_log_show_test.setObjectName(u"bottom_log_show_test")
        Test.left_widget.setObjectName(u"left_widget")
        Test.bottom_widget.setObjectName(u"bottom_widget")
        # self.tab_widget_new.setObjectName(u"tab_widget")
        Test.tab.setObjectName(u"tab")
        Test.tab_1.setObjectName(u"tab1")
        Test.gridLayout_111.setObjectName(u"gridLayout_111")
        Test.Dockable_1.setObjectName(u"Dockable_1")
        Test.Dockable_2.setObjectName(u"Dockable_2")
        Test.text_.setObjectName(u"text_")

    # 初始化ui
    def _init_ui(self, Test=None):
        self.menu_init(Test=Test)
        self.bottom_bar(Test=Test)
        Test.tab_widget = QTabWidget()
        Test.ip_widget = QWidget()
        Test.device_widget_ = QWidget()
        Test.device_widget_.setObjectName(u"list_")
        Test.gridLayout_13 = QGridLayout(Test.device_widget_)
        # self.gridLayout_13.setSpacing(4)
        Test.gridLayout_13.setObjectName(u"gridLayout_13")
        Test.gridLayout_13.setContentsMargins(0, 0, 0, 0)
        Test.treeWidget_device_info = JuDevcieInfoWidget(Test.device_widget_)
        Test.treeWidget_device_info.setObjectName(u"treeWidget_device_info")
        Test.gridLayout_13.addWidget(Test.treeWidget_device_info, 1, 0, 1, 1)
        Test.btn_device_support = QPushButton(Test.device_widget_)
        Test.btn_device_support.setObjectName(u"btn_device_support")
        Test.gridLayout_13.addWidget(Test.btn_device_support, 2, 0, 1, 1)
        Test.horizontalLayout = QHBoxLayout()
        Test.horizontalLayout.setObjectName(u"horizontalLayout")
        Test.btn_connect_device = QPushButton(Test.device_widget_)
        Test.btn_connect_device.setObjectName(u"btn_connect_device")
        Test.horizontalLayout.addWidget(Test.btn_connect_device)
        Test.btn_disconnect_device = QPushButton(Test.device_widget_)
        Test.btn_disconnect_device.setObjectName(u"btn_disconnect_device")
        Test.horizontalLayout.addWidget(Test.btn_disconnect_device)
        Test.gridLayout_13.addLayout(Test.horizontalLayout, 0, 0, 1, 1)
        # Test.dockWidget_device_info.setWidget(Test.device_widget_)
        # device_parent.addDockWidget(Qt.BottomDockWidgetArea, self.dockWidget_device_info)
        Test.btn_connect_device.setText("Reconnect")
        Test.btn_device_support.setText("Support device info")
        Test.btn_device_support.hide()
        Test.btn_disconnect_device.setText("Disconnect")
        Test.btn_device_support.setObjectName(u"btn_device_support")
        Test.btn_connect_device.setObjectName(u"btn_connect_device")
        Test.btn_disconnect_device.setObjectName(u"btn_disconnect_device")


        # Test.device_widget_ = QTableWidget()
        # Test.device_widget_.setObjectName(u"list_")
        # v_layot = QVBoxLayout()
        # v_layot.setSpacing(0)
        # v_layot.setObjectName(u"gridLayout_111-2")
        # v_layot.setContentsMargins(0, 0, 0, 0)
        # Test.bottom_left_widget = QWidget()
        # v_layot.addWidget(Test.tab_widget)
        # Test.bottom_left_widget.setLayout(v_layot)
        #
        v_layot = QVBoxLayout()
        v_layot.setSpacing(0)
        v_layot.setObjectName(u"gridLayout_111-2")
        v_layot.setContentsMargins(0, 0, 0, 0)
        Test.left_widget = QWidget()
        v_layot.addWidget(Test.tab_widget)
        Test.left_widget.setLayout(v_layot)
        Test.tab = QWidget()
        # Test.tab.tree_copy
        # Test.tab = QWidget()
        Test.tab.setObjectName(u"tab_new_project_widget")
        Test.gridLayout_111 = QVBoxLayout(Test.tab)
        Test.gridLayout_111.setSpacing(0)
        Test.gridLayout_111.setContentsMargins(0, 0, 0, 0)
        # Test.tab.setStyleSheet(u"border-left:1px solid #4A4AEA;")
        Test.tab_widget.addTab(Test.tab, "project file")
        label_name = QLabel('可用插件')
        label_name.setMaximumHeight(30)
        label_name.setAlignment(Qt.AlignCenter)
        label_name.setStyleSheet(u"\nfont: 12pt \"\u963f\u91cc\u5df4\u5df4\u666e\u60e0\u4f53 M\";color: #8EBABA")
        Test.listWidget = QListWidget()
        Test.listWidget.setObjectName(u"tab")

        Test.tab_1 = QWidget()
        verticalLayout = QVBoxLayout(Test.tab_1)
        verticalLayout.setSpacing(0)
        verticalLayout.setObjectName(u"gridLayout")
        verticalLayout.setContentsMargins(0, 0, 0, 0)
        verticalLayout.addWidget(label_name)
        verticalLayout.addWidget(Test.listWidget)
        # Test.tab_widget.addTab(Test.tab_1, "project name")
        Test.tab_widget.setTabPosition(QTabWidget.TabPosition.West)
        # Test.log_show_ui = LogEdit()
        # Test.log_show_ui.setReadOnly(True)
        # Test.log_show_ui.setStyleSheet(u"\n"
        #                                "font: 12pt \"\u963f\u91cc\u5df4\u5df4\u666e\u60e0\u4f53 M\";color: #8EBABA")
        # # 在窗口区域设置QWidget，添加列表控件
        Test.center_widget = QWidget()
        Test.gridLayout_center = QVBoxLayout(Test.center_widget)
        Test.gridLayout_center.setSpacing(0)
        Test.gridLayout_center.setObjectName(u"gridLayout_111")
        Test.gridLayout_center.setContentsMargins(0, 0, 0, 0)
        Test.text_ = QWidget()
        Test.gridLayout_center.addWidget(Test.text_)
        Test.text_.setVisible(True)
        Test.setCentralWidget(Test.center_widget)
        self.init_dock(Test=Test)
        Test.setWindowTitle('manage_platform_v3')
        self.add_toolbar(Test=Test)
        title_text = "Plugins can update"
        content_text = ""
        btn_text = "View..."
        text_info = [title_text, content_text, btn_text]
        Test._plugin_version = JuUpdateNotification(parent=Test, text_info=text_info)
        Test._plugin_version.adjustSize()
        Test._plugin_version.hide()
        self.tree_(Test=Test)
        self.tab_new_(Test=Test)

    # 初始化dock
    def init_dock(self, Test=None):

        Test.bottom_log_show = LogEdit()
        Test.bottom_log_show_test = LogEdit()
        Test.bottom_log_show.moveCursor(QTextCursor.End)
        Test.bottom_log_show.setReadOnly(True)
        Test.bottom_log_show_test.setReadOnly(True)
        Test.bottom_log_show_test.setVisible(False)
        Test.bottom_log_show_test.moveCursor(QTextCursor.End)
        Test.bottom_log_show_test.setMaximumBlockCount(500)
        Test.bottom_log_show.setMaximumBlockCount(500)
        # Test.tab1 = QTextEdit()
        # gridLayout_111 = QVBoxLayout(Test.tab1)
        # gridLayout_111.setSpacing(0)
        # gridLayout_111.setObjectName(u"gridLayout_111-")
        # gridLayout_111.setContentsMargins(0, 0, 0, 0)
        #
        # Test.tab1.setObjectName(u"tab1")
        # Test.tab_widget1.addTab(Test.tab1, "project file1")
        # # Test.horizontalLayout_2 = QHBoxLayout(self.tab)
        # # self.tab.setColumnCount(2)
        #
        # label_name = QLabel('可用插件')
        # label_name.setMaximumHeight(30)
        # label_name.setAlignment(Qt.AlignCenter)
        # label_name.setStyleSheet(u"\n"
        #                          "font: 12pt \"\u963f\u91cc\u5df4\u5df4\u666e\u60e0\u4f53 M\";color: #8EBABA")
        # Test.listWidget1 = QListWidget()
        #
        # Test.listWidget1.setObjectName(u"tab")
        # test_item = QListWidgetItem('test')
        # test_item.setTextAlignment(Qt.AlignCenter)
        # test_item.setFont(QFont('\"\u963f\u91cc\u5df4\u5df4\u666e\u60e0\u4f53 M\"', 12))
        # self.listWidget.addItem(test_item)

        Test.tab1_1 = QWidget()
        verticalLayout = QVBoxLayout(Test.tab1_1)
        verticalLayout.setSpacing(0)
        verticalLayout.setObjectName(u"gridLayout")
        verticalLayout.setContentsMargins(0, 0, 0, 0)
        # verticalLayout.addWidget(label_name)
        # verticalLayout.addWidget(Test.listWidget1)
        # verticalLayout.set

        # Test.tab_widget1.addTab(Test.tab1_1, "project name")
        # Test.tab_widget1.setTabPosition(QTabWidget.TabPosition.North)
        # Test.tabbtn = QPushButton()
        # Test.tabbtn.setFixedWidth(20)
        # Test.tabbtn.setStyleSheet("QPushButton{border-image: url(../../JuResource/img/min_3.png)};"
        #                           "QPushButton:hover{background-color: #3C3F41}")
        # # self.tabbtn.setStyleSheet("QPushButton{background-color: #4C5052}")
        # Test.bottom_log_show.setCornerWidget(Test.tabbtn)
        v_layot = QVBoxLayout()
        v_layot.setSpacing(0)
        v_layot.setObjectName(u"gridLayout_111-")
        v_layot.setContentsMargins(0, 0, 0, 0)
        Test.bottom_widget = QWidget()
        v_layot.addWidget(Test.bottom_log_show)
        v_layot.addWidget(Test.bottom_log_show_test)
        Test.tab_bottom = JuBottomWidget()
        v_layot.addWidget(Test.tab_bottom)
        Test.bottom_widget.setLayout(v_layot)
        Test.Dockable_1 = QDockWidget('Dockable', Test)
        Test.Dockable_1.setTitleBarWidget(QWidget())
        Test.Dockable_2 = QDockWidget('Dockable1', Test)
        Test.Dockable_2.setTitleBarWidget(QWidget())
        Test.Dockable_3 = QDockWidget('Dockable3', Test)
        Test.Dockable_4 = QDockWidget('Dockable4', Test)
        Test.Dockable_3.setTitleBarWidget(QWidget())
        Test.Dockable_4.setTitleBarWidget(QWidget())
        Test.Dockable_1.setWidget(Test.left_widget)
        Test.Dockable_2.setWidget(Test.bottom_widget)
        Test.Dockable_3.setWidget(Test.device_widget_)
        Test.Dockable_4.setWidget(Test.ip_widget)
        Test.Dockable_1.setMaximumWidth(450)
        Test.Dockable_1.setMinimumWidth(150)
        Test.Dockable_2.setMaximumHeight(500)
        Test.Dockable_4.setMinimumWidth(100)
        Test.Dockable_3.setMaximumWidth(300)
        Test.Dockable_1.setFloating(False)
        Test.Dockable_2.setFloating(False)
        Test.Dockable_3.setFloating(False)
        Test.Dockable_4.setFloating(False)
        Test.Dockable_1.setFeatures(QDockWidget.NoDockWidgetFeatures)
        Test.Dockable_2.setFeatures(QDockWidget.NoDockWidgetFeatures)
        Test.Dockable_3.setFeatures(QDockWidget.NoDockWidgetFeatures)
        Test.Dockable_4.setFeatures(QDockWidget.NoDockWidgetFeatures)
        Test.addDockWidget(Qt.LeftDockWidgetArea, Test.Dockable_1)
        Test.addDockWidget(Qt.BottomDockWidgetArea, Test.Dockable_2)
        Test.addDockWidget(Qt.BottomDockWidgetArea, Test.Dockable_3)
        Test.addDockWidget(Qt.RightDockWidgetArea, Test.Dockable_4)
        Test.Dockable_4.setVisible(False)

    # 底部bar
    def bottom_bar(self, Test=None):
        Test.label0 = QLabel()
        Test.statuBar = QStatusBar(Test)

        Test.setStatusBar(Test.statuBar)
        Test.project_label_loc = QLabel()
        Test.statuBar.addWidget(Test.project_label_loc)
        Test.statuBar.addPermanentWidget(Test.label0)

    # 初始化顶部菜单栏
    def menu_init(self, Test=None):
        Test.setContextMenuPolicy(Qt.CustomContextMenu)
        Test.bar = Test.menuBar()
        # 创建主菜单file，在其中添加子菜单
        Test.file = Test.bar.addMenu('文件')
        new = Test.file.addMenu('New')
        new.addAction('New Project')
        # new.addAction('New Plugin')
        Test.file.addAction('Open Project')
        # Test.open_recent = Test.file.addMenu('Open Recent Project')
        Test.file.addAction('Save')
        Test.file.addAction('Save Project As')
        Test.file.addAction('Quit')
        # Test.file.addAction('Setting')
        # self.file.triggered[QAction].connect(self.File)

        Test.Edit_ = Test.bar.addMenu('编辑')
        Test.Edit_.addAction('撤销')
        Test.Edit_.addAction('查找')
        Test.Edit_.addAction('替换')
        # self.Edit_.triggered[QAction].connect(self.Edit)

        Test.plugin = Test.bar.addMenu('插件')
        Test.plugin.addAction('Python Package')
        Test.plugin.addAction('Platform Plugin')
        Test.plugin.addAction('Import Plugin')
        # self.plugin.triggered[QAction].connect(self.Plugin)
        Test.help = Test.bar.addMenu('帮助')
        Test.help.addAction('About')
        Test.help.addAction('Check update')
        # self.help.triggered[QAction].connect(self.Help)

    def tree_(self, Test=None):
        Test.tree = JuQTreeWidget()
        # Test.tree.header().setHidden(True)
        # Test.tree.header().setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        # Test.tree.header().setSectionResizeMode(QHeaderView.ResizeToContents)
        # Test.tree.header().setStretchLastSection(False)
        # Test.tree.setTextElideMode(Qt.ElideNone)
        Test.gridLayout_111.addWidget(Test.tree)
        # 设置列数
        Test.tree.setColumnCount(2)
        Test.tree.hideColumn(1)
        # 设置树形控件头部的标题
        Test.tree.setHeaderLabels(['Key', 'Value'])
        Test.tree.setContextMenuPolicy(Qt.CustomContextMenu)  # 打开右键菜单的策略

        # 设置树形控件的列的宽度
        Test.tree.setColumnWidth(0, 150)
        Test.tree.expandAll()
        Test.tree.setHeaderHidden(True)

    def add_toolbar(self, Test=None):
        Test.tb = Test.addToolBar("top")
        Test.tb.setStyleSheet(u"border-bottom: 1px solid #515151")
        Test.tb.setMovable(False)
        Test.spacerWidget = QWidget(Test)
        Test.spacerWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        Test.tb.addWidget(Test.spacerWidget)
        Test.tb.setIconSize(QSize(15, 15))
        new = QAction(QIcon("./JuResource/img/run.png"), "run", Test)
        # Test.tb.addWidget(new)
        Test.tb.addAction(new)
        # reload = QAction(QIcon("./JuResource/img/reload.png"), "reload plugin", Test)
        # tb.addAction(reload)
        # 添加第二个action  参数分别是 图片， 名字(可以理解给这个action起个名字)，上下文
        open = QAction(QIcon("./JuResource/img/stop.png"), "stop", Test)
        Test.tb.addAction(open)

        # save = QAction(QIcon("./main/resource/img/stop.png"), "save", self)
        # tb.addAction(save)
        # ation一般是用这个作为绑定的点击事件 注意方括号里面的QAction
        # tb.actionTriggered[QAction].connect(self.toolbtnpressed)

        # Test.spacerWidget = QWidget(Test)
        # Test.spacerWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        # tb.addWidget(Test.spacerWidget)


    def tab_new_(self, Test=None):
        # Test.center_widget = QWidget()
        # Test.center_widget.setObjectName(u"center_widget")
        Test.tab_widget_new = QTabWidget(Test)
        Test.gridLayout_center.addWidget(Test.tab_widget_new)
        Test.tab_widget_new.setTabsClosable(True)
        Test.tab_widget_new.setVisible(False)

    def close_(self):
        self.parent.close()

#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     win = QMainWindow()
#     Ju_Ui_Main(parent=win)
#     win.show()
#     sys.exit(app.exec_())
