#!/usr/bin/env python3
# -*- coding: utf-8 -*-

r"""
"""
__author__ = "Jiang Jun"

import time
from multiprocessing import Queue
from os import makedirs, path, listdir, sep, walk, getcwd, mkdir, system
from shutil import rmtree, copyfile
from threading import Thread
from zipfile import ZipFile, ZIP_DEFLATED
from copy import deepcopy
from json import loads, dumps
from qdarkstyle import load_stylesheet_pyside2
from JuControl.ju_software_update import JuDeviceUi
from JuLog.ju_logger_queue import JuLogger
from win32clipboard import OpenClipboard, GetClipboardData, CF_HDROP, CloseClipboard
from JuControl.ju_import_ui import JuUploadPlugin
from JuControl.ju_sql_info import JuSqlInfo
from JuControl.notification import notification
# from JuFileOperate.ju_file_reader import JuFileRead
# from JuQueue.ju_queue_manage import Ju_Process_Manage
from JuControl.ju_about_ui import JuAboutDialog
from qtpyeditor import PMGPythonEditor
from ju_cfg import JuConfig
from PySide2.QtCore import QObject, QTimer, Qt, Signal, QPoint, QCoreApplication, QThread
from PySide2.QtGui import QCursor, QTextCharFormat, QColor
from PySide2.QtWidgets import QAction, QTreeWidget, QMenu, QTreeWidgetItem, QMessageBox, QTabWidget, QWidget, \
    QVBoxLayout, QFileDialog, QApplication
from subprocess import Popen, STDOUT, PIPE
from psutil import pids, Process
from JuControl.ju_new_file import NewProject
from JuControl.ju_right_bottom_widget import Ju_Right_Bottom
from JuControl.ju_qss_set import Ju_Qss_Set
# from JuScoket.ju_scoket_server import Ju_Socket_Manage_Server
from JuNodeEditor.calc_window import CalculatorWindow
from JuQueue.ju_run_manage import Ju_Run_Manage


class Test_Ui_Thread(QThread):

    def __init__(self, parent, log=None):
        super(Test_Ui_Thread, self).__init__()
        self.parent = parent
        self._user_logger = log

    def run(self):
        while 1:
            if not self.parent.deal_receive.empty():
                msg = self.parent.deal_receive.get()
                if isinstance(msg, dict) is True and hasattr(self, msg.get("func")) is True:
                    getattr(self, msg.get("func"))(*msg.get("args", ()), **msg.get("kwargs", {}))
            # print(2)
            time.sleep(0.00001)

    def ui_log(self, text):
        self._user_logger.info(text)

    def set_thread_run(self, flag):
        self.parent.thread_run = flag

    def closeEvent(self):
        self.terminate()  # 结束此进程
        self.wait()  # 等待结束完成
        if self.isFinished():  # 如果当前线程已经完成工作，则删除
            del self

class Ju_Test_Ui_Fuc(QWidget):
    update_msg = Signal(int)
    s_test_log = Signal(str)

    def __init__(self, parent=None, deal_receive=None, deal_send=None, person_type=None, new_ui_test=None):
        super(Ju_Test_Ui_Fuc, self).__init__()
        self.ui_break = False
        # consumer_receive = Queue()
        # producer_send = Queue()
        # p = Ju_Process_Manage(receive=producer_send, send=consumer_receive)
        # p.daemon = True
        # p.start()
        self.python_path = None
        self.file_name = None
        self.parent = parent
        self._user_logger = JuLogger("user_log")
        self._test_logger = JuLogger("test_log")
        self.CalculatorWindow = CalculatorWindow(log=self._user_logger)
        # self.CalculatorWindow.set_log(self._user_logger)
        self.deal_receive = deal_receive
        self.deal_send = deal_send
        self.person_type = person_type
        self.Test_Ui_Thread = Test_Ui_Thread(self, log=self._user_logger)
        self.Test_Ui_Thread.start()
        self.thread_run = False
        self._right_bottom_info = Ju_Right_Bottom(parent=self)
        self._ui_base = new_ui_test
        self.init_parameter()
        self._init_ui()

        self._set_qss()
        self.setStyleSheet(load_stylesheet_pyside2())
        # self.setStyleSheet(JuFileRead.read_file(u"./JuResource/2.qss"))
        self.drag_list()
        self._tree_device()
        # self.deal_send.put({"func": "upload_login_record", "args": (self.person_type, )})
        #
        # ju_socket_manage = Ju_Run_Manage(receive=self.deal_receive)
        # ju_socket_manage.daemon = True
        # ju_socket_manage.start()
        # self._ui_base._plugin_version.win_show()
        # self._ui_base.setStyleSheet(JuFileRead.read_file(u"./JuResource/2.qss"))
        # self._test_show()
        # print(self._ui_base._plugin_version.a)

    def _test_show(self):
        # widget = QWidget()
        _Layout = QVBoxLayout(self._ui_base.text_)
        _Layout.setContentsMargins(0, 0, 0, 0)
        _Layout.setSpacing(0)
        _Layout.addWidget(self.CalculatorWindow.getCurrentNodeEditorWidget())

    def drag_list(self):
        self._Layout = QVBoxLayout(self._ui_base.ip_widget)
        self._Layout.setContentsMargins(0, 0, 0, 0)
        self._Layout.setSpacing(0)
        self._Layout.addWidget(self.CalculatorWindow.nodesListWidget)

    def _init_ui(self):
        self._bind_event()
        if self.person_type == "teacher":
            self.socket_receive = Queue()
            self.socket_send = Queue()
            # ju_socket_manage = Ju_Socket_Manage_Server(receive=self.socket_receive, send=self.socket_send)
            # ju_socket_manage.daemon = True
            # ju_socket_manage.start()
            q_receive = Thread(target=self.queue_receive, args=())
            q_receive.start()
            self._right_bottom_info.info_show(text="欢迎回来，感谢使用", timeout=20)
        self.text_all = {}
        self.recent_get_project()
        self._save_flag = True
        self.new_project = False
        self.save_file_flag = False
        self._update_exe_flag = True
        self.flag_recent = False
        update_sql_Thread = Thread(target=self._update_test_log_function)
        update_sql_Thread.start()
        self.path_python()
        # q_receive1 = Thread(target=self._test_, args=())
        # q_receive1.start()
        # self.tab_new_()

    def path_python(self):
        python_path = JuConfig.CURRENT_FILE_PATH + '/python/python.exe'
        if path.exists(python_path):
            self.python_path = python_path
            self._ui_base.tab_bottom.btn3.setToolTip(str(python_path))

    def init_parameter(self):
        self.text_all = {}
        self._select_btn_text = "btn1"

    def _set_qss(self):
        self.qss = Ju_Qss_Set(parent=self._ui_base, ui=self.CalculatorWindow)
        self.qss.ju_qss_set_one()

    def queue_receive(self):
        while True:
            if self.ui_break:
                break
            else:
                if not self.socket_receive.empty():
                    msg = self.socket_receive.get(timeout=0.1)
                    self._user_logger.info(msg)
            time.sleep(0.1)
            # logger.debug(msg)

    def _bind_event(self):
        self._ui_base.tab_bottom.btn3.setStyleSheet("background-color:#2D2F30;color:#FFFFFF")
        self._ui_base.file.triggered[QAction].connect(self._File)
        self._ui_base.Edit_.triggered[QAction].connect(self._Edit)
        self._ui_base.plugin.triggered[QAction].connect(self._Plugin)
        self._ui_base.help.triggered[QAction].connect(self._Help)
        self._ui_base.tab_bottom.btn1.mouse_enter_leave.connect(self.bottom_label_css)
        self._ui_base.tab_bottom.btn2.mouse_enter_leave.connect(self.bottom_label_css)
        self._ui_base.tab_bottom.btn1.mylabelSig.connect(self.tab_bottom_btn_click)
        self._ui_base.tab_bottom.btn2.mylabelSig.connect(self.tab_bottom_btn_click)
        self._ui_base.tree.customContextMenuRequested.connect(self.show_context_menu)  # 绑定事件
        self._ui_base.tree.doubleClicked.connect(self.treeonClicked)
        self.update_msg.connect(self._update_exe_info)
        self._ui_base.tab_widget_new.tabCloseRequested.connect(self.close_tab)
        self._user_logger.s_log.connect(self._ui_log_display)
        self.s_test_log.connect(self._test_log_display)
        self._ui_base.bottom_log_show.press_log.connect(self.press_log)
        self._ui_base.bottom_log_show_test.press_log.connect(self.press_log_test)
        self._ui_base.tree.tree_copy.connect(self.Copy_File)
        self._ui_base.tree.tree_paste.connect(self.Paste_File)
        self._ui_base.btn_connect_device.clicked.connect(self.btn_connect_device)
        self._ui_base.btn_disconnect_device.clicked.connect(self.btn_disconnect_device)
        self._ui_base.tb.actionTriggered[QAction].connect(self.toolbtnpressed)
        self._ui_base.tab_bottom.btn2.hide()

    def btn_connect_device(self):
        # self.CalculatorWindow.Auto_Pack.auto_get_device_class_new()
        dic = self.CalculatorWindow.Auto_Pack.show_device()
        self._ui_base.treeWidget_device_info.device_info_show(device_init_info=dic,
                                                              init_flag=False)
        self._ui_base.treeWidget_device_info.device_info_show(device_init_info=dic,
                                                              init_flag=True)
        self.CalculatorWindow.Auto_Pack.ip_device_reconnect()
        self.CalculatorWindow.nodesListWidget.reconnect_item()
        self._user_logger.info("重新加载插件成功")

    def btn_disconnect_device(self):
        self._ui_base.treeWidget_device_info.device_info_show(device_init_info={},
                                                              init_flag=True)

    def _tree_device(self):
        dic = self.CalculatorWindow.Auto_Pack.show_device()
        self._ui_base.treeWidget_device_info.device_info_show(device_init_info=dic,
                                                              init_flag=True)

    def toolbtnpressed(self, a):
        # self.ui_log_show("pressed tool button is " + a.text())
        index = self._ui_base.tab_widget_new.currentIndex()
        value = self._ui_base.tab_widget_new.tabText(index)
        # self.ui_log_show(value)
        if a.text() == 'run':
            if self.thread_run is False:
                if '.py' in value:
                    if self.python_path is not None:
                        self.text_all[value].save()
                        self._user_logger.info("进程启动中······")
                        self.ju_run_manage = Ju_Run_Manage(receive=self.deal_receive, python_path=self.python_path,
                                                           file_path=value)
                        self.ju_run_manage.start()
                        print(self.ju_run_manage.pid)
                        self.thread_run = True
                    else:
                        self._user_logger.info("python path don't exist")
                else:
                    self._user_logger.info("请选择py文件！！")
                    # QMessageBox.critical(self, "error", "请选择py文件！！")
            else:
                self._user_logger.info("{}正在运行".format(value.split('/')[-1]))
                # self.ui_log_show("{}正在运行".format(value.split('/')[-1]))
        elif a.text() == 'stop':
            if self.thread_run:

                process = 'C:/Windows/System32/taskkill /f /pid %s' % self.ju_run_manage.pid
                system(process)
                self._user_logger.info("文件结束运行")
                self.thread_run = False

    def _ui_log_display(self, log):
        color_format = self._set_log_color(log)
        self._ui_base.bottom_log_show.setCurrentCharFormat(color_format)
        self._ui_base.bottom_log_show.appendPlainText(log)

    def _test_log_display(self, log):
        color_format = self._set_log_color(log)
        self._ui_base.bottom_log_show_test.setCurrentCharFormat(color_format)
        self._ui_base.bottom_log_show_test.appendPlainText(log)

    def _set_log_color(self, log):
        color_format = QTextCharFormat()
        if "ERROR" in log:
            color_format.setForeground(QColor(255, 96, 74))
        else:
            color_format.setForeground(QColor(177, 180, 179))
        return color_format

    def _update_test_log_function(self):
        while True:
            test_log_msg = self._test_logger.msg_queue_get()
            if test_log_msg is not None:
                if self.ui_break:
                    break
                else:
                    self._test_log_display(test_log_msg)
            time.sleep(0.05)

    def log_menu_generate(self, mouse_x, mouse_y):
        project_menu = QMenu(self._ui_base.bottom_widget)
        # project_menu.addAction(QIcon(u"AwResource/select_all.png"), "Select All")
        # project_menu.addAction(QIcon(self._icon_copy), "Copy")
        # project_menu.addAction(QIcon(self._icon_delete), "Delete All")
        project_menu.addAction("Select All")
        project_menu.addAction("Copy")
        project_menu.addAction("Delete All")
        # self.seq_tree_widget.mapToGlobal(QPoint(mouse_x, mouse_y))
        current_action = project_menu.exec_(self._ui_base.bottom_widget.mapToGlobal(QPoint(mouse_x, mouse_y)))
        result = "" if current_action is None else current_action.text()
        return result

    def press_log(self, mouse_x, mouse_y):
        self._test_logger.error("====")
        menu_select = self.log_menu_generate(mouse_x, mouse_y)
        if menu_select == "Copy":
            self._ui_base.bottom_log_show.copy()
        elif menu_select == "Select All":
            self._ui_base.bottom_log_show.selectAll()
        elif menu_select == "Delete All":
            self._ui_base.bottom_log_show.clear()

    def press_log_test(self, mouse_x, mouse_y):
        self._test_logger.error("====1")
        menu_select = self.log_menu_generate(mouse_x, mouse_y)
        if menu_select == "Copy":
            self._ui_base.bottom_log_show_test.copy()
        elif menu_select == "Select All":
            self._ui_base.bottom_log_show_test.selectAll()
        elif menu_select == "Delete All":
            self._ui_base.bottom_log_show_test.clear()

    def _bind_qtimer(self):
        timer = QTimer(self)
        timer.timeout.connect(self.showtime)
        timer.start(1000)

    def _File(self, q):
        if q.text() == "New Project":
            self.Project_new()
        elif q.text() == "Open Project":
            fileName1, filetype = QFileDialog.getOpenFileName(self,
                                                              "选取文件",
                                                              "E:/",
                                                              "jmszs (*.jmszs)")  # 设置文件扩展名过滤,注意用双分号间隔
            # self.ui_log_show(fileName1)
            if fileName1 == '':
                pass
            else:
                self.open_project_url(fileName1)
        elif q.text() == 'Save':
            self.Project_save()

        elif q.text() == "Save Project As":
            if self._save_flag:
                fileName1, filetype = QFileDialog.getSaveFileName(self,
                                                                 "选取文件",
                                                                 "C:/",
                                                                 "jmszs (*.jmszs)")  # 设置文件扩展名过滤,注意用双分号间隔
                # self.ui_log_show(fileName1)
                if fileName1 == '':
                    pass
                else:
                    self.Project_Save_As(file=fileName1)
        elif q.text() == "Quit":
            self.parent.close()
            # self.Project_save()
        elif q.text() == "New Plugin":
            print(2)
        self._user_logger.info(q.text())

    def _Edit(self, q):
        self._user_logger.info(q.text())

    def _Plugin(self, q):
        self._user_logger.info(q.text())
        if q.text() == "Platform Plugin":
            install_win = JuDeviceUi(self)
            install_win.exec_()
            if install_win.install_flag:
                self.CalculatorWindow.Auto_Pack.ip_device_reconnect()
                self.CalculatorWindow.nodesListWidget.reconnect_item()
        elif q.text() == "Import Plugin":
            install_win = JuUploadPlugin(self, log=self._user_logger)
            install_win.exec_()
        elif q.text() == "Python Package":
            pass

    def _Help(self, q):
        if q.text() == "Check update":
            QMessageBox.information(self, "Info", '正在开发中.', QMessageBox.Ok)
            # if self._update_exe_flag:
            #     self._update_exe_flag = False
                # _update_v3_exe = Thread(target=self._update_v3_exe)
                # _update_v3_exe.start()
        elif q.text() == "About":
            install_win = JuAboutDialog(self)
            install_win.exec_()
        self._user_logger.info(q.text())

    def _update_v3_exe(self):
        ver = JuConfig.VERSION
        flag = False
        if JuSqlInfo.sql_connect():
            try:
                pl = pids()
                for pid in pl:
                    if Process(pid).name() == "manage_platform_v3_update.exe":
                        flag = True
            except Exception:
                pass
            if flag is False:
                exe_order = "--version {} --user {} --password {} --host {} --database {}" \
                    .format(ver, JuConfig.MYSQL_USER, JuConfig.MYSQL_PASSWORD, JuConfig.MYSQL_HOST,
                            JuConfig.MYSQL_DATABASE)
                file_path = getcwd() + "/" + "manage_platform_v3_update.exe"
                if path.exists(file_path):
                    self.update_msg.emit(1)
                    Popen(file_path + " " + exe_order, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
            #     else:
            #         self.update_msg.emit(3)
            # else:
            #     self.update_msg.emit(3)
        else:
            self.update_msg.emit(4)
        self._update_exe_flag = True

    def _update_exe_info(self, num):
        if num == 1:
            notification("Info", "Program is starting.")
        # elif num == 2:
        #     QMessageBox.warning(self, "Info", 'program is downloading.', QMessageBox.Ok)
        # elif num == 3:
        #     QMessageBox.warning(self, "Info", 'Update program is developing.', QMessageBox.Ok)
        elif num == 4:
            QMessageBox.warning(self, "Error", 'Please connect to the network.', QMessageBox.Ok)
        # elif num == 5:
        #     QMessageBox.warning(self, "Error", 'Program download failed.', QMessageBox.Ok)

    def showtime(self):
        """
        显示时间
        """
        self._ui_base.label0.setText("     " + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))

    def bottom_label_css(self, flag, object_name):
        if self._select_btn_text == "btn1":
            if object_name == "btn1":
                self._ui_base.tab_bottom.btn1.setStyleSheet(
                    "background-color:#2D2F30;color:#FFFFFF;margin-left: 15px"
                )
                self._ui_base.tab_bottom.btn2.setStyleSheet(
                    "background-color:#3C3F41;color:#FFFFFF"
                )
            else:
                if flag:
                    self._ui_base.tab_bottom.btn1.setStyleSheet(
                        "background-color:#2D2F30;color:#FFFFFF;margin-left: 15px"
                    )
                    self._ui_base.tab_bottom.btn2.setStyleSheet(
                        "background-color:#353739;color:#FFFFFF"
                    )
                else:
                    self._ui_base.tab_bottom.btn1.setStyleSheet(
                        "background-color:#2D2F30;color:#FFFFFF;margin-left: 15px"
                    )
                    self._ui_base.tab_bottom.btn2.setStyleSheet(
                        "background-color:#3C3F41;color:#FFFFFF"
                    )
        elif self._select_btn_text == "btn2":
            if object_name == "btn2":
                self._ui_base.tab_bottom.btn2.setStyleSheet(
                    "background-color:#2D2F30;color:#FFFFFF"
                )
                self._ui_base.tab_bottom.btn1.setStyleSheet(
                    "background-color:#3C3F41;color:#FFFFFF;margin-left: 15px"
                )
            else:
                if flag:
                    self._ui_base.tab_bottom.btn2.setStyleSheet(
                        "background-color:#2D2F30;color:#FFFFFF"
                    )
                    self._ui_base.tab_bottom.btn1.setStyleSheet(
                        "background-color:#353739;color:#FFFFFF;margin-left: 15px"
                    )
                else:
                    self._ui_base.tab_bottom.btn2.setStyleSheet(
                        "background-color:#2D2F30;color:#FFFFFF"
                    )
                    self._ui_base.tab_bottom.btn1.setStyleSheet(
                        "background-color:#3C3F41;color:#FFFFFF;margin-left: 15px"
                    )

    def tab_bottom_btn_click(self, text):
        if text == "btn1":
            if self._select_btn_text != "btn1":
                self._ui_base.bottom_log_show.setVisible(True)
                self._ui_base.bottom_log_show_test.setVisible(False)
                self._select_btn_text = "btn1"
                self._ui_base.tab_bottom.btn1.setStyleSheet(
                    "background-color:#2D2F30;color:#FFFFFF;margin-left: 15px"
                )
                self._ui_base.tab_bottom.btn2.setStyleSheet(
                    "background-color:#3C3F41;color:#FFFFFF"
                )
        elif text == "btn2":
            if self._select_btn_text != "btn2":
                self._ui_base.bottom_log_show.setVisible(False)
                self._ui_base.bottom_log_show_test.setVisible(True)
                self._select_btn_text = "btn2"
                self._ui_base.tab_bottom.btn2.setStyleSheet(
                    "background-color:#2D2F30;color:#FFFFFF"
                )
                self._ui_base.tab_bottom.btn1.setStyleSheet(
                    "background-color:#3C3F41;color:#FFFFFF;margin-left: 15px"
                )

    # 找到选中的item位置及内容
    def find_item(self, value):
        item_list = self._ui_base.tree.findItems(value, Qt.MatchExactly | Qt.MatchRecursive,
                                                 column=1)
        # self.ui_log_show(item_list)
        if len(item_list) > 0:
            # self.ui_log_show('111')
            item = item_list[0]
            return item

    # 新增tree节点
    def tree_item1(self, item, name, value):
        child1 = QTreeWidgetItem(item)
        child1.setText(0, name)
        child1.setText(1, value)

    def show_context_menu(self, pos):
        menu = QMenu(self._ui_base)
        item = self._ui_base.tree.currentItem()
        if item is None:
            pass
        else:
            # action = menu.addAction('Copy')
            # action.triggered.connect(...)
            # action.triggered.connect(self.Copy_File)
            # action = menu.addAction('Rename')
            # action.triggered.connect(self.Rename_File)
            # action = menu.addAction('Delete')
            # action.triggered.connect(self._delete)
            # self.ui_log_show('Key=%s,value=%s' % (item.text(0), item.text(1)))
            if '.' in item.text(0):
                action = menu.addAction('Copy')
                # action.triggered.connect(...)
                action.triggered.connect(self.Copy_File)
                action = menu.addAction('Rename')
                # action.triggered.connect(self.Rename_File)
                action = menu.addAction('Delete')
                # action.triggered.connect(self._delete)
            elif '.' not in item.text(0):
                action = menu.addAction('New File')
                action.triggered.connect(self.File_New)
                action = menu.addAction('New Folder')
                action.triggered.connect(self.Folder_New)
                action = menu.addAction('Paste')
                action.triggered.connect(self.Paste_File)
                action = menu.addAction('Copy')
                action.triggered.connect(self.Copy_File)
                action = menu.addAction('Rename')
                # action.triggered.connect(self.Rename_File)
                if item.text(1) != 'Project_Project':
                    action = menu.addAction('Delete')
                    # action.triggered.connect(self._delete)
                if item.text(1) == 'Project_Project':
                    action = menu.addAction('New Plugin')
                    # action.triggered.connect(self._delete)
                # action.triggered.connect(...)
            menu.exec_(QCursor.pos())

    def Folder_New(self):
        url = self.file_url()
        # print(url)
        # print(base_loc + '/' + url + '/')
        item = self._ui_base.tree.currentItem()
        new_project_win = NewProject(self, flag=4, tree=item)
        new_project_win.exec_()
        if new_project_win.get_create_success_flag() is True:
            name = new_project_win.lineEdit.text()
            if item.text(1) == 'Project_Project':
                self.tree_item1(self.root, name, name)
                mkdir(JuConfig.RECENT_PROJECT_PATH + '/' + name)
            else:
                self.tree_item1(item, name, name)
                mkdir(JuConfig.RECENT_PROJECT_PATH + '/' + url + '/' + name)

    def File_New(self):
        url = self.file_url()
        # print(url)
        item = self._ui_base.tree.currentItem()
        if item is None:
            pass
        else:
            # self.ui_log_show('Key=%s,value=%s' % (item.text(0), item.text(1)))
            # if item.text(1) == 'Project_Project':
            #     QMessageBox.critical(self, "error", "主节点不能新建文件")
            # else:
            new_project_win = NewProject(self, flag=1)
            new_project_win.exec_()
            if new_project_win.get_create_success_flag() is True:
                name = new_project_win.file_name
                if ".py" in name:
                    with open(JuConfig.RECENT_PROJECT_PATH + "/" + url + "/" + name, "w") as f:  # 打开文件
                        f.write("#!/usr/bin/env python\n")
                        f.write("# -*- coding: utf-8 -*-\n")
                        f.write("\n\n\n\n")
                    # item = self.find_item(item.text(1))
                    # self.tree_item1(item, name, item.text(1) + '/' + name)
                elif ".juncfg" in name:
                    a = self.CalculatorWindow.createMdiChild(file=JuConfig.RECENT_PROJECT_PATH +
                                                                  "/" + url + "/" + name)
                    del a
                else:
                    with open(JuConfig.RECENT_PROJECT_PATH + "/" + url + "/" + name, "w") as f:  # 打开文件
                        pass
                item = self.find_item(item.text(1))
                self.tree_item1(item, name, item.text(1) + '/' + name)

    def Copy_File(self):
        item = self._ui_base.tree.currentItem()
        if item is None:
            pass
        else:
            if item.text(1) == 'Project_Project':
                QMessageBox.critical(self, "error", "主节点复制")
            else:
                path = JuConfig.RECENT_PROJECT_PATH + '/' + item.text(1)
                # print(path)
                args = ['powershell', 'Get-Item {} | Set-Clipboard'.format(path)]
                Popen(args=args)

    def readClipboardFilePaths(self):
        OpenClipboard()
        try:
            res = True, GetClipboardData(CF_HDROP)
        except Exception:
            res = False, None
        finally:
            CloseClipboard()
        return res

    def Paste_File(self):
        flag = 0
        item = self._ui_base.tree.currentItem()
        if item is None:
            pass
        else:
            # try:
            _, folder_name = self.readClipboardFilePaths()
            if _:
                for a1 in folder_name:
                    a1 = a1.replace("\\", "/")
                    # a1 = a1.split('/')
                    if '.' in a1.split('/')[-1]:
                        if item.text(1) == 'Project_Project':
                            for i in range(item.childCount()):
                                if item.child(i).text(0) == a1.split('/')[-1]:
                                    flag = 1
                                    new_project_win = NewProject(self, flag=3, tree=item)
                                    new_project_win.exec_()
                                    if new_project_win.get_create_success_flag() is True:
                                        name = new_project_win.lineEdit.text()
                                        flag = 2
                                        break
                                    else:
                                        break
                            if flag == 2:
                                src_dir = a1
                                dst_dir = JuConfig.RECENT_PROJECT_PATH + '/' + name
                                copyfile(src_dir, dst_dir)
                                self.tree_item1(self.root, name, name)
                            elif flag == 0:
                                src_dir = a1
                                dst_dir = JuConfig.RECENT_PROJECT_PATH + '/' + src_dir.split('/')[-1]
                                copyfile(src_dir, dst_dir)
                                self.tree_item1(self.root, (src_dir.split('/')[-1]),
                                                src_dir.split('/')[-1])
                            elif flag == 1:
                                QMessageBox.critical(self, "error", "文件复制失败")
                        elif '.' in item.text(1):
                            QMessageBox.critical(self, "error", "文件下不能存放文件")
                        else:
                            for i in range(item.childCount()):
                                if item.child(i).text(0) == a1.split('/')[-1]:
                                    new_project_win = NewProject(self, flag=3, tree=item)
                                    new_project_win.exec_()
                                    flag = 1
                                    if new_project_win.get_create_success_flag() is True:
                                        name = new_project_win.lineEdit.text()
                                        flag = 2
                                        break
                                    else:
                                        break
                            if flag == 2:
                                src_dir = a1
                                dst_dir = JuConfig.RECENT_PROJECT_PATH + '/' + item.text(1) + '/' + name
                                copyfile(src_dir, dst_dir)
                                item = self.find_item(item.text(1))
                                self.tree_item1(item, (name), item.text(1) + '/' + name)
                            elif flag == 0:
                                src_dir = a1
                                dst_dir = JuConfig.RECENT_PROJECT_PATH + '/' + item.text(1) + '/' + src_dir.split('/')[
                                    -1]
                                copyfile(src_dir, dst_dir)
                                item = self.find_item(item.text(1))
                                self.tree_item1(item, (src_dir.split('/')[-1]),
                                                item.text(1) + '/' + src_dir.split('/')[-1])
                            elif flag == 1:
                                QMessageBox.critical(self, "error", "文件复制失败")
                    else:
                        if item.text(1) == 'Project_Project':
                            for i in range(item.childCount()):
                                if item.child(i).text(0) == a1.split('/')[-1]:
                                    new_project_win = NewProject(self, flag=3, tree=item)
                                    new_project_win.exec_()
                                    flag = 1
                                    if new_project_win.get_create_success_flag() is True:
                                        name = new_project_win.lineEdit.text()
                                        flag = 2
                                        break
                                    else:
                                        break
                            if flag == 2:
                                src_dir = a1
                                dst_dir = JuConfig.RECENT_PROJECT_PATH + '/' + name + '/'
                                # print('src_dir1', src_dir)
                                # print('dst_dir1', dst_dir)
                                self.copy_demo(src_dir, dst_dir)
                                dic_all = self.get_config_dirs(dst_dir)
                                # print(dic_all)
                                # item = self.find_item(item.text(1))
                                self.tree_item1(self.root, (name),
                                                name)
                                item = self.find_item(name)
                                for i in range(len(dic_all['files'])):
                                    self.tree_item1(item, dic_all['files'][i],
                                                    name + '/' + dic_all['files'][i])
                                self.loc_search = dst_dir
                                self.get_key_copy(dic_all['child_dirs'], item)
                            elif flag == 0:
                                src_dir = a1
                                dst_dir = JuConfig.RECENT_PROJECT_PATH + '/' + src_dir.split('/')[-1] + '/'
                                # print('src_dir1', src_dir)
                                # print('dst_dir1', dst_dir)
                                self.copy_demo(src_dir, dst_dir)
                                dic_all = self.get_config_dirs(dst_dir)
                                # print(dic_all)
                                # item = self.find_item(item.text(1))
                                self.tree_item1(self.root, (src_dir.split('/')[-1]),
                                                src_dir.split('/')[-1])
                                item = self.find_item(src_dir.split('/')[-1])
                                for i in range(len(dic_all['files'])):
                                    self.tree_item1(item, dic_all['files'][i],
                                                    src_dir.split('/')[-1] + '/' + dic_all['files'][i])
                                self.loc_search = dst_dir
                                self.get_key_copy(dic_all['child_dirs'], item)
                            elif flag == 1:
                                QMessageBox.critical(self, "error", "文件复制失败")
                        elif '.' in item.text(1):
                            QMessageBox.critical(self, "error", "文件下不能存放文件")
                        else:
                            for i in range(item.childCount()):
                                if item.child(i).text(0) == a1.split('/')[-1]:
                                    new_project_win = NewProject(self, flag=3, tree=item)
                                    new_project_win.exec_()
                                    flag = 1
                                    if new_project_win.get_create_success_flag() is True:
                                        name = new_project_win.lineEdit.text()
                                        flag = 2
                                        break
                                    else:
                                        break
                            if flag == 2:
                                src_dir = a1
                                dst_dir = JuConfig.RECENT_PROJECT_PATH + '/' + item.text(1) + '/' + name + '//'
                                self.copy_demo(src_dir, dst_dir)
                                dic_all = self.get_config_dirs(dst_dir)
                                item = self.find_item(item.text(1))
                                self.tree_item1(item, name, item.text(1) + '/' + name)
                                # print(item.text(1) + '/' + folder_name)
                                item = self.find_item(item.text(1) + '/' + name)
                                for i in range(len(dic_all['files'])):
                                    self.tree_item1(item, dic_all['files'][i],
                                                    item.text(1) + '/' + dic_all['files'][i])
                                    # print(item.text(1) + '/' + folder_name + '/' + dic_all['files'][i])
                                self.loc_search = dst_dir
                                self.get_key_copy(dic_all['child_dirs'], item)
                            elif flag == 0:
                                src_dir = a1
                                dst_dir = JuConfig.RECENT_PROJECT_PATH + '/' + item.text(1) + '/' + folder_name + '/'
                                self.copy_demo(src_dir, dst_dir)
                                dic_all = self.get_config_dirs(dst_dir)
                                item = self.find_item(item.text(1))
                                self.tree_item1(item, (src_dir.split('/')[-1]),
                                                item.text(1) + '/' + folder_name)
                                # print(item.text(1) + '/' + folder_name)
                                item = self.find_item(item.text(1) + '/' + folder_name)
                                for i in range(len(dic_all['files'])):
                                    self.tree_item1(item, dic_all['files'][i],
                                                    item.text(1) + '/' + dic_all['files'][i])
                                    # print(item.text(1) + '/' + folder_name + '/' + dic_all['files'][i])
                                self.loc_search = dst_dir
                                self.get_key_copy(dic_all['child_dirs'], item)
                            elif flag == 1:
                                QMessageBox.critical(self, "error", "文件复制失败")
            else:
                QMessageBox.critical(self, "error", "复制失败，请重新复制")
            # except BaseException as e:
            #     QMessageBox.critical(self._ui_base, "error", "复制失败，请重新复制")

    def get_key_copy(self, lis, root):
        for i in range(len(lis)):
            # self.ui_log_show(lis[i])
            if lis[i]['child_dirs'] == []:
                value = str(lis[i]['dirname'].split('recent_project/')[1])
                if '//' in value:
                    value_list = lis[i]['dirname'].split('//')
                    self.tree_item1(root, value_list[-1], value_list[-1])
                    item = self.find_item(value_list[-1])
                    for j in range(len(lis[i]['files'])):
                        # self.ui_log_show('value_1' + value + '/' + lis[i]['files'][j])
                        self.tree_item1(item, lis[i]['files'][j], value + '/' + lis[i]['files'][j])
                else:
                    self.tree_item1(root, value, value)
                    item = self.find_item(value)
                    for j in range(len(lis[i]['files'])):
                        # self.ui_log_show('value_1' + value + '/' + lis[i]['files'][j])
                        self.tree_item1(item, lis[i]['files'][j], value + '/' + lis[i]['files'][j])
            else:
                # self.ui_log_show(lis[i]['dirname'].split('recent_project\\')[1])
                value = str(lis[i]['dirname'].split('recent_project/')[1])
                if '//' in value:
                    value_list = lis[i]['dirname'].split('//')
                    item = self.find_item(value_list[-2])
                    self.tree_item1(item, value_list[-1], value_list[-1])
                    for j in range(len(lis[i]['files'])):
                        item = self.find_item(value_list[-1])
                        self.tree_item1(item, lis[i]['files'][j], value + '/' + lis[i]['files'][j])
                    self.get_key_copy(lis[i]['child_dirs'], item)
                else:
                    self.tree_item1(root, value, value)
                    item = self.find_item(value)
                    for j in range(len(lis[i]['files'])):
                        # self.ui_log_show('value ' + value + '/' + lis[i]['files'][j])
                        self.tree_item1(item, lis[i]['files'][j], value + '/' + lis[i]['files'][j])
                    self.get_key_copy(lis[i]['child_dirs'], item)

    def copy_demo(self, src_dir, dst_dir):
        """
        复制src_dir目录下的所有内容到dst_dir目录
        :param src_dir: 源文件目录
        :param dst_dir: 目标目录
        :return:
        """
        if not path.exists(dst_dir):
            makedirs(dst_dir)
        if path.exists(src_dir):
            for file in listdir(src_dir):
                file_path = path.join(src_dir, file)
                dst_path = path.join(dst_dir, file)
                if path.isfile(path.join(src_dir, file)):
                    copyfile(file_path, dst_path)
                else:
                    self.copy_demo(file_path, dst_path)

    def Project_new(self):
        new_project_win = NewProject(self)
        new_project_win.exec_()
        if new_project_win.get_create_success_flag() is True:
            try:
                rmtree(JuConfig.RECENT_PROJECT_PATH)
            except Exception:
                pass
            name = new_project_win.lineEdit.text()
            try:
                makedirs(JuConfig.RECENT_PROJECT_PATH + '/' + name)
            except BaseException as e:
                QMessageBox.critical(self, "error", "{},\n{}".format('请重新创建一次', e))
            with open(JuConfig.RECENT_PROJECT_PATH + "/" + name + '/' + name + ".py", "w") as f:  # 打开文件
                f.write("#!/usr/bin/env python\n")
                f.write("# -*- coding: utf-8 -*-\n")
                f.write("\n\n\n\n")
            with open(JuConfig.RECENT_PROJECT_PATH + "/" + "recent_project.jmszs", "w") as f:  # 打开文件
                f.write("1")
            self._ui_base.tree.clear()
            self.close_all_tab()
            self.save_file_flag = True
            self.root = QTreeWidgetItem(self._ui_base.tree)
            self.root.setText(0, name)
            self.root.setText(1, 'Project_Project')
            self.tree_item1(self.root, name, name)
            item = self.find_item(name)
            self.tree_item1(item, name + '.py', name + '/' + name + '.py')
            self.new_project = True
            self.flag_recent = True

    def open_project_url(self, fileName1, flag=False):
        try:
            rmtree(JuConfig.RECENT_PROJECT_PATH)
        except BaseException as e:
            pass
        self.file_name = fileName1
        value_all = fileName1.split('/')
        try:
            zipFile = ZipFile(fileName1)
            for file in zipFile.namelist():
                zipFile.extract(file, JuConfig.RECENT_PROJECT_PATH)
            zipFile.close()
            self._ui_base.tree.clear()
            # self.project_label_loc.setText('项目路径:  ' + fileName1)
        except BaseException as e:
            QMessageBox.critical(self, "error", "请打开正确工程\n{}".format(e))
            if flag:
                self.recent_project_open(flag=True)
            return
        check_status = self._check()
        if check_status:
            self.close_all_tab()
            self.root = QTreeWidgetItem(self._ui_base.tree)
            self.root.setText(0, value_all[-1].replace(".jmszs", ""))
            self.root.setText(1, 'Project_Project')
            a = self.get_config_dirs(JuConfig.RECENT_PROJECT_PATH)
            self.get_key(a.get('child_dirs'), self.root)
            b = a.get('files')
            # print("b", b)
            for i in range(len(b)):
                if b[i] == 'recent_project.jmszs':
                    pass
                else:
                    self.tree_item1(self.root, b[i], b[i])
            self.recent_project_open()
            self.new_project = True
        else:
            QMessageBox.critical(self, "error", "工程文件损坏！！")
            for i in range(len(self.list_projetc_name)):
                if self.list_project_loc[i] == self.file_name:
                    self.open_recent.removeAction(self.list_projetc_name[i])
            if flag:
                self.recent_project_open(flag=True)

    def recent_get_project(self):
        # try:
        self.list_project_loc = []
        self.list_projetc_name = []
        base_ = JuConfig.RECENT_PROJECT_PATH + '/recent.jmszs'
        # print(base_)
        if path.exists(base_):
            content = {}
            with open(base_, encoding='utf-8') as file:
                content = str(file.read().rstrip())
                content = content.replace("'", '"')
                # print(content)
                content = loads(content)
            for k in content:
                self.list_project_loc.append(content[k])
                self.list_projetc_name.append(content[k].split('/')[-1])
        for i in range(len(self.list_projetc_name)):
            self._ui_base.open_recent.addAction(self.list_projetc_name[i])

    def list_dir(self, path1, res):
        for i in listdir(path1):
            temp_dir = path.join(path1, i)
            # print(temp_dir)
            if '__pycache__' in temp_dir:
                pass
            else:
                if path.isdir(temp_dir):
                    temp = {"dirname": temp_dir, 'child_dirs': [], 'files': []}
                    res['child_dirs'].append(self.list_dir(temp_dir, temp))
                else:
                    res['files'].append(i)
        return res

    def get_config_dirs(self, url):
        res = {'dirname': 'root', 'child_dirs': [], 'files': []}  # 当前路径认为是root根目录，向其子文件夹与子文件填充
        return self.list_dir(url, res)  # 输入路径

    def close_all_tab(self):
        number = self._ui_base.tab_widget_new.count()
        for i in range(number):
            self.close_tab(i)
        if self._ui_base.Dockable_4.isVisible() is True:
            self._ui_base.Dockable_4.setVisible(False)

    def _check(self):
        # self.ui_log_show('recent_project.jmszs')
        try:
            with open(JuConfig.RECENT_PROJECT_PATH + '/recent_project.jmszs', 'r', encoding='utf-8') as f:
                data = f.readline()
                if data == '1':
                    return True
        except BaseException as e:
            self._user_logger.info(e)

    def close_tab(self, index):
        # self.ui_log_show(self.tab_widget_new.tabText(index))
        value = self._ui_base.tab_widget_new.tabText(index)
        file_suffix = ['py', 'txt', 'cpp', 'h']
        if value.split('.')[-1] in file_suffix:
            # self.ui_log_show(self.text_all)
            self.text_all[value].save()
            self.text_all.pop(value)
        if value.split('.')[-1] == "juncfg":
            self.text_all[value].save()
            self.text_all.pop(value)
        self._ui_base.tab_widget_new.removeTab(index)
        if self._ui_base.tab_widget_new.count() == 0:
            self._ui_base.tab_widget_new.setVisible(False)
            self._ui_base.text_.setVisible(True)
            if self._ui_base.Dockable_4.isVisible() is True:
                self._ui_base.Dockable_4.setVisible(False)
        temp_list = []
        for i in range(self._ui_base.tab_widget_new.count()):
            temp_list.append(self._ui_base.tab_widget_new.tabText(i).split('.')[-1])
        if 'juncfg' not in temp_list:
            if self._ui_base.Dockable_4.isVisible() is True:
                self._ui_base.Dockable_4.setVisible(False)

    # def tab_new_(self):
    #     self.tab_widget_new = QTabWidget()
    #     self._ui_base.gridLayout_center.addWidget(self.tab_widget_new)
    #     self.tab_widget_new.setTabsClosable(True)
    #     self.tab_widget_new.setVisible(False)

    # tree的双击事件
    def treeonClicked(self):
        item = self._ui_base.tree.currentItem()
        self._user_logger.info('Key=%s,value=%s' % (item.text(0), item.text(1)))
        imgNmaeList = ['jpg', 'png', 'bmp']
        file_url = self.file_url()
        if '.py' in item.text(0) or '.txt' in item.text(0) or '.juncfg' in item.text(0):
            self.add_tab_(item.text(0), file_url)
        else:
            for i in imgNmaeList:  # 遍历后缀列表
                if i in item.text(0):  # 如果确认为图像后缀
                    self.add_tab_img(item.text(0), file_url)
            # self.read_t(item.text(0), item.text(1))

    def file_url(self, index=None):
        item = self._ui_base.tree.currentItem()  # 获取选中节点
        ret = self.getLocation(item)  # 获取选中节点父节点
        if ret:
            bin_path = path.join(ret, item.text(0)).replace('\\', '/')
            bin_path = bin_path.split('/')
            del bin_path[0]
            loc = ''
            for i in range(len(bin_path)):
                loc = loc + str(bin_path[i]) + '/'
            loc = loc[0:-1]
        else:
            loc = ''
        return loc

    def getLocation(self, item):
        if item.parent():
            temp = item.parent().text(0)
            parent = self.getLocation(item.parent())  # 递归获取上层节点，直到顶层
            if parent:
                res = path.join(parent, temp)
                return res
            else:
                return temp
        else:
            return 0

    # tab页面显示文件内容
    def add_tab_(self, name, value):
        tab_all = self._ui_base.tab_widget_new.count()
        if tab_all == 0:
            self._ui_base.text_.setVisible(False)
            self._ui_base.tab_widget_new.setVisible(True)
        for i in range(tab_all):
            if self._ui_base.tab_widget_new.tabText(i) == value:
                self._ui_base.tab_widget_new.setCurrentIndex(i)
                return
        file_name, _ = name.split(".")
        tab = QWidget()
        if _ == "py":
            self.text_ = PMGPythonEditor(user_log=self._user_logger)
            python_path = JuConfig.CURRENT_FILE_PATH + "/python"
            self.text_.edit.autocomp_thread.set_envs(python_path)
            filc_loc = "{}/{}".format(JuConfig.RECENT_PROJECT_PATH, value)
            self.text_.load_file(filc_loc)
            self.text_._init_actions()
            self.text_._init_signals()
            self.text_all[value] = self.text_
        elif _ == "juncfg":
            try:
                filc_loc = "{}/{}".format(JuConfig.RECENT_PROJECT_PATH, value)
                self.text_ = self.CalculatorWindow.file_load(filc_loc)
                #         mdiArea.s_del.connect(self.onEditDelete)
                #         mdiArea.s_copy.connect(self.onEditCopy)
                #         mdiArea.s_paste.connect(self.onEditPaste)
                #         mdiArea.s_cut.connect(self.onEditCut)
                self.text_.s_save.connect(self.node_save)
                self.text_.s_del.connect(self.node_del)
                self.text_.s_copy.connect(self.node_copy)
                self.text_.s_paste.connect(self.node_paste)
                self.text_.s_cut.connect(self.node_cut)
                # text_ = self.CalculatorWindow.getCurrentNodeEditorWidget()

                self.text_.fileLoad(filc_loc)
                # text_._init_actions()
                # text_._init_signals()
                self.text_all[value] = self.text_
                if self._ui_base.Dockable_4.isVisible() is False:
                    self._ui_base.Dockable_4.setVisible(True)
            except BaseException as e:
                self._user_logger.error(e)
        gridLayout_112 = QVBoxLayout(tab)
        gridLayout_112.setSpacing(0)
        gridLayout_112.setObjectName(u"gridLayout")
        gridLayout_112.setContentsMargins(0, 0, 0, 0)
        gridLayout_112.addWidget(self.text_)
        self._ui_base.tab_widget_new.addTab(tab, value)
        self._ui_base.tab_widget_new.setCurrentIndex(tab_all)
        self._ui_base.tab_widget_new.setTabToolTip(tab_all, str(value))

    def node_save(self):
        # self.Project_save()
        index = self._ui_base.tab_widget_new.currentIndex()
        value = self._ui_base.tab_widget_new.tabText(index)
        text_ = self.text_all[value]
        file_path = JuConfig.RECENT_PROJECT_PATH + "/" + value
        text_.fileSave(file_path)

    def node_del(self):
        index = self._ui_base.tab_widget_new.currentIndex()
        value = self._ui_base.tab_widget_new.tabText(index)
        text_ = self.text_all[value]
        # file_path = JuConfig.RECENT_PROJECT_PATH + "/" + value
        text_.scene.getView().deleteSelected()

    def node_copy(self):
        index = self._ui_base.tab_widget_new.currentIndex()
        value = self._ui_base.tab_widget_new.tabText(index)
        text_ = self.text_all[value]
        data = text_.scene.clipboard.serializeSelected(delete=False)
        str_data = dumps(data, indent=4)
        QApplication.clipboard().setText(str_data)

    def node_paste(self):
        index = self._ui_base.tab_widget_new.currentIndex()
        value = self._ui_base.tab_widget_new.tabText(index)
        text_ = self.text_all[value]
        if text_:
            raw_data = QApplication.clipboard().text()
            try:
                data = loads(raw_data)
            except ValueError as e:
                print("Pasting of not valid json data!", e)
                return

            # check if the json data are correct
            if 'nodes' not in data:
                print("JSON does not contain any nodes!")
                return
            return text_.scene.clipboard.deserializeFromClipboard(data)

    def node_cut(self):
        index = self._ui_base.tab_widget_new.currentIndex()
        value = self._ui_base.tab_widget_new.tabText(index)
        text_ = self.text_all[value]
        if text_:
            data = text_.scene.clipboard.serializeSelected(delete=True)
            str_data = dumps(data, indent=4)
            QApplication.instance().clipboard().setText(str_data)

    def Project_Save_As(self, file=None):
        if file is not None:
            file_loc = file
            batch_zip = Thread(target=self.batch_zip, args=(JuConfig.RECENT_PROJECT_PATH, file_loc,))
            # Project_save.setDaemon(True)
            batch_zip.start()
            self._ui_base.project_label_loc.setText(file)

    def Project_save(self):
        if self.new_project:
            if self.file_name is not None:
                file_loc = deepcopy(self.file_name)
                file_loc = file_loc.split('.')[0]
                batch_zip = Thread(target=self.batch_zip, args=(JuConfig.RECENT_PROJECT_PATH, self.file_name,))
                # Project_save.setDaemon(True)
                batch_zip.start()
                self._ui_base.project_label_loc.setText(file_loc)
                # self.batch_zip(base_loc, self.file_name)
            #     self.s_singal_save.emit(1)
            # else:
            #     self.s_singal_save.emit(2)
            else:
                self._user_logger.info(2)
                get_filename_path, ok2 = QFileDialog.getSaveFileName(self,
                                                                     "文件保存",
                                                                     "E:/",
                                                                     "Jmszs Files (*.jmszs)")
                # get_filename_path = QFileDialog.getExistingDirectory(self, "选取文件夹", "E:/")
                if get_filename_path != '':
                    # self.ui_log_show(get_filename_path)
                    self._ui_base.project_label_loc.setText(get_filename_path)
                    self.new_project = True
                    self.save_file_flag = True
                    self.file_name = get_filename_path
                    file_loc = deepcopy(self.file_name)
                    file_loc = file_loc.split('.')[0]
                    # self.ui_log_show(file_loc)
                    # self.ui_log_show(self.file_name)
                    # print(self.file_name)
                    # print(base_loc)
                    batch_zip = Thread(target=self.batch_zip, args=(JuConfig.RECENT_PROJECT_PATH, self.file_name,))
                    # Project_save.setDaemon(True)
                    batch_zip.start()
                    # self.batch_zip(base_loc, self.file_name)
                    # with py7zr.SevenZipFile(self.file_name, 'w') as archive:
                    #     archive.writeall(base_loc, '')
                    # self.s_singal_save.emit(3)
                    # self.project_label_loc.setText('项目路径:  ' + self.file_name)
                    if self.flag_recent:
                        # print(22)
                        self.recent_project_open()
                        self.flag_recent = False

        # notification('Info', '项目工程保存成功！！！！！')

    def batch_zip(self, start_dir, zip_file):
        # start_dir要压缩的文件路径
        # zip_file 输出zip文件的路径
        zip_file = zip_file
        z = ZipFile(zip_file, 'w', ZIP_DEFLATED)
        # print(z)
        for path1, dirname, file_name in walk(start_dir):
            fpath = path1.replace(start_dir, '')
            fpath = fpath and fpath + sep  # 在原fpath加上\
            for filename in file_name:  # 逐个循环读取文档名称
                z.write(path.join(path1, filename), fpath + filename)  # 实现在输出路径的Zip压缩操作
        z.close()
        self._save_flag = True
        return zip_file

    def recent_project_open(self, flag=False):
        if flag is False:
            base_ = JuConfig.RECENT_PROJECT_PATH + '/recent.jmszs'
            # print(base_)
            if path.exists(base_):
                # print(2)
                content = {}
                try:
                    with open(base_, encoding='utf-8') as file:
                        content = file.read().rstrip()
                        content = loads(content)
                except BaseException as e:
                    self._user_logger.info(e)
                content = {}
                if self.file_name is not None:
                    num = -1
                    for k in content:
                        if content[k] == self.file_name:
                            num = 0
                    if num == -1:
                        # print(223, self.file_name)
                        _name = str(time.time()).split('.')[0]
                        # file_name = self.file_name
                        # print(type(file_name))
                        # print(content)
                        # print(_name)
                        content[_name] = str(self.file_name)
                        # print(str(content))
                        # print(type(str(content)))
                        with open(base_, "w") as f:  # 打开文件
                            f.write(str(content))
        else:
            base_ = JuConfig.RECENT_PROJECT_PATH + '/recent.jmszs'
            with open(base_, encoding='utf-8') as file:
                content = file.read().rstrip()
                content = loads(content)
                if self.file_name is not None:
                    for k in content:
                        if content[k] == self.file_name:
                            content.pop(k)
                            break

    def get_key(self, lis, root):
        # self.ui_log_show(dic.get('child_dirs'))
        # self.ui_log_show(lis)
        # self.ui_log_show(len(lis))
        for i in range(len(lis)):
            # self.ui_log_show(lis[i])
            if lis[i]['child_dirs'] == []:
                value = str(lis[i]['dirname'].split('recent_project\\')[1])
                # print("va", value)
                if '\\' in value:
                    value_list = lis[i]['dirname'].split('\\')
                    self.tree_item1(root, value_list[-1], value_list[-1])
                    item = self.find_item(value_list[-1])
                    for j in range(len(lis[i]['files'])):
                        # self.ui_log_show('value_1' + value + '/' + lis[i]['files'][j])
                        self.tree_item1(item, lis[i]['files'][j], value + '/' + lis[i]['files'][j])
                else:
                    self.tree_item1(root, value, value)
                    item = self.find_item(value)
                    for j in range(len(lis[i]['files'])):
                        # self.ui_log_show('value_1' + value + '/' + lis[i]['files'][j])
                        self.tree_item1(item, lis[i]['files'][j], value + '/' + lis[i]['files'][j])
            else:
                # self.ui_log_show(lis[i]['dirname'].split('recent_project\\')[1])
                value = str(lis[i]['dirname'].split('recent_project\\')[1])
                # print('value', value)
                if '\\' in value:
                    # if '__pycache__' in value:
                    #     pass
                    # else:
                    value_list = lis[i]['dirname'].split('\\')
                    item = self.find_item(value_list[-2])
                    self.tree_item1(item, value_list[-1], value_list[-1])
                    for j in range(len(lis[i]['files'])):
                        item = self.find_item(value_list[-1])
                        self.tree_item1(item, lis[i]['files'][j], value + '/' + lis[i]['files'][j])
                    self.get_key(lis[i]['child_dirs'], item)
                else:
                    self.tree_item1(root, value, value)
                    item = self.find_item(value)
                    for j in range(len(lis[i]['files'])):
                        # self.ui_log_show('value ' + value + '/' + lis[i]['files'][j])
                        self.tree_item1(item, lis[i]['files'][j], value + '/' + lis[i]['files'][j])
                    self.get_key(lis[i]['child_dirs'], item)

    def close_(self, flag=1):
        if flag == 1:
            if self._right_bottom_info.isVisible():
                self._right_bottom_info.win_close()
            self.ui_break = True
            self.close()
            self._test_logger.info("login out")
            self.deal_send.put("break")
        elif flag == 2:
            self.Project_save()
            if self._right_bottom_info.isVisible():
                self._right_bottom_info.win_close()
            self.ui_break = True
            self.close()
            self._test_logger.info("login out")
            self.deal_send.put("break")
            print(2)

    # def resizeEvent(self, e):
    #     # don't forget to call the resizeEvent() of super class
    #     super(self.parent).resizeEvent(e)
    #     print("1==================")
    #     self.parent.title_ui.label.resize(self.parent.width() - 138, 28)
    #     if self.parent.widget:
    #         self.parent.widget.resize(self.parent.width(), self.parent.height() - 28)
    #         self.parent.widget.move(0, 28)
    #         x = self.parent.widget.width() - self.parent._ju_ui._plugin_version.width() - 5
    #         y = self.parent.widget.height() - self.parent._ju_ui._plugin_version.height() - 30
    #         self.parent._ju_ui._plugin_version.move(x, y)
