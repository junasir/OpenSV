#!/usr/bin/env python3
# -*- coding: utf-8 -*-

r"""
"""

__author__ = "Jiang Jun"

from os import path, makedirs
from shutil import copyfile
from PySide2.QtWidgets import QGridLayout, QLabel, QLineEdit, QPushButton, QFileDialog, \
    QMessageBox, QDialog
from ju_cfg import JuConfig


class JuUploadPlugin(QDialog):
    def __init__(self, parent=None, log=None):
        super().__init__(parent)
        self.setWindowTitle("本地插件导入")
        self.user_log = log
        self._init_ui()
        self._bind_event()

    def _init_ui(self):
        label_input_variable = QLabel(self, text="IP类别:")
        self.label_input_variable = QLineEdit(self)

        self.btn_ip_path = QPushButton(self, text="Ip文件:")
        self.ip_path = QLineEdit(self)
        self.ip_path.setReadOnly(True)

        self.btn_device_path = QPushButton(self, text="Device文件:")
        self.device_path = QLineEdit(self)
        self.device_path.setReadOnly(True)
        self.update_btn = QPushButton(self, text="update")
        self._grid = QGridLayout(self)
        self._grid.addWidget(label_input_variable, 0, 0)
        self._grid.addWidget(self.label_input_variable, 0, 1)
        self._grid.addWidget(self.btn_ip_path, 1, 0)
        self._grid.addWidget(self.ip_path, 1, 1)
        self._grid.addWidget(self.btn_device_path, 2, 0)
        self._grid.addWidget(self.device_path, 2, 1)
        self._grid.addWidget(self.update_btn, 3, 0, 1, 2)

    def _bind_event(self):
        self.btn_ip_path.clicked.connect(self.ip_select)
        self.btn_device_path.clicked.connect(self.device_select)
        self.update_btn.clicked.connect(self._commit)

    def ip_select(self):
        fileName1, filetype = QFileDialog.getOpenFileName(self,
                                                          "导入Ip文件",
                                                          "C:/",
                                                          "py (*.py)")
        if fileName1 == '':
            pass
        else:
            self.ip_path.setText(str(fileName1))

    def device_select(self):
        fileName1, filetype = QFileDialog.getOpenFileName(self,
                                                          "导入Device文件",
                                                          "C:/",
                                                          "py (*.py)")
        if fileName1 == '':
            pass
        else:
            self.device_path.setText(str(fileName1))

    def _commit(self):
        ip_path = self.ip_path.text()
        device_path = self.device_path.text()
        class_name = self.label_input_variable.text()
        if ip_path != "" and device_path != "" and class_name != "":
            ip_name = ip_path.split("/")[-1]
            device_name = device_path.split("/")[-1]
            current_ip_path = f"{JuConfig.CURRENT_FILE_PATH}/JuPluginPack/JuIp/{class_name}/" \
                              f"{ip_name.title().split('.')[0]}_Pack"
            current_device_path = f"{JuConfig.CURRENT_FILE_PATH}/JuPluginPack/JuDevice/{class_name}/" \
                                  f"{device_name.title().split('.')[0]}_Pack"
            if path.exists(current_ip_path) is False:
                makedirs(current_ip_path)
            if path.exists(current_device_path) is False:
                makedirs(current_device_path)
            try:
                copyfile(ip_path, f"{current_ip_path}/{ip_name}")
                copyfile(device_path, f"{current_device_path}/{device_name}")
                self.user_log.info("导入成功，请重新加载驱动")
                self.ip_path.clear()
                self.device_path.clear()
                self.label_input_variable.clear()
                QMessageBox.information(self, "Info", '插件导入成功.', QMessageBox.Ok)
            except BaseException as e:
                QMessageBox.warning(self, "Error", str(e), QMessageBox.Ok)
        else:
            QMessageBox.warning(self, "Error", '请填写信息.', QMessageBox.Ok)
#
#
# if __name__ == "__main__":
#     app = QApplication(argv)
#     window = JuUploadPlugin()
#     window.show()
#     sys.exit(app.exec_())
