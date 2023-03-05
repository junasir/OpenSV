from sys import argv

from PySide2.QtCore import Qt, Signal, QRect, QSize
from PySide2.QtGui import QIcon, QPainter, QCursor
from PySide2.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QPushButton, QApplication


class JuMysqlLogin(QWidget):
    download_signal = Signal(str, int)
    update_table_signal = Signal(str)

    def __init__(self, parent=None, logger=None, username=None, chip_name=None, ip_handle=None, plugin_menu=None,
                 *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.setWindowTitle("Online Login")
        self.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        self._init_ui()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.resize(350, 250)
        self.setMaximumSize(QSize(350, 250))
        self.setMinimumSize(QSize(350, 250))

    def _init_ui(self):
        gridLayoutWidget = QWidget(self)
        gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        gridLayoutWidget.setGeometry(QRect(70, 40, 211, 141))
        gridLayout = QGridLayout(gridLayoutWidget)
        gridLayout.setObjectName(u"gridLayout")
        gridLayout.setContentsMargins(0, 0, 0, 0)
        self.label_account = QLabel(gridLayoutWidget)
        self.label_account.setObjectName(u"label_account")
        self.label_account.setMaximumSize(QSize(20, 20))
        self.label_account.setScaledContents(True)
        gridLayout.addWidget(self.label_account, 0, 0, 1, 1)
        self.label_password = QLabel(gridLayoutWidget)
        self.label_password.setObjectName(u"label_password")
        self.label_password.setMaximumSize(QSize(20, 20))
        self.label_password.setScaledContents(True)
        gridLayout.addWidget(self.label_password, 1, 0, 1, 1)
        self.lineEdit_account = QLineEdit(gridLayoutWidget)
        self.lineEdit_account.setObjectName(u"lineEdit_account")
        gridLayout.addWidget(self.lineEdit_account, 0, 1, 1, 1)
        self.lineEdit_password = QLineEdit(gridLayoutWidget)
        self.lineEdit_password.setObjectName(u"lineEdit_2")
        gridLayout.addWidget(self.lineEdit_password, 1, 1, 1, 1)
        self.pushButton_login = QPushButton(self)
        self.pushButton_login.setObjectName(u"pushButton_login")
        self.pushButton_login.setGeometry(QRect(130, 180, 101, 31))
        self.label_account.setPixmap("./act.png")
        self.label_password.setPixmap("./psd.png")
        self.lineEdit_password.setEchoMode(QLineEdit.Password)
        self.pushButton_login.setText("Login")

        self.pushButton_close = QPushButton(self)
        self.pushButton_close.setObjectName(u"pushButton_close")
        self.pushButton_close.setGeometry(QRect(320, 5, 20, 20))
        self.pushButton_close.setStyleSheet("QPushButton{border-image: url(./JuResource/img/close_1.png)}")
        self.pushButton_close.clicked.connect(self.close)

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

#
# if __name__ == '__main__':
#
#     app = QApplication(argv)
#     MainWindow = JuMysqlLogin()
#     # MainWindow = Ju_Test_Ui_New()
#     app.setWindowIcon(QIcon("./JuResource/img/icon.ico"))
#     MainWindow.show()
#     exit(app.exec_())
