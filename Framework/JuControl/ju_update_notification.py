#!/usr/bin/env python3
# cython: language_level=3
# -*- coding: utf-8 -*-

r"""
"""

__author__ = "Jiang Jun"

from PySide2.QtCore import QRectF, Qt, Signal
from PySide2.QtGui import QPainter, QPainterPath, QColor, QPen, QPixmap, QImage, QCursor
from PySide2.QtWidgets import QLabel, QWidget, QGridLayout, QApplication, QPushButton, QAction


class JuUpdateNotification(QWidget):
    btn_clicked_signal = Signal(QAction)

    def __init__(self, parent=None, text_info=None, rgb="#696969", mode=None, *args, **kwargs):
        super(JuUpdateNotification, self).__init__(parent, *args, **kwargs)
        if mode is not None:
            self.setStyleSheet(mode)
        self.a = 121
        self._color = rgb
        self._background_color = QColor(self._color)
        self._border_color = QColor(self._color)
        self._title_text = text_info[0]
        self._content_text = text_info[1]
        self._btn_text = text_info[2]
        self._setup_ui()

    def set_color(self, rgb="#696969"):
        """set background color and border color"""
        self._color = rgb
        self._background_color = QColor(self._color)
        self._border_color = QColor(self._color)

    def _setup_ui(self):
        info_pixmap = QPixmap(QImage("AwResource/image/info.png")).scaled(20, 20)
        close_pixmap = QPixmap(QImage("AwResource/image/close_win.png")).scaled(20, 20)
        self.setMinimumHeight(80)
        grid_layout = QGridLayout(self)
        grid_layout.setContentsMargins(8, 8, 8, 16)

        info_label = QLabel(self)
        info_label.setMaximumSize(20, 20)
        info_label.setPixmap(info_pixmap)
        grid_layout.addWidget(info_label, 0, 0, 1, 1)
        self._title_label = QLabel(self, text=self._title_text)
        grid_layout.addWidget(self._title_label, 0, 1, 1, 3)

        close_label = AwLabel(self)
        close_label.close_signal.connect(self.close_info)
        close_label.setPixmap(close_pixmap)
        close_label.setAlignment(Qt.AlignRight)
        close_label.setCursor(QCursor(Qt.PointingHandCursor))
        close_label.setMaximumSize(20, 20)
        grid_layout.addWidget(close_label, 0, 4, 1, 1)

        self._content_label = QLabel(self)
        if self._content_text == "" or self._content_text is None:
            self._content_label.setVisible(False)
        else:
            self._content_label.setText(self._content_text)
            self._content_label.setAlignment(Qt.AlignLeft)
            grid_layout.addWidget(self._content_label, 1, 1, 1, 1)

        operate_btn = QPushButton(self)
        operate_btn.setText(self._btn_text)
        operate_btn.setStyleSheet(
            "QPushButton{border:none;background:transparent;color:rgb(44, 167, 146);text-align:left;}"
            "QPushButton:hover{border:none;color:rgb(44, 167, 146);text-align:left;}")
        operate_btn.setCursor(QCursor(Qt.PointingHandCursor))
        operate_btn.clicked.connect(self._btn_clicked)
        grid_layout.addWidget(operate_btn, 2, 1, 1, 1)

    def set_title_text(self, text=""):
        """set text of title"""
        if type(text) is str:
            self._title_label.setText(text)
            QApplication.processEvents()

    def set_content_text(self, text=""):
        """set text of content"""
        if type(text) is str:
            self._content_label.setText(text)
            if text != "":
                self._content_label.setVisible(True)
            else:
                self._content_label.setVisible(False)
            QApplication.processEvents()

    def set_button_text(self, text=""):
        """set text of button"""
        if type(text) is str:
            self._title_label.setText(text)
            QApplication.processEvents()

    def close_info(self):
        self.close()

    def win_show(self):
        self.show()

    def _btn_clicked(self):
        text_info = "Plugin Admin"
        if self._btn_text == "Update":
            text_info = "Check for Update"
        action = QAction(self, text=text_info, objectName=text_info)
        self.btn_clicked_signal.emit(action)
        # self._close_info()

    def paintEvent(self, event):
        super(JuUpdateNotification, self).paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rectPath = QPainterPath()
        height = self.height() - 8
        rectPath.addRoundedRect(QRectF(0, 0, self.width(), height), 5, 5)
        painter.setPen(QPen(self._background_color, 1, Qt.SolidLine,
                            Qt.RoundCap, Qt.RoundJoin))
        painter.setBrush(self._border_color)
        painter.drawPath(rectPath)
        painter.setPen(QPen(self._border_color, 1,
                            Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))


class AwLabel(QLabel):
    close_signal = Signal()

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        if event.button() == Qt.LeftButton:
            self.close_signal.emit()

#
# if __name__ == '__main__':
#     app = QApplication(argv)
#     window = JuUpdateNotification(title_text=None, content_text=None, btn_text="Update...")
#     window.win_show()
#     exit(app.exec_())
