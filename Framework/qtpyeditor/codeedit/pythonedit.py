# -*- coding:utf-8 -*-
# @Time: 2021/1/30 11:36
# @Author: Zhanyi Hou
# @Email: 1295752786@qq.com
# @File: pythonedit.py
import time
import re
from typing import Tuple, List, TYPE_CHECKING

from PySide2.QtGui import QTextCursor, QMouseEvent, QKeyEvent, QTextBlock
from PySide2.QtWidgets import QLabel, QListWidgetItem, QApplication
from PySide2.QtCore import QPoint, QModelIndex, Signal

from qtpyeditor.codeedit import PMBaseCodeEdit
from qtpyeditor.highlighters import PythonHighlighter
from qtpyeditor.Utilities import AutoCompThread

if TYPE_CHECKING:
    from jedi.api import Completion


class PMPythonCodeEdit(PMBaseCodeEdit):
    def __init__(self, parent=None, log=None):
        super(PMPythonCodeEdit, self).__init__(parent)
        self.user_logger = log
        # self.setLineWrapMode(QPlainTextEdit.NoWrap)
        # self.doc_tab_widget: 'PMGPythonEditor' = parent
        # self.filename = '*'
        # self.path = ''
        # self.modified = True
        self.highlighter = PythonHighlighter(self.document())
        self.setTabChangesFocus(False)
        self.autocomp_thread = AutoCompThread(log=self.user_logger)
        self.autocomp_thread.trigger.connect(self.on_autocomp_signal_received)
        self.autocomp_thread.start()

        self.setMouseTracking(True)
        self.last_mouse_position: QPoint = None
        self.last_mouse_moved = time.time()

        self.hint_widget = QLabel('', parent=self)
        self.hint_widget.setVisible(False)

    def on_autocomp_signal_received(self, text_cursor_content: tuple, completions: List['jedi.api.Completion']):
        '''
        当收到自动补全提示信号时，执行的函数。
        :param text_cursor_content:(row,col,hint_when_completion_triggered)
        :param completions:
        :return:
        '''

        hint = self._get_hint()
        self.user_logger.info('hint_when_completion_triggered:{0},current_hint:{1}'.format(text_cursor_content[2], hint))
        if hint.startswith(text_cursor_content[2]):
            if len(completions) == 1:
                if completions[0].name == self._get_hint():
                    self.hide_autocomp()
                    return
            self.autocomp_show(completions)
        else:
            self.hide_autocomp()

    def hide_autocomp(self):
        self.popup_hint_widget.hide_autocomp()

    def on_text_changed(self):
        super(PMPythonCodeEdit, self).on_text_changed()
        self._get_textcursor_pos()
        cursor_pos = self.cursorRect()
        self.popup_hint_widget.setGeometry(
            cursor_pos.x() + 5, cursor_pos.y() + 20,
            self.popup_hint_widget.sizeHint().width(),
            self.popup_hint_widget.sizeHint().height())
        self._request_autocomp()

    def _insert_autocomp(self, e: QModelIndex = None):
        row = self.popup_hint_widget.currentRow()
        if 0 <= row < self.popup_hint_widget.count():
            complete, word_type = self.popup_hint_widget.get_complete(row)
            word = self.popup_hint_widget.get_text(row)
            if not word.startswith(self._get_hint()):
                return
            comp = word[len(self._get_hint()):]
            self.insertPlainText(comp)
            textcursor: QTextCursor = self.textCursor()
            word = self.get_word(textcursor.blockNumber(), textcursor.columnNumber() - 1)
            if word_type == 'function':
                self.insertPlainText('()')
                tc = self.textCursor()
                tc.movePosition(QTextCursor.PreviousCharacter)
                self.setTextCursor(tc)
            elif word_type == 'keyword':
                self.insertPlainText(' ')
            self.popup_hint_widget.hide()

    def _get_nearby_text(self):
        block_text = self.textCursor().block().text()
        col = self.textCursor().columnNumber()
        return block_text[:col]

    def _get_hint(self):
        block_text = self.textCursor().block().text()
        if block_text.lstrip().startswith('#'):  # 在注释中
            return ''
        col = self.textCursor().columnNumber()
        nearby_text = block_text[:col]
        hint = re.split(
            '[.:;,?!\s \+ \- = \* \\ \/  \( \)\[\]\{\} ]', nearby_text)[-1]
        return hint

    def _request_autocomp(self):
        pos = self._get_textcursor_pos()
        nearby_text = self._get_nearby_text()
        hint = self._get_hint()

        if hint == '' and not nearby_text.endswith(('.', '\\\\', '/')):
            self.popup_hint_widget.hide_autocomp()
            return
        self.autocomp_thread.text_cursor_pos = (pos[0] + 1, pos[1])
        self.autocomp_thread.text = self.toPlainText()

    def autocomp_show(self, completions: List['Completion']):
        l = []
        if len(completions) != 0:
            self.popup_hint_widget.set_completions(completions)
        else:
            self.popup_hint_widget.hide()
        self.popup_hint_widget.autocomp_list = l

    def _get_textcursor_pos(self) -> Tuple[int, int]:
        return self.textCursor().blockNumber(), self.textCursor().columnNumber()

    def mousePressEvent(self, a0: QMouseEvent) -> None:
        # PluginInterface.show_tool_bar('code_editor_toolbar')
        if self.popup_hint_widget.isVisible():
            self.popup_hint_widget.hide_autocomp()
        super().mousePressEvent(a0)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        super().keyPressEvent(event)

    def on_back_tab(self):
        cursor = self.textCursor()
        if cursor.hasSelection():
            self.editUnindent()
        else:
            cursor = self.textCursor()
            cursor.clearSelection()
            cursor.movePosition(QTextCursor.StartOfBlock)
            for i in range(4):
                cursor.movePosition(QTextCursor.NextCharacter, QTextCursor.KeepAnchor, 1)
                if not cursor.selectedText().endswith(' '):
                    cursor.movePosition(QTextCursor.PreviousCharacter, QTextCursor.KeepAnchor, 1)
                    break
            cursor.removeSelectedText()

    def on_tab(self):
        cursor = self.textCursor()
        if cursor.hasSelection():
            self.editIndent()
            return
        else:
            nearby_text = self._get_nearby_text()
            hint = self._get_hint()

            if hint == '' and not nearby_text.endswith(('.', '\\\\', '/')):
                cursor = self.textCursor()
                cursor.insertText("    ")
            else:
                self._request_autocomp()

    def mouseMoveEvent(self, e: QMouseEvent):
        """
        鼠标移动
        移动到marker上的时候，便弹出提示框。
        :param e:
        :return:
        """
        super(PMPythonCodeEdit, self).mouseMoveEvent(e)
        cursor: QTextCursor = self.cursorForPosition(e.pos())

        if not self.should_check_code():
            return
        line, col = cursor.blockNumber(), cursor.positionInBlock()
        flag = False
        text = ''
        if line in self.highlighter.highlight_marks:
            marker_propertys = self.highlighter.highlight_marks.get(line)
            for marker_property in marker_propertys:
                start = marker_property[0]
                if marker_property[1] == -1:
                    end = len(cursor.block().text())
                else:
                    end = start + marker_property[1]
                if start <= col < end:
                    flag = True
                    text += marker_property[3] + '\n'
                    break

        self.hint_widget.setGeometry(e.x() + 30, e.y(),
                                     self.hint_widget.sizeHint().width(), self.hint_widget.sizeHint().height())

        self.hint_widget.setText(text.strip())
        self.hint_widget.setVisible(flag)

    def should_check_code(self) -> bool:
        """
        返回是否会对代码做insight.
        :return:
        """
        return len(self.toPlainText()) < 10000 * 120


# if __name__ == '__main__':
#     app = QApplication([])
#     e = PMPythonCodeEdit()
#     e.show()
#     app.exec_()
