import os
import subprocess

from PySide2.QtCore import Signal, QThread
from PySide2.QtWidgets import QDialog, QGridLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QComboBox


class pip_install_thread(QThread):
    emit_signal_log = Signal()

    def __init__(self, NewProject, name):
        super(pip_install_thread, self).__init__()
        self.NewProject = NewProject
        self.name = name

    def run(self):
        # location = r"E:\project\manage_platform_v2.1\code_editer\1.py"
        self.NewProject.log_Signal.emit("开始安装{}".format(self.name))
        # envs = os.getcwd().replace('\\', '/') + '/envs/python E:/project/manage_platform_v2.1/new_code1/nn/nn.py'
        envs = os.getcwd().replace('\\', '/') + '/envs/python -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple'
        cmd = "{} {}".format(envs, self.name)
        code = "utf8"
        process = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT)
        while process.poll() is None:
            line = process.stdout.readline()
            line = line.strip()
            if line:
                print(line.decode(code, 'ignore'))
                self.NewProject.log_Signal.emit(line.decode(code, 'ignore'))
                if 'Successfully' in line.decode(code, 'ignore'):
                    self.emit_signal_log.emit()
                    # QMessageBox.information(self, 'Successfully', 'Package 安装成功')
                    # QMessageBox.critical(self, "Info", "Package 安装成功")
                # print(line.decode(code, 'ignore'))
        self.NewProject.log_Signal.emit("安装结束{}".format(self.name))
        self.NewProject.install_flag = False
        self.NewProject._btn_ok.setText('Install')


class NewProject(QDialog):

    def __init__(self, parent=None, flag=0, log_Signal=None, tree=None):
        super(NewProject, self).__init__(parent=parent)
        self._grid = QGridLayout(self)
        self.tree = tree
        self.resize(300, 100)
        self.flag = flag
        self.install_flag = False
        self.new_name = None
        self.log_Signal = log_Signal
        self.lineEdit = QLineEdit()

        if flag == 0:
            print(2)
            self.setWindowTitle('新建项目')
            label_product = QLabel(self, text="Project Name:")
            self._btn_ok = QPushButton(self, text="Create Project")
            self._grid.addWidget(self.lineEdit, 0, 1, 1, 3)
        elif flag == 1:
            self.setWindowTitle('新建文件')
            label_product = QLabel(self, text="File Name:")
            self._btn_ok = QPushButton(self, text="New File")
            self._cmb_index = QComboBox(self)
            self._cmb_index.addItems([".py", ".txt", ".juncfg"])
            self._grid.addWidget(self._cmb_index, 0, 3, 1, 1)
            self._grid.addWidget(self.lineEdit, 0, 1, 1, 2)
        elif flag == 2:
            self.setWindowTitle('pip包安装')
            label_product = QLabel(self, text="Package Name:")
            self._btn_ok = QPushButton(self, text="Install")
            self._grid.addWidget(self.lineEdit, 0, 1, 1, 3)
        elif flag == 3:
            label_product = QLabel(self, text="New Name:")
            self._btn_ok = QPushButton(self, text="Update")
            self.setWindowTitle('更新文件名称')
            self._grid.addWidget(self.lineEdit, 0, 1, 1, 3)
        elif flag == 4:
            label_product = QLabel(self, text="New Folder:")
            self._btn_ok = QPushButton(self, text="Create")
            self.setWindowTitle('创建文件')
            self._grid.addWidget(self.lineEdit, 0, 1, 1, 3)
        elif flag == 5:
            label_product = QLabel(self, text="New Plugin:")
            self._btn_ok = QPushButton(self, text="Create")
            self.setWindowTitle('新建插件')
            self._grid.addWidget(self.lineEdit, 0, 1, 1, 3)
        self._grid.addWidget(label_product, 0, 0, 1, 1)
        # self._grid.addWidget(self.lineEdit, 0, 1, 1, 2)
        self._grid.addWidget(self._btn_ok, 7, 0, 1, 4)
        self._btn_ok.clicked.connect(self._btn_ok_clicked)
        self._project_flag = False
        self.lineEdit.setFocus()

    def _btn_ok_clicked(self):
        name = self.lineEdit.text()
        if self.flag == 2:
            if self.install_flag is False:
                if name != '':
                    self.pip_install_thread = pip_install_thread(self, name)
                    self.pip_install_thread.start()
                    self.pip_install_thread.emit_signal_log.connect(self.show_message)
                    self.install_flag = True
                    self._btn_ok.setText('Installing')
            else:
                QMessageBox.critical(self, "error", "package正在安装，请在终端查看安装信息!!")
        elif self.flag == 3 or self.flag == 4 or self.flag == 5:
            a = []
            for i in range(self.tree.childCount()):
                a.append(self.tree.child(i).text(0))
            if name in a:
                QMessageBox.critical(self, "error", "不能与文件重复，请重新命名")
            else:
                self._project_flag = True
                self.close()

        elif self.flag == 0:
            print(self.lineEdit.text())
            if '/' in name or '.' in name or '-' in name or ' ' in name or len(name) == 0:
                QMessageBox.critical(self, "error", "文件名不能包含'/','.','-'")
            else:
                self.file_name = self.lineEdit.text()
                self._project_flag = True
                self.close()
        elif self.flag == 1:
            if '/' in name or '.' in name or '-' in name or ' ' in name or len(name) == 0:
                QMessageBox.critical(self, "error", "文件名不能包含'/','.','-'")
            else:
                self.file_name = self.lineEdit.text() + self._cmb_index.currentText()
                self._project_flag = True
                self.close()

    def get_create_success_flag(self):
        return self._project_flag

    def show_message(self):
        QMessageBox.critical(self, "Info", "Package 安装成功")
#
#
# if __name__ == '__main__':
#     app = QApplication(argv)
#     aw_add_product = NewProject()
#     aw_add_product.show()
#     exit(app.exec_())