from json import loads, dumps
from sys import argv
from os import path, makedirs, walk, rename, remove
from threading import Thread
from time import time
from zipfile import ZipFile

from PySide2.QtCore import Qt, Signal
from PySide2.QtWidgets import QWidget, QGridLayout, QListWidget, QPlainTextEdit, QComboBox, QLabel, \
    QSpacerItem, QSizePolicy, QPushButton, QProgressBar, QMessageBox, QDialog
from qdarkstyle import load_stylesheet_pyside2
from requests import post
from webdav3.client import Client

from JuFileOperate.ju_aes_encrypt import JuAESEncrypt
from ju_cfg import JuConfig


class JuDeviceUi(QDialog):
    process_signal = Signal(int)

    def __init__(self, parent=None):
        super().__init__()
        self.install_flag = False
        self._value = 0
        self.temp = 0
        self.setStyleSheet(load_stylesheet_pyside2())
        self.ip_dic = {}
        self.parent = parent
        self.setWindowTitle("可用IP插件")
        self.resize(450, 400)
        self.right_widget = QWidget(self)
        self.right_widget.setMinimumWidth(200)
        grid_layout = QGridLayout(self)
        self.listWidget = QListWidget(self)
        grid_layout.addWidget(self.listWidget, 0, 0, 1, 1)
        grid_layout.addWidget(self.right_widget, 0, 1, 1, 1)
        self._down_win = JuProcessBar(self)
        self._get_sql_info()
        self._init_ui()
        self._bind_event()
        self.process_signal.connect(self.process_win)

        pass

    def _init_ui(self):
        right_widget_grid = QGridLayout(self.right_widget)
        self.plainTextEdit = QPlainTextEdit(self)
        self.combobox = QComboBox(self)
        label = QLabel(self)
        label.setText("版本")
        self.btn = QPushButton(self)
        self.btn.setText("Install")
        ver = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        right_widget_grid.addWidget(self.plainTextEdit, 0, 0, 1, 2)
        right_widget_grid.addWidget(self.combobox, 2, 1, 1, 1)
        right_widget_grid.addWidget(label, 2, 0, 1, 1)
        right_widget_grid.addItem(ver, 1, 0, 1, 2)
        right_widget_grid.addWidget(self.btn, 3, 0, 1, 2)

    def _bind_event(self):
        self.listWidget.itemClicked.connect(self.list_click)
        self.btn.clicked.connect(self.btn_click)

    def _get_sql_info(self):
        dic_text = {"operation": "get_ip_info", "value": ["get_ip_info"]}
        data = JuAESEncrypt().encrypt(dumps(dic_text, ensure_ascii=False, separators=(',', ':')))
        response = post(url=JuConfig.URL, data=data)
        de_data = JuAESEncrypt().decrypt(response.text)
        if loads(de_data)["flag"]:
            value = loads(de_data)["value"]
            for i in range(len(value)):
                if value[i][1] in self.ip_dic:
                    self.ip_dic[value[i][1]][4].append(value[i][4])
                else:
                    value[i][4] = [value[i][4]]
                    self.ip_dic[value[i][1]] = value[i]
                    self.listWidget.addItem(value[i][1])
        else:

            pass

    def list_click(self, item):
        select_name = item.text()
        print(select_name)
        self.select_name = select_name
        if select_name in self.ip_dic:
            all_info = self.ip_dic[select_name]
            self.combobox.clear()
            self.combobox.addItems(all_info[4])
            info = "ip_name: {} \ninfo: {}".format(select_name, all_info[-1])
            self.plainTextEdit.setPlainText(info)
            print(all_info)

    def install_file(self):
        all_info = self.ip_dic[self.select_name]
        self.install_flag = True
        save_ip_path = JuConfig.CURRENT_FILE_PATH + "/JuPluginPack/JuIp/" + all_info[5] + "/" + all_info[2] + "_Pack/"
        save_device_path = JuConfig.CURRENT_FILE_PATH + "/JuPluginPack/JuDevice/" + all_info[5] + "/" + all_info[3] + "_Pack/"
        if path.exists(save_ip_path) is False:
            makedirs(save_ip_path)
        else:
            for root_path, dirs, files in walk(save_ip_path):
                for file in files:
                    if "_backup_" not in file:
                        new_file = save_ip_path + "/" + file.split(".")[0] + "_backup_" + str(time()) + "." \
                                   + file.split(".")[-1]
                        rename(save_ip_path + "/" + file, new_file)
        if path.exists(save_device_path) is False:
            makedirs(save_device_path)
        else:
            for root_path, dirs, files in walk(save_device_path):
                for file in files:
                    if "_backup_" not in file:
                        new_file = save_device_path + "/" + file.split(".")[0] + "_backup_" + str(time()) + "." \
                                   + file.split(".")[-1]
                        rename(save_device_path + "/" + file, new_file)
        self.process_signal.emit(1)
        self._new_process = 1
        save_path = save_ip_path + all_info[8].split("/")[-1]
        self._down_win.set_label_text("Install {}".format(all_info[8].split("/")[-1]))
        self._get_post_file(all_info[8], save_path)
        self._extractall_file(save_path, save_ip_path)
        self._del_file(save_path)
        self._new_process = 2
        self._down_win.set_label_text("Install {}".format(all_info[9].split("/")[-1]))
        save_path = save_device_path + all_info[9].split("/")[-1]
        self._get_post_file(all_info[9], save_path)
        self._extractall_file(save_path, save_device_path)
        self._del_file(save_path)
        self.process_signal.emit(2)

    def process_win(self, num):
        if num == 1:
            self._down_win.show()
        elif num == 2:
            self._down_win.hide()
            self._down_win.set_value(0)
            QMessageBox.information(self, "Info", "Install ok", QMessageBox.Ok)

    def btn_click(self):
        install = Thread(target=self.install_file, args=())
        install.start()

    def _get_post_file(self, download_path, save_path):
        # 需要修改这边
        try:
            options = {
                'webdav_hostname': "",
                'webdav_login': "",
                'webdav_password': "",
                'disable_check': True,  # 有的网盘不支持check功能
            }
            client = Client(options)
            client.download(download_path, save_path, progress=self.progress_update)
            return True, save_path
        except BaseException as e:
            return False, e

    def progress_update(self, current, total, *args):
        print(current, total)
        if total != 0 and current != 0:
            self._value = (int(current) / int(total)) / 2 * self._new_process * 100 + self.temp
            if self._value >= 99:
                self._down_win.set_value(99)
            # self.temp = 0
        if current == 0:
            self.temp = self._value

    def _extractall_file(self, zip_file, file_unzip_path):
        if not path.exists(file_unzip_path):
            makedirs(file_unzip_path)
        with ZipFile(zip_file, "r") as z:
            z.extractall(file_unzip_path)

    def _del_file(self, file_path):
        try:
            if path.exists(file_path):
                remove(file_path)
        except Exception:
            pass


class JuProcessBar(QWidget):

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        # self.setStyleSheet(load_stylesheet_pyside2())
        self._stylesheet = '''
        #BlueProgressBar {
            border: 2px solid #8bd9d3;
            background-color: #505050;
            border-radius:10px;
            text-align: center;
            font-size: 30px;
        }
        #BlueProgressBar::chunk {
            background-color: #8bd9d3;
            width: 10px;
            margin: 0.5px;
        }
        '''
        self._bar = None
        # self.setStyleSheet("background:#505050;")
        self.setStyleSheet("background:#3C3F41;")
        self.setWindowTitle("Info")
        self.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.ApplicationModal)
        self._grid = QGridLayout()
        self._setup_ui()
        self.adjustSize()
        self.setLayout(self._grid)

    def _setup_ui(self):
        self._label = QLabel(self)
        self._label.setMinimumSize(300, 30)
        self._grid.addWidget(self._label, 1, 0)
        self._bar = QProgressBar(self, objectName="BlueProgressBar")
        self._bar.setStyleSheet(self._stylesheet)
        self._bar.setMinimum(0)
        self._bar.setMaximum(100)
        self._bar.setValue(0)
        self._bar.setMinimumWidth(300)
        self._grid.addWidget(self._bar, 2, 0)

    def set_value(self, value):
        self._bar.setValue(value)

    def get_value(self):
        return self._bar.value()

    def set_label_text(self, text):
        self._label.setText(text)

    def set_min_value(self, value):
        self._bar.setMinimum(value)

    def set_max_value(self, value):
        self._bar.setMaximum(value)

#
# if __name__ == "__main__":
#     app = QApplication(argv)
#     window = JuDeviceUi()
#     window.show()
#     exit(app.exec_())
