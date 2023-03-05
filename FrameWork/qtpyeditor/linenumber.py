# -*- coding:utf-8 -*-
# @Time: 2021/1/18 18:23
# @Author: Zhanyi Hou
# @Email: 1295752786@qq.com
# @File: linenumber.py
#!/usr/bin/python3
# QcodeEditor.py by acbetter.
# 来源：https://stackoverflow.com/questions/40386194/create-text-area-textedit-with-line-number-in-pyqt
# -*- coding: utf-8 -*-

from PySide2.QtCore import Qt, QRect, QSize
from PySide2.QtWidgets import QWidget, QPlainTextEdit, QTextEdit
from PySide2.QtGui import QColor, QPainter, QTextFormat, QFont


class QLineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.codeEditor = editor

    def sizeHint(self):
        return QSize(self.editor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        self.codeEditor.lineNumberAreaPaintEvent(event)


class QCodeEditor(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        # QPlainTextEdit
        # monoEdit;
        # QTextDocument * doc = monoEdit.document();
        # QFont
        # font = doc->defaultFont();
        # font.setFamily("Courier New");
        # doc->setDefaultFont(font);
        # doc = self.document()
        # font = doc.defaultFont()
        # font.setPixelSize(20)
        # doc.setDefaultFont(font)
        # self._font = font

        self.lineNumberArea = QLineNumberArea(self)
        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)
        self.updateLineNumberAreaWidth(0)
        self.highlightCurrentLine()

    def lineNumberAreaWidth(self):
        digits = 1
        max_value = max(1, self.blockCount())
        while max_value >= 10:
            max_value /= 10
            digits += 1
        space = 3 + self.fontMetrics().width('9') * digits
        return space

    def updateLineNumberAreaWidth(self, _):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()))

    def highlightCurrentLine(self):
        """
        TODO:如何在不出现问题的情况下保证编辑器打开？
        :return:
        """
        # return
        extraSelections = []
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            lineColor = QColor("#2B2B2B").lighter(140)
            selection.format.setBackground(lineColor)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extraSelections.append(selection)
        self.setExtraSelections(extraSelections)

    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self.lineNumberArea)

        painter.fillRect(event.rect(), QColor("#262b34"))

        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()
        self.setStyleSheet("""
        font-size: 18px;
        """)
        # Just to make sure I use the right font
        height = self.fontMetrics().height()
        while block.isValid() and (top <= event.rect().bottom()):
            if block.isVisible() and (bottom >= event.rect().top()):
                number = str(blockNumber + 1)
                painter.setPen(QColor(118, 150, 185))
                painter.drawText(0, top, self.lineNumberArea.width(), height, Qt.AlignRight, number)

            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            blockNumber += 1


# if __name__ == '__main__':
#     import sys
#     from PySide2.QtWidgets import QApplication
#
#     app = QApplication(sys.argv)
#     codeEditor = QCodeEditor()
#     codeEditor.show()
#     sys.exit(app.exec_())