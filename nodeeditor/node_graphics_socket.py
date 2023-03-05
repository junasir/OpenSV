# -*- coding: utf-8 -*-
"""
A module containing Graphics representation of a :class:`~nodeeditor.node_socket.Socket`
"""
import math

from PySide2.QtWidgets import QGraphicsItem
from PySide2.QtGui import QColor, QBrush, QPen, QFontMetrics
from PySide2.QtCore import Qt, QRectF

SOCKET_COLORS = [
    QColor("#FFFF7700"), # Orange: Number (int or float)
    QColor("#FF52e220"), # Green: FreeCAD vector (FreeCAD.Base.Vector)
    QColor("#FF0056a6"), # Blue: Text (str)
    QColor("#FFa86db1"), # Purple: FreeCAD tree object (Part::PartFeature)
    QColor("#FFb54747"), # Brown
    QColor("#FFdbe220"), # Yellow
    QColor("#FF888888"), # Gray
    QColor("#FFFF7700"), # Orange 2
    QColor("#FF52e220"), # Green 2
    QColor("#FF0056a6"), # Blue 2
    QColor("#FFa86db1"), # Purple 2
    QColor("#FFb54747"), # Brown 2
    QColor("#FFdbe220"), # Yellow 2
    QColor("#FF888888"), # Gray 2
]

class QDMGraphicsSocket(QGraphicsItem):
    """Class representing Graphic `Socket` in ``QGraphicsScene``"""
    def __init__(self, socket:'Socket'):
        """
        :param socket: reference to :class:`~nodeeditor.node_socket.Socket`
        :type socket: :class:`~nodeeditor.node_socket.Socket`
        """
        super().__init__(socket.node.grNode)

        self.socket = socket

        self.isHighlighted = False

        self.radius = 6
        self.outline_width = 1
        self.initAssets()

    @property
    def socket_type(self):
        return self.socket.socket_type

    def getSocketColor(self, key):
        """Returns the ``QColor`` for this ``key``"""
        if type(key) == int: return SOCKET_COLORS[key]
        elif type(key) == str: return QColor(key)
        return Qt.transparent

    def changeSocketType(self):
        """Change the Socket Type"""
        self._color_background = self.getSocketColor(self.socket_type)
        self._brush = QBrush(self._color_background)
        # print("Socket changed to:", self._color_background.getRgbF())
        self.update()

    def initAssets(self):
        """Initialize ``QObjects`` like ``QColor``, ``QPen`` and ``QBrush``"""

        # determine socket color
        self._color_background = self.getSocketColor(self.socket_type)
        self._color_outline = QColor("#FF000000")
        self._color_highlight = QColor("#FF37A6FF")
        self._color_label = QColor("#FFFFFF")

        self._pen = QPen(self._color_outline)
        self._pen.setWidthF(self.outline_width)
        self._pen_highlight = QPen(self._color_highlight)
        self._pen_highlight.setWidthF(2.0)
        self._pen_label = QPen(self._color_label)
        self._brush = QBrush(self._color_background)

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        """Painting a circle and the socket label"""
        # Painting socket circle
        painter.setBrush(self._brush)
        painter.setPen(self._pen if not self.isHighlighted else self._pen_highlight)
        painter.drawEllipse(-self.radius, -self.radius, 2 * self.radius, 2 * self.radius)

        # Painting socket label
        painter.setPen(self._pen_label)
        label_metrics = QFontMetrics(painter.font())
        label_width = label_metrics.horizontalAdvance(self.socket.label)
        label_height = label_metrics.height()
        if self.socket.is_input:
            painter.drawText(self.radius + 5, int(label_height/4), self.socket.label)
        else:
            painter.drawText(-self.radius - label_width - 5, int(label_height / 4), self.socket.label)

    def boundingRect(self) -> QRectF:
        """Defining Qt' bounding rectangle"""
        return QRectF(
            - self.radius - self.outline_width,
            - self.radius - self.outline_width,
            2 * (self.radius + self.outline_width),
            2 * (self.radius + self.outline_width),
        )
