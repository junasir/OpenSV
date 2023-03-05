# coding:utf-8
import sys

from PySide2.QtCore import QEvent, Qt
from PySide2.QtWidgets import QHBoxLayout, QWidget, QLabel

from ..utils import startSystemMove
from .title_bar_buttons import CloseButton, MaximizeButton, MinimizeButton, SvgTitleBarButton


class TitleBar(QWidget):
    """ Title bar """

    def __init__(self, parent):
        super().__init__(parent)
        self.minBtn = MinimizeButton(parent=self)
        self.closeBtn = CloseButton(parent=self)
        self.maxBtn = MaximizeButton(parent=self)
        self.hBoxLayout = QHBoxLayout(self)
        self._isDoubleClickEnabled = True
        self.label = QLabel(self)
        self.label.move(0, 0)
        # self.label.resize(1920, 28)
        self.label.setStyleSheet("background-color:#323131;")

        self.resize(0, 0)
        self.setFixedHeight(28)

        # add buttons to layout
        self.hBoxLayout.setSpacing(0)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.addWidget(self.minBtn, 0, Qt.AlignRight)
        self.hBoxLayout.addWidget(self.maxBtn, 0, Qt.AlignRight)
        self.hBoxLayout.addWidget(self.closeBtn, 0, Qt.AlignRight)
        self.hBoxLayout.setAlignment(Qt.AlignRight)

        # connect signal to slot
        self.minBtn.clicked.connect(self.window().showMinimized)
        self.maxBtn.clicked.connect(self.__toggleMaxState)
        self.closeBtn.clicked.connect(self.window().close)

        self.window().installEventFilter(self)

    def eventFilter(self, obj, e):
        if obj is self.window():
            if e.type() == QEvent.WindowStateChange:
                self.maxBtn.setMaxState(self.window().isMaximized())
                return False

        return super().eventFilter(obj, e)

    def mouseDoubleClickEvent(self, event):
        """ Toggles the maximization state of the window """
        if event.button() != Qt.LeftButton or not self._isDoubleClickEnabled:
            return

        self.__toggleMaxState()

    def mouseMoveEvent(self, e):
        if sys.platform != "win32" or not self._isDragRegion(e.pos()):
            return

        startSystemMove(self.window(), e.globalPos())

    def mousePressEvent(self, e):
        if sys.platform == "win32" or e.button() != Qt.LeftButton or not self._isDragRegion(e.pos()):
            return

        startSystemMove(self.window(), e.globalPos())

    def __toggleMaxState(self):
        """ Toggles the maximization state of the window and change icon """
        if self.window().isMaximized():
            self.window().showNormal()
        else:
            self.window().showMaximized()

    def _isDragRegion(self, pos):
        """ Check whether the pressed point belongs to the area where dragging is allowed """
        return 0 < pos.x() < self.width() - 46 * 3

    def setDoubleClickEnabled(self, isEnabled):
        """ whether to switch window maximization status when double clicked

        Parameters
        ----------
        isEnabled: bool
            whether to enable double click
        """
        self._isDoubleClickEnabled = isEnabled
