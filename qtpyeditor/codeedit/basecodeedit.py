# -*- coding:utf-8 -*-
# @Time: 2021/1/18 9:26
# @Author: Zhanyi Hou
# @Email: 1295752786@qq.com
# @File: basecodeedit.py
import os
import re
import time
from itertools import groupby
from queue import Queue

from PySide2.QtGui import QDropEvent, QPixmap

from PySide2.QtWidgets import QAction, QAbstractItemView
from PySide2.QtCore import QRegExp, Qt, QModelIndex, Signal, QThread, QCoreApplication, QTimer, QUrl, QSize
from PySide2.QtWidgets import QApplication, QFileDialog, QTextEdit, QTabWidget, \
    QMessageBox, QListWidget, QListWidgetItem, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPlainTextEdit, QShortcut, \
    QTableWidget, QTableWidgetItem, QHeaderView
from PySide2.QtGui import QTextCursor, QKeyEvent, QMouseEvent, QIcon, QKeySequence, QFocusEvent, QColor, QTextFormat, \
    QPainter, QTextDocument, QTextBlock
from typing import List, Tuple, Dict, TYPE_CHECKING

from qtpyeditor.highlighters.python import PythonHighlighter
from qtpyeditor.syntaxana import getIndent

from qtpyeditor.linenumber import QCodeEditor

# from pmgwidgets import create_icon

if TYPE_CHECKING:
    from jedi.api import Completion



def create_icons():
    icons = {}
    icon_folder = "JuResource/icons/autocomp"
    # icon_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'icons', 'autocomp')
    for icon_file_name in os.listdir(icon_folder):
        icon_abso_path = os.path.join(icon_folder, icon_file_name)
        icon1 = QIcon()  # create_icon(icon_abso_path)
        icon1.addPixmap(QPixmap(icon_abso_path), QIcon.Normal, QIcon.Off)
        icons[icon_file_name[:-4]] = icon1

    return icons


class AutoCompList(QTableWidget):
    # {'module':}  # , class, instance, function, param, path, keyword, property and statement.'}
    ROLE_NAME = 15
    ROLE_TYPE = 16
    ROLE_COMPLETE = 17
    ROLE_COMPLETION = 18

    def __init__(self, parent: 'PMBaseCodeEdit' = None):
        super().__init__(parent)
        self._parent: 'PMBaseCodeEdit' = parent
        self.last_show_time = 0
        self.icons = create_icons()
        self.verticalHeader().setDefaultSectionSize(20)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.horizontalHeader().hide()

        self.setStyleSheet("AutoCompList{selection-background-color: #515457;background-color:#46484A;"
                           "color: #BBBBBB;selection-color:#579CDD}")
        self.verticalHeader().setMinimumWidth(20)
        # self.horizontalHeader().setMinimumWidth(300)
        # self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setColumnHidden(0, True)
        self.setColumnHidden(1, True)
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

    def verticalHeader(self) -> QHeaderView:
        return super(AutoCompList, self).verticalHeader()

    def show(self) -> None:
        self.last_show_time = time.time()
        super().show()

    def hide_autocomp(self):
        """
        隐藏自动补全菜单并且主界面设置焦点。
        :return:
        """
        self.hide()
        self._parent.setFocus()

    def count(self):
        return self.rowCount()

    def keyPressEvent(self, e: QKeyEvent) -> None:
        if self.isVisible():
            if e.key() == Qt.Key_Return or e.key() == Qt.Key_Tab:
                self._parent._insert_autocomp()
                self._parent.setFocus()
                e.accept()
                return
            elif e.key() == Qt.Key_Escape:
                self.hide()
                self._parent.setFocus()
                return
            elif e.key() == Qt.Key_Up or e.key() == Qt.Key_Down:
                super().keyPressEvent(e)
                e.accept()
                return
            elif e.key() == Qt.Key_Left or e.key() == Qt.Key_Right:
                self.hide_autocomp()
            elif e.key() == Qt.Key_Control or e.key() == Qt.Key_Alt:  # 按下Ctrl键时，不关闭界面，因为可能存在快捷键。
                pass
            else:
                if (Qt.Key_0 <= e.key() <= Qt.Key_9) and (
                        e.modifiers() == Qt.ControlModifier or e.modifiers() == Qt.AltModifier):
                    index = e.key() - Qt.Key_0
                    if 0 <= index < self.count():
                        self.setCurrentItem(self.item(index, 0))
                        self._parent._insert_autocomp()
                        self._parent.setFocus()
                        self.hide()
                        e.accept()
                        return
                self.hide_autocomp()
                e.ignore()
                return
        super().keyPressEvent(e)
        e.ignore()

    def set_completions(self, completions: List['Completion']):
        """
        module, class, instance, function, param, path, keyword, property and statement.
        :param completions:
        :return:
        """

        t0 = time.time()
        self.setRowCount(0)
        self.items_list = []
        self.setRowCount(len(completions))
        self.setColumnCount(1)
        labels = []
        for i, completion in enumerate(completions):
            item = QTableWidgetItem(completion.name)
            item.setData(AutoCompList.ROLE_NAME, completion.name)

            item.setData(AutoCompList.ROLE_COMPLETION, completion)
            item.setText(completion.name)
            # if i < 30:  # 当条目数太多的时候，不能添加图标，否则速度会非常慢
            #     icon = self.icons.get(completion.type)
            #     if icon is not None:
            #         item.setIcon(icon)

            self.setItem(i, 0, item)
            if 0 <= i <= 9:
                labels.append(str(i))
            else:
                labels.append('')
        self.setVerticalHeaderLabels(labels)
        self.show()
        self.setFocus()
        self.setCurrentItem(self.item(0, 0))
        t1 = time.time()
        # logger.info('completion time:{0},completion list length:{1}'.format(t1 - t0, len(completions)))

    def get_complete(self, row: int) -> Tuple[str, str]:
        return self.item(row, 0).data(AutoCompList.ROLE_COMPLETION).complete, self.item(row, 0).data(
            AutoCompList.ROLE_COMPLETION).type

    def get_text(self, row: int) -> str:
        return self.item(row, 0).text()


class PMBaseCodeEdit(QCodeEditor):
    # cursorPositionChanged = Signal()
    signal_save = Signal()
    signal_focused_in = Signal(
        QFocusEvent)  # Signal Focused in . But as it was too often triggered, I use click event instead.
    signal_idle = Signal()
    signal_text_modified = Signal()  # If status changed from unmodified to modified, this signal emits.
    signal_file_dropped = Signal(str)
    UPDATE_CODE_HIGHLIGHT = 1

    def __init__(self, parent=None):
        super(PMBaseCodeEdit, self).__init__(parent)
        self._last_operation: float = 0.0  # 记录上次操作的时间
        self.update_request_queue = Queue()
        self.user_logger = parent.user_logger
        self.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.doc_tab_widget: 'PMGPythonEditor' = parent
        self.filename = '*'
        self.path = ''
        self.modified = False
        self._last_text = ''
        self.highlighter: 'PythonHighlighter' = None
        self.text_modified_signal_allowed = True
        self.setTabChangesFocus(False)

        self.textChanged.connect(self.on_text_changed)

        self.popup_hint_widget = AutoCompList(self)
        self.popup_hint_widget.doubleClicked.connect(self._insert_autocomp)
        self.popup_hint_widget.hide()
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui_update_timer = QTimer()
        self.ui_update_timer.start(300)

        self.ui_update_timer.timeout.connect(self.update_ui)

        self.textChanged.connect(self.update_last_operation_time)

    def update_last_operation_time(self):
        """
        更新上一次操作的时间
        :return:
        """
        self._last_operation = time.time()

    def update_ui(self):
        if not self.isVisible():
            return
        if time.time() - self._last_operation > 0.5:
            if self.update_request_queue.qsize() > 0:

                action: int = self.update_request_queue.get()
                if action == self.UPDATE_CODE_HIGHLIGHT:
                    self.text_modified_signal_allowed = False
                    focus_widget: QWidget = QApplication.focusWidget()
                    self.highlighter.rehighlight()
                    self.text_modified_signal_allowed = True
                    if focus_widget is not None:
                        focus_widget.setFocus()

    def on_autocomp_signal_received(self, text_cursor_pos: tuple, completions: List['jedi.api.classes.Completion']):
        '''
        当收到自动补全提示信号时，执行的函数。
        :param text_cursor_pos:
        :param completions:
        :return:
        '''
        current_cursor_pos = self._get_textcursor_pos()
        if current_cursor_pos[0] + 1 == text_cursor_pos[0] and current_cursor_pos[1] == text_cursor_pos[1]:
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
        """
        文字发生改变时的方法
        :return:
        """
        if self.modified == True:
            pass
        else:
            if self.toPlainText() != self._last_text:
                self.modified = True
                if self.text_modified_signal_allowed:
                    self.signal_text_modified.emit()
            else:
                pass
        self._last_text = self.toPlainText()

    def _insert_autocomp(self, e: QModelIndex = None):
        print(e)
        raise NotImplementedError

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

    def autocomp_show(self, completions: list):
        raise NotImplementedError

    def _get_textcursor_pos(self) -> Tuple[int, int]:
        return self.textCursor().blockNumber(), self.textCursor().columnNumber()

    def mousePressEvent(self, a0: QMouseEvent) -> None:
        if self.popup_hint_widget.isVisible():
            self.popup_hint_widget.hide_autocomp()
        self.signal_focused_in.emit(None)
        super().mousePressEvent(a0)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        k = event.key()
        if k == Qt.Key_Tab:
            self.on_tab()
            return
        elif k == Qt.Key_Backtab:
            self.on_back_tab()
            return
        elif k == Qt.Key_S and event.modifiers() == Qt.ControlModifier:
            self.save()
            return
        elif k == Qt.Key_Slash and event.modifiers() == Qt.ControlModifier:
            self.comment()
        elif k == Qt.Key_Return:
            if not self.textCursor().atBlockEnd():
                pass
            else:
                self.on_return_pressed()
                event.accept()
                return
        elif k == Qt.Key_Backspace:
            self.on_backspace(event)
            event.accept()
            return
        elif k == Qt.Key_ParenLeft:
            cursor = self.textCursor()
            cursor.beginEditBlock()
            cursor.insertText('()')
            cursor.movePosition(QTextCursor.PreviousCharacter, QTextCursor.MoveAnchor, 1)
            cursor.endEditBlock()
            self.setTextCursor(cursor)
            event.accept()
            return
        elif k == Qt.Key_BracketLeft:
            cursor = self.textCursor()
            cursor.beginEditBlock()
            cursor.insertText('[]')
            cursor.movePosition(QTextCursor.PreviousCharacter, QTextCursor.MoveAnchor, 1)
            cursor.endEditBlock()
            self.setTextCursor(cursor)
            event.accept()
            return
        elif k == Qt.Key_BraceLeft:
            cursor = self.textCursor()
            cursor.beginEditBlock()
            cursor.insertText('{}')
            cursor.movePosition(QTextCursor.PreviousCharacter, QTextCursor.MoveAnchor, 1)
            cursor.endEditBlock()
            self.setTextCursor(cursor)

            event.accept()
            return
        super().keyPressEvent(event)

    def on_backspace(self, key_backspace_event: QKeyEvent):
        cursor: QTextCursor = self.textCursor()
        cursor.beginEditBlock()
        previous_text = cursor.block().text()[:cursor.positionInBlock()]
        if previous_text.strip() == '':
            move_left = (cursor.columnNumber()) % 4
            if cursor.positionInBlock() == 0:
                move_left = 1  # 如果位于一行起始位置，就向左删除一个。
            else:
                if move_left == 0:  # 如果不位于起始位置且余数等于0，就向左删除一些。
                    move_left = 4

            for i in range(move_left):
                cursor.deletePreviousChar()
        else:
            cursor.deletePreviousChar()
        cursor.endEditBlock()

    def on_return_pressed(self):
        '''
        按回车换行的方法
        :return:
        '''
        cursor = self.textCursor()
        cursor.beginEditBlock()
        text = cursor.block().text()
        text, indent = getIndent(text)

        if text.endswith(':'):
            cursor.insertText('\n' + ' ' * (indent + 4))
        else:
            cursor.insertText('\n' + ' ' * indent)
        cursor.endEditBlock()

    def comment(self):
        cursor = self.textCursor()

        cursor.beginEditBlock()
        if cursor.hasSelection():
            start = cursor.anchor()
            end = cursor.position()

            if start > end:
                start, end = end, start

            cursor.clearSelection()

            cursor.setPosition(start)
            cursor.movePosition(QTextCursor.StartOfLine)
            start_line = cursor.blockNumber()

            start = cursor.position()  # 将光标移动到行首，获取行首的位置
            cursor.setPosition(end)  # 将光标设置到末尾
            cursor.movePosition(QTextCursor.StartOfLine)  # 将光标设置到选区最后一行
            end_line = cursor.blockNumber()  # 获取光标的行号

            cursor.setPosition(start)
            current_line = cursor.blockNumber()
            last_line = current_line
            while current_line <= end_line:
                line_text, indent = getIndent(cursor.block().text())
                if line_text.startswith('#'):
                    cursor.movePosition(
                        QTextCursor.NextCharacter, QTextCursor.MoveAnchor, indent)
                    cursor.deleteChar()
                else:
                    cursor.insertText('#')
                cursor.movePosition(QTextCursor.StartOfLine)
                cursor.movePosition(QTextCursor.Down)
                current_line = cursor.blockNumber()
                if current_line == last_line:
                    break
                last_line = current_line

            cursor.movePosition(QTextCursor.StartOfLine)
        else:
            cursor.movePosition(QTextCursor.StartOfLine)
            line_text, indent = getIndent(cursor.block().text())
            if line_text.startswith('#'):
                cursor.movePosition(QTextCursor.NextCharacter,
                                    QTextCursor.MoveAnchor, indent)
                cursor.deleteChar()
            else:
                cursor.insertText('#')
            pass

        cursor.endEditBlock()

    def on_back_tab(self):
        cursor = self.textCursor()
        if cursor.hasSelection():
            self.editUnindent()

        else:
            cursor = self.textCursor()
            cursor.clearSelection()

            cursor.movePosition(QTextCursor.StartOfBlock)

            for i in range(4):
                cursor.movePosition(QTextCursor.NextCharacter,
                                    QTextCursor.KeepAnchor, 1)
                if not cursor.selectedText().endswith(' '):
                    cursor.movePosition(QTextCursor.PreviousCharacter,
                                        QTextCursor.KeepAnchor, 1)
                    break
            # print('cursor.selected',cursor.selectedText())
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

    def editIndent(self):
        cursor = self.textCursor()
        cursor.beginEditBlock()
        if cursor.hasSelection():
            start = pos = cursor.anchor()
            start_line = self.document().findBlock(start)
            end = cursor.position()

            if start > end:
                start, end = end, start
                pos = start
            cursor.clearSelection()

            cursor.setPosition(end)
            cursor.movePosition(QTextCursor.StartOfLine)
            end = cursor.position()
            cursor.setPosition(start)
            cursor.movePosition(QTextCursor.StartOfLine)
            start = cursor.position()

            cursor.setPosition(end)
            while pos >= start:
                cursor.insertText("    ")

                cursor.movePosition(QTextCursor.Up)
                cursor.movePosition(QTextCursor.StartOfLine)
                lastPos = pos
                pos = cursor.position()
                if lastPos == pos:
                    break
            cursor.setPosition(start)
            cursor.movePosition(QTextCursor.NextCharacter,
                                QTextCursor.KeepAnchor, end - start)
        cursor.endEditBlock()
        return True

    def editUnindent(self):
        cursor = self.textCursor()
        cursor.beginEditBlock()
        if cursor.hasSelection():
            start = pos = cursor.anchor()
            end = cursor.position()
            if start > end:
                start, end = end, start
                pos = start
            cursor.clearSelection()
            cursor.setPosition(start)
            cursor.movePosition(QTextCursor.StartOfLine)
            start = cursor.position()
            cursor.setPosition(end)
            cursor.movePosition(QTextCursor.StartOfLine)
            end = cursor.position()
            while pos >= start:
                cursor.movePosition(QTextCursor.NextCharacter,
                                    QTextCursor.KeepAnchor, 4)
                if cursor.selectedText() == "    ":
                    cursor.removeSelectedText()
                cursor.movePosition(QTextCursor.Up)
                cursor.movePosition(QTextCursor.StartOfLine)
                lastpos = pos
                pos = cursor.position()
                if pos == lastpos:
                    break
            cursor.setPosition(start)
            cursor.movePosition(QTextCursor.NextCharacter,
                                QTextCursor.KeepAnchor, end - start)

        cursor.endEditBlock()

    def save(self):
        self.signal_save.emit()

    def isModified(self):
        return self.modified

    def firstVisibleLine(self) -> int:
        return self.firstVisibleBlock().blockNumber()

    def currentLine(self) -> int:
        return self.textCursor().blockNumber()

    def goToLine(self, line: int):
        tc = self.textCursor()
        pos = self.document().findBlockByNumber(line - 1).position()
        tc.setPosition(pos, QTextCursor.MoveAnchor)
        # self.setTextCursor(tc)

    def getSelectedText(self) -> str:
        if self.textCursor().hasSelection():
            return self.textCursor().selectedText()
        else:
            return ''

    def getSelectedRows(self) -> Tuple[int, int]:
        """
        返回选中的行号范围
        :return:
        """
        start = self.textCursor().selectionStart()
        end = self.textCursor().selectionEnd()
        start_block_id = self.document().findBlock(start).blockNumber()
        end_block_id = self.document().findBlock(end).blockNumber()

        return (start_block_id, end_block_id)

    def set_eol_status(self):
        """
        根据文件内容中的换行符设置底部状态

        :return:
        """
        eols = re.findall(r'\r\n|\r|\n', self.toPlainText())
        if not eols:
            print('\\n')
            # self.label_status_eol.setText('Unix(LF)')
            # self.textEdit.setEolMode(QsciScintilla.EolUnix)  # \n换行
            return
        grouped = [(len(list(group)), key) for key, group in groupby(sorted(eols))]
        eol = sorted(grouped, reverse=True)[0][1]
        if eol == '\r\n':
            print('\\r\\n')
            # self.label_status_eol.setText('Windows(CR LF)')
            # self.textEdit.setEolMode(QsciScintilla.EolWindows)  # \r\n换行
            # return QsciScintilla.EolWindows
        if eol == '\r':
            print('\\r')
            # self.label_status_eol.setText('Mac(CR)')
            # self.textEdit.setEolMode(QsciScintilla.EolMac)  # \r换行
            return
        # self.label_status_eol.setText('Unix(LF)')
        # self.textEdit.setEolMode(QsciScintilla.EolUnix)  # \n换行

    def load_color_scheme(self, scheme: Dict[str, str]):
        PythonHighlighter.font_cfg.load_color_scheme(scheme)

    def getCursorPosition(self) -> int:
        # QTextCursor.position()
        return self.textCursor().position()

    def setSelection(self):
        raise NotImplementedError
        text_cursor: QTextCursor = self.textCursor()
        text_cursor.clearSelection()
        # text_cursor.setPosition()

    def hasSelectedText(self):
        return self.textCursor().hasSelection()

    def replace(self, replacement: str):
        cursor: QTextCursor = self.textCursor()
        cursor.removeSelectedText()
        cursor.insertText(replacement)
        # self.textCursor().replace(replacement, self.textCursor())
        self.setTextCursor(cursor)

    def get_word(self, row=-1, col=0) -> str:
        """
        获取某个行列位置下的文本.若row=-1则获取光标之下的文本
        :return:
        """
        if row == -1:
            line_no = self.currentLine()
            text_cursor: QTextCursor = self.textCursor()
            col = text_cursor.positionInBlock()
        else:
            line_no = row
        text: str = self.document().findBlockByLineNumber(line_no).text()

        col_forward = col
        col_backward = col
        seps_set = ' \n,()[]{}\'\";:\t!+-*/\\=.'
        try:
            while 1:
                if col_forward >= 0 and text[col_forward] in seps_set:
                    break
                if col_forward > 0:
                    col_forward -= 1
                else:
                    break
            length = len(text)
            while 1:
                if col_backward < length and text[col_backward] in seps_set:
                    break
                if col_backward < length - 1:
                    col_backward += 1
                else:
                    break
            word = text[col_forward:col_backward + 1].strip(seps_set)
            return word
        except:
            import traceback
            traceback.print_exc()
            return ''

    def register_highlight(self, line: int, start: int, length: int, marker: int, hint: str):
        """
        注册高亮
        :param line: 要高亮的行号
        :param start: 从line行的哪一列开始高亮
        :param length: 高亮区域的长度
        :param marker: 使用的标记颜色等
        :param hint: 使用的提示文字
        :return:
        """
        self.highlighter.registerHighlight(line, start, length, marker, hint)

    def clear_highlight(self):
        """
        清除高亮
        :return:
        """
        self.highlighter.highlight_marks = {}

    def rehighlight(self):
        self.update_request_queue.put(self.UPDATE_CODE_HIGHLIGHT)

    def textCursor(self) -> QTextCursor:
        return super(PMBaseCodeEdit, self).textCursor()

    def dragEnterEvent(self, QDragEnterEvent):  # 3
        print('Drag Enter')
        if QDragEnterEvent.mimeData().hasText():
            QDragEnterEvent.acceptProposedAction()
            print()

    def dragMoveEvent(self, QDragMoveEvent):  # 4
        # print('Drag Move')
        pass

    def dragLeaveEvent(self, QDragLeaveEvent):  # 5
        # print('Drag Leave')
        pass

    def dropEvent(self, drop_event: QDropEvent):  # 6
        url: QUrl = None
        urls = drop_event.mimeData().urls()
        for url in urls:
            try:
                file = url.toLocalFile()
                self.signal_file_dropped.emit(file)
            except:
                import traceback
                traceback.print_exc()


# if __name__ == '__main__':
#     app = QApplication([])
#     e = AutoCompList()
#     e.show()
#
#
#     class A():
#         pass
#
#
#     c = A()
#     c.name = 'aaaaa'
#     c.type = 'module'
#     c.complete = 'aaa'
#     e.set_completions([c, c, c, c])
#     app.exec_()
