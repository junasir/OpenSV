
from pyautogui import position
from PySide2.QtCore import Qt, Signal
from PySide2.QtGui import QFont, QColor
from PySide2.QtWidgets import QHBoxLayout, QLabel, QSpacerItem, QSizePolicy, QWidget, QPushButton
from win32api import GetMonitorInfo, MonitorFromPoint


class JuTitleBar(QWidget):

    # 窗口最小化信号
    windowMinimumed = Signal()
    # 窗口最大化信号
    windowMaximumed = Signal()
    # 窗口还原信号
    windowNormaled = Signal()
    # 窗口关闭信号
    windowClosed = Signal()
    # 窗口移动
    windowMoved = Signal(int, int, int, bool)

    def __init__(self, *args, **kwargs):
        super(JuTitleBar, self).__init__(*args, **kwargs)

        # 支持qss设置背景
        monitor_info = GetMonitorInfo(MonitorFromPoint((0, 0)))
        monitor_height = monitor_info["Monitor"][-1]
        # print('monitor info:{}'.format(monitor_info))  # 监视器信息
        monitor = monitor_info.get('Monitor')
        work = monitor_info.get('Work')  # 工作区间
        work_lan = monitor[3] - work[3]
        self.max_move = monitor_height - work_lan -20
        # print('任务栏高度:{}'.format(monitor[3] - work[3]))  # 任务栏高度
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.mPos = None
        self.iconSize = 20  # 图标的默认大小
        # 设置默认背景颜色,否则由于受到父窗口的影响导致透明
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(palette.Window, QColor(240, 240, 240))
        self.setPalette(palette)
        # 布局
        layout = QHBoxLayout(self, spacing=0)
        layout.setContentsMargins(0, 0, 0, 0)
        # 窗口图标
        self.iconLabel = QLabel(self)
#         self.iconLabel.setScaledContents(True)
        layout.addWidget(self.iconLabel)
        # 窗口标题
        self.titleLabel = QLabel(self)
        self.titleLabel.setMargin(2)
        layout.addWidget(self.titleLabel)
        # 中间伸缩条
        layout.addSpacerItem(QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        # 利用Webdings字体来显示图标
        font = self.font() or QFont()
        font.setFamily('Webdings')
        # 最小化按钮
        self.buttonMinimum = QPushButton(
            '0', self, clicked=self.windowMinimumed.emit, font=font, objectName='buttonMinimum')
        layout.addWidget(self.buttonMinimum)
        # 最大化/还原按钮
        self.buttonMaximum = QPushButton(
            '1', self, clicked=self.showMaximized, font=font, objectName='buttonMaximum')
        layout.addWidget(self.buttonMaximum)
        # 关闭按钮
        self.buttonClose = QPushButton(
            'r', self, clicked=self.windowClosed.emit, font=font, objectName='buttonClose')
        layout.addWidget(self.buttonClose)
        # 初始高度
        self.setHeight()
        self.flag_max_release = False
        self.flag_normal = False
        self.flag_move = False
        self.setStyleSheet("""
                /*标题栏*/
                JuTitleBar {
                    background-color: #3C3F41;
                }
                QWidget{
                    color:#FFFFFF;
                    font-size:16px;
                    border-bottom:0.5px solid #515151;
                }
                /*最小化最大化关闭按钮通用默认背景*/
                #buttonMinimum,#buttonMaximum,#buttonClose {
                    border: none;
                                        border-width: 1px;
                   border-bottom:0.5px solid #515151;
                    background-color: #3C3F41;
                }
                /*悬停*/
                #buttonMinimum:hover,#buttonMaximum:hover {
                    background-color: #4F5254;
                    color: white;
                }
                #buttonClose:hover {
                    background-color: red;
                    color: white;
                }

                /*鼠标按下不放*/
                #buttonMinimum:pressed,#buttonMaximum:pressed {
                    background-color: Firebrick;
                }
                #buttonClose:pressed {
                    color: white;
                    background-color: Firebrick;
                }
                #buttonClose:hover {
                    color: white;
                }
                """)

    def showMaximized(self):
        if self.buttonMaximum.text() == '1':
            # 最大化
            self.buttonMaximum.setText('2')
            self.flag_normal = True
            self.windowMaximumed.emit()
        else:  # 还原
            self.buttonMaximum.setText('1')
            self.windowNormaled.emit()
            self.flag_normal = False

    def setHeight(self, height=25):
        """设置标题栏高度"""
        self.setMinimumHeight(height)
        self.setMaximumHeight(height)
        # 设置右边按钮的大小
        self.buttonMinimum.setMinimumSize(height, height)
        self.buttonMinimum.setMaximumSize(height, height)
        self.buttonMaximum.setMinimumSize(height, height)
        self.buttonMaximum.setMaximumSize(height, height)
        self.buttonClose.setMinimumSize(height, height)
        self.buttonClose.setMaximumSize(height, height)

    def setTitle(self, title):
        """设置标题"""
        self.titleLabel.setText(title)

    def setIcon(self, icon):
        """设置图标"""
        self.iconLabel.setPixmap(icon.pixmap(self.iconSize, self.iconSize))

    def setIconSize(self, size):
        """设置图标大小"""
        self.iconSize = size

    def enterEvent(self, event):
        self.setCursor(Qt.ArrowCursor)
        super(JuTitleBar, self).enterEvent(event)

    def mouseDoubleClickEvent(self, event):
        super(JuTitleBar, self).mouseDoubleClickEvent(event)
        self.showMaximized()

    def mousePressEvent(self, event):
        """鼠标点击事件"""
        if event.button() == Qt.LeftButton:
            self.mPos = event.pos()
        event.accept()

    def mouseReleaseEvent(self, event):
        '''鼠标弹起事件'''
        if self.flag_max_release:
            self.flag_max_release = False
            self.buttonMaximum.setText('1')
            self.showMaximized()
        self.flag_move = False
        self.mPos = None
        event.accept()

    def mouseMoveEvent(self, event):
        x, y = position()
        if y < 5:
            if self.flag_max_release is False:
                self.flag_max_release = True
        else:
            self.flag_max_release = False
        if y < 38:
            if self.flag_normal:
                self.flag_move = True
                self.flag_max_release = False
                self.showMaximized()
        if event.buttons() == Qt.LeftButton and self.mPos:
            pos_x = self.mapToGlobal(event.pos() - self.mPos).x()
            pos_y = self.mapToGlobal(event.pos() - self.mPos).y()
            if self.max_move < y:
                pos_y = self.max_move
            self.windowMoved.emit(pos_x, pos_y, x, self.flag_move)
        event.accept()