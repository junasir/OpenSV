# -*- coding:utf-8 -*-
# @Time: 2021/1/18 9:23
# @Author: Zhanyi Hou
# @Email: 1295752786@qq.com
# @File: baseeditor.py
# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
编辑器
编辑器构造参数：
{'language':'Python',
'ext_name':'.py',
'lexer':PythonLexer,
'builtin_keywords':['int','float',...],
'dynamic_keywords':['func','method',...]
}
常用功能：
1、批量缩进、批量取消缩进（语言无关）
2、整理格式（语言相关，需要对应语言进行重写）
3、在终端执行代码（语言相关：需要已知编译器或者解释器的路径。）
4、更新补全选项（语言无关）
5、复制、粘贴、剪切（语言无关）
6、批量注释、批量取消注释（未实现。注意，这部分功能比较复杂，需要该语言的注释符号）
7、查找、替换等（语言无关）
8、保存、打开（需要已知扩展名）
Created on 2020/9/7
@author: Irony
@email: 892768447@qq.com
@file: editor
@description: Code Editor
"""

__version__ = '0.1'

import logging
import os
import time
from typing import TYPE_CHECKING, List, Iterable, Dict, Set, Tuple, Any
from PySide2.QtGui import QIcon, QKeySequence, QTextDocument, QTextCursor, QTextBlock, QDropEvent
from PySide2.QtCore import QDir, QCoreApplication, Qt, QPoint, Signal, QTranslator, QLocale, QUrl
from PySide2.QtWidgets import QWidget, QMessageBox, QFileDialog, QAction, QShortcut, QDialog, QVBoxLayout, QPushButton, \
    QHBoxLayout, QApplication, QLabel

from pmgwidgets.widgets.composited import PMGPanel
from qdarkstyle import load_stylesheet_pyside2

from qtpyeditor.ui.gotoline import Ui_DialogGoto
from qtpyeditor.codeeditor.abstracteditor import PMAbstractEditor

if TYPE_CHECKING:
    from qtpyeditor.codeedit import PMBaseCodeEdit

logger = logging.getLogger(__name__)


class GotoLineDialog(QDialog, Ui_DialogGoto):
    def __init__(self, parent=None):
        super(GotoLineDialog, self).__init__(parent)
        self.current_line = -1
        self.max_row_count = 0
        self.setupUi(self)
        self.buttonBox.accepted.connect(self.run_goto)
        self.buttonBox.rejected.connect(self.reject)

    def set_max_row_count(self, length: int):
        """
        设置最大可跳转的行数
        :param length:
        :return:
        """
        self.max_row_count = length

    def set_current_line(self, line: int):
        """
        line：从0开始
        :param line:
        :return:
        """
        self.current_line = line
        self.lineEdit.setText(str(line + 1))

    def run_goto(self):
        """
        跳转到行
        :return:
        """
        text = self.lineEdit.text()
        if not text.isdecimal():
            QMessageBox.warning(self, self.tr('Input Value Error'), self.tr('Cannot convert \'%s\' to integer.') % text)
            return
        line = int(text)
        if not 0 <= line < self.max_row_count:
            QMessageBox.warning(self, self.tr('Input Value Error'),
                                self.tr('Line Number {line} out of range!').format(line=line))
            return
        self.accept()

    def get_line(self) -> int:
        return int(self.lineEdit.text())


class FindDialog(QDialog):
    def __init__(self, parent=None, text_editor: 'PMGBaseEditor' = None):
        super(FindDialog, self).__init__(parent)
        self.setStyleSheet(load_stylesheet_pyside2())
        self.text_editor = text_editor
        self.text_edit: 'PMBaseCodeEdit' = text_editor.text_edit
        views = [('line_ctrl', 'text_to_find', self.tr('Text to Find'), ''),
                 ('line_ctrl', 'text_to_replace', self.tr('Text to Replace'), ''),
                 ('check_ctrl', 'wrap', self.tr('Wrap'), True),
                 ('check_ctrl', 'regex', self.tr('Regex'), False),
                 ('check_ctrl', 'case_sensitive', self.tr('Case Sensitive'), True),
                 ('check_ctrl', 'whole_word', self.tr('Whole Word'), True),
                 ]
        self.settings_panel = PMGPanel(parent=self, views=views)
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.settings_panel)
        self.button_up = QPushButton(self.tr('Up'))
        self.button_down = QPushButton(self.tr('Down'))
        self.button_replace = QPushButton(self.tr('Replace'))
        self.button_replace_all = QPushButton(self.tr('Replace All'))

        self.button_up.clicked.connect(self.search_up)
        self.button_down.clicked.connect(self.search_down)
        self.button_replace.clicked.connect(self.replace_current)
        self.button_replace_all.clicked.connect(self.replace_all)

        self.button_bar = QHBoxLayout()
        self.button_bar.addWidget(self.button_up)
        self.button_bar.addWidget(self.button_down)
        self.button_bar.addWidget(self.button_replace)
        self.button_bar.addWidget(self.button_replace_all)
        self.button_bar.setContentsMargins(0, 0, 0, 0)
        self.layout().addLayout(self.button_bar)

    def search_up(self):
        settings = self.settings_panel.get_value()
        self.text_editor.search_word(forward=True, **settings)

        pass

    def search_down(self):
        """
        反方向查找。注意，简单的设置qsci的forward=False是不够的，还需要对位置进行处理。
        这似乎是QSciScintilla的bug.
        """
        settings = self.settings_panel.get_value()
        self.text_editor.search_word(forward=False, **settings)

        pass

    def replace_current(self):
        text: str = self.settings_panel.widgets_dic['text_to_replace'].get_value()
        if self.text_edit.hasSelectedText():
            self.text_edit.replace(text)
            self.search_up()

    def replace_all(self):
        settings = self.settings_panel.get_value()
        text_to_replace = self.settings_panel.widgets_dic['text_to_replace'].get_value()
        while (1):
            b = self.text_editor.search_word(forward=True, **settings)
            if b:
                self.text_edit.replace(text_to_replace)

            else:
                break

    def show(self) -> None:
        super().show()
        if self.text_edit.getSelectedText() != '':
            self.settings_panel.set_value({'text_to_find': self.text_edit.getSelectedText()})

    def show_replace_actions(self, replace_on: bool = False):
        self.settings_panel.get_ctrl('text_to_replace').setVisible(replace_on)
        self.button_replace.setVisible(replace_on)
        self.button_replace_all.setVisible(replace_on)

    def closeEvent(self, a0: 'QCloseEvent') -> None:
        pass
        # sel = self.text_edit.getCursorPosition()
        # self.text_edit.setSelection(sel[0], sel[1], sel[0], sel[1])

    def close(self) -> bool:
        return False


class PMGBaseEditor(PMAbstractEditor):
    signal_focused_in: Signal = None
    signal_new_requested: Signal = Signal(str, int)  # 文件路径；文件的打开模式（目前都是0）
    signal_save_requested: Signal = Signal()
    signal_request_find_in_path: Signal = Signal(str)

    def __init__(self, parent):
        app = QApplication.instance()
        trans_editor_tb = QTranslator()
        app.trans_editor_tb = trans_editor_tb
        trans_editor_tb.load('/JuResource/translations', 'qt_%s.qm' % QLocale.system().name())
        app.installTranslator(trans_editor_tb)

        super().__init__(parent)
        self.find_dialog: 'FindDialog' = None
        self.goto_line_dialog: 'GotoLineDialog' = None
        self.last_save_time = 0
        self._path = ''
        self._modified = False
        self.text_edit: 'PMBaseCodeEdit' = None
        self._extension_names: List[str] = []  # 该编辑器支持的文件名
        self._indicator_dict: Dict[str, str] = {}

        self.line_number_area = QWidget()
        self.line_number_area.setMaximumHeight(60)
        self.line_number_area.setMinimumHeight(20)
        # self.line_number_area.setContentsMargins(0, 0, 0, 0)
        self.status_label = QLabel()
        self.status_label.setStyleSheet("""color:#BBBBBB""")
        line_number_area_layout = QHBoxLayout()
        line_number_area_layout.addWidget(self.status_label)
        line_number_area_layout.setContentsMargins(0, 0, 0, 0)
        self.line_number_area.setLayout(line_number_area_layout)
        self.modified_status_label = QLabel()
        self.modified_status_label.setText('')
        line_number_area_layout.addWidget(self.modified_status_label)

    def set_edit(self, edit: 'PMBaseCodeEdit'):
        self.text_edit = edit
        self.signal_focused_in = self.text_edit.signal_focused_in
        self.text_edit.signal_save.connect(self.save)
        self.text_edit.signal_text_modified.connect(lambda: self.slot_modification_changed(True))
        self.text_edit.cursorPositionChanged.connect(self.show_cursor_pos)
        self.text_edit.signal_file_dropped.connect(lambda name: self.signal_new_requested.emit(name, 0))
        self.find_dialog = FindDialog(parent=self, text_editor=self)
        self.goto_line_dialog = GotoLineDialog(parent=self)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        self.layout().addWidget(self.text_edit)
        self.layout().addWidget(self.status_label)
        # self.layout().setContentsMargins(0, 0, 0, 0)

    def layout(self) -> QVBoxLayout:
        return super(PMGBaseEditor, self).layout()

    def show_cursor_pos(self):
        row = self.text_edit.textCursor().block().blockNumber()
        col = self.text_edit.textCursor().columnNumber()
        self.status_label.setText(
            '行：{row},列:{col}'.format(row=row + 1, col=col + 1))

    def set_shortcut(self):
        pass

    def update_settings(self, settings: Dict[str, Any]):
        pass

    def slot_text_edit_focusedin(self, e):
        pass

    def goto_line(self, line_no: int):
        """
        跳转到对应行列
        :return:
        """
        doc: QTextDocument = self.text_edit.document()
        lines = doc.blockCount()
        assert 1 <= line_no <= lines
        pos = doc.findBlockByLineNumber(line_no - 1).position()
        text_cursor: QTextCursor = self.text_edit.textCursor()
        text_cursor.setPosition(pos)
        self.text_edit.setTextCursor(text_cursor)

    def _init_lexer(self, lexer: 'QsciLexer') -> None:
        """
        初始化语法解析器

        :return: None
        """
        pass

    def search_word(self, text_to_find: str, wrap: bool, regex: bool, case_sensitive: bool, whole_word: bool,
                    forward: bool, index=-1, line=-1, **kwargs) -> bool:
        find_flags = 0
        # if wrap:
        #     find_flags = find_flags | QTextDocument.FindFlags
        if case_sensitive:
            find_flags = find_flags | QTextDocument.FindCaseSensitively
        if whole_word:
            find_flags = find_flags | QTextDocument.FindWholeWords
        if not forward:
            find_flags = find_flags | QTextDocument.FindBackward
        if find_flags == 0:
            find_flags = QTextDocument.FindFlags
        # print(find_flags)
        ret = self.text_edit.find(text_to_find, options=find_flags)
        cursor_pos = self.text_edit.getCursorPosition()
        print(ret, wrap)
        if wrap and (not ret):
            cursor = self.text_edit.textCursor()
            cursor.clearSelection()
            if forward:
                cursor.movePosition(QTextCursor.Start)
                print('cursor to start!')

            else:
                cursor.movePosition(QTextCursor.End)
            self.text_edit.setTextCursor(cursor)
            ret = self.text_edit.find(text_to_find, options=find_flags)
            # print(ret,cursor)
            if not ret:
                cursor = self.text_edit.textCursor()
                cursor.setPosition(cursor_pos)
                self.text_edit.setTextCursor(cursor)
        return ret

    def autocomp(self):
        pass

    def get_word_under_cursor(self):
        pass

    def set_text(self, text: str) -> None:
        """
        设置编辑器内容

        :type text: str
        :param text: 文本内容
        :return: None
        """
        self.text_edit.setPlainText(text)

    def set_modified(self, modified: bool) -> None:
        """
        设置内容是否被修改

        :param modified: 是否被修改 True or False
        :type: bool
        :return: None
        """
        self._modified = modified
        self.text_edit.modified = modified
        self.slot_modification_changed(modified)

    def load_file(self, path: str) -> None:
        """
        加载文件

        :param path: 文件路径
        :type path: str
        :return: None
        """
        from qtpyeditor.Utilities import decode
        self._path = ''
        try:
            # 读取文件内容并加载
            with open(path, 'rb') as fp:
                text = fp.read()
                text, coding = decode(text)
                self.set_encoding(coding)
                self.set_text(text)
                self.set_modified(False)
                self.text_edit.set_eol_status()
        except Exception as e:
            import traceback
            traceback.print_exc()
            logger.warning(str(e))

        self._path = path
        self.setWindowTitle(self.filename())
        self.last_save_time = time.time()
        self.set_modified(False)

    def set_encoding(self, encoding: str):
        """
        设置文本编码，仅支持 ASCII 和 UTF-8

        :param encoding: ascii or gbk or utf-8
        :type: str
        :return:
        """

    def slot_about_close(self, save_all=False) -> QMessageBox.StandardButton:
        """
        是否需要关闭以及保存

        :param save_all: 当整个窗口关闭时增加是否全部关闭
        :return:QMessageBox.StandardButton
        """
        # QCoreApplication.translate = QCoreApplication.translate
        if not self._modified:
            return QMessageBox.Discard

        buttons = QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
        if save_all:
            buttons |= QMessageBox.SaveAll  # 保存全部
            buttons |= QMessageBox.NoToAll  # 放弃所有
        ret = QMessageBox.question(self, QCoreApplication.translate('PMGBaseEditor', 'Save'),
                                   QCoreApplication.translate('PMGBaseEditor', 'Save file "{0}"?').format(
                                       self.filename()), buttons,
                                   QMessageBox.Save)
        if ret == QMessageBox.Save or ret == QMessageBox.SaveAll:
            if not self.save():
                return QMessageBox.Cancel
        return ret

    def slot_modification_changed(self, modified: bool) -> None:
        """
        内容被修改槽函数

        :param modified: 是否被修改
        :type modified: bool
        :return:
        """
        title = self.windowTitle()
        if modified:
            if not title.startswith('*'):
                self.setWindowTitle('*' + title)
        else:
            if title.startswith('*'):
                self.setWindowTitle(title[1:])

    def slot_save(self) -> None:
        """
        保存时触发的事件。
        :return:
        """
        self.save()
        self.set_modified(False)

    def slot_text_changed(self) -> None:
        pass

    def is_temp_file(self) -> bool:
        """
        返回文件是否为临时文件
        :return:
        """
        tmp_path = QDir.tempPath().replace('\\', '/')
        if self._path.replace('\\', '/').startswith(tmp_path):
            return True
        else:
            return False

    def save(self) -> bool:
        """
        The method call when saving files.
        If the file is not saved yet, the qfiledialog will open save dialog at default_dir,generated by get_default_dir method.
        :return:
        """
        QCoreApplication.translate = QCoreApplication.translate
        path = self._path.replace(os.sep, '/')
        default_dir = self.default_save_path()
        if path.startswith(QDir.tempPath().replace(os.sep, '/')):
            assert os.path.exists(default_dir) or default_dir == ''
            # 弹出对话框要求选择真实路径保存
            path, ext = QFileDialog.getSaveFileName(self, QCoreApplication.translate("PMGBaseEditor", 'Save file'),
                                                    default_dir,
                                                    filter='*.py')

            if not path:
                return False
            if not path.endswith('.py'):
                path += '.py'
            self._path = path
        try:
            with open(self._path, 'wb') as fp:
                fp.write(self.text().encode('utf-8', errors='ignore'))

            self.setWindowTitle(os.path.basename(path))
            self.set_modified(False)
            self.last_save_time = time.time()
            return True
        except Exception as e:
            # 保存失败
            logger.warning(str(e))
        return False

    def modified(self) -> bool:
        """
        返回内容是否被修改

        :rtype: bool
        :return: 返回内容是否被修改
        """
        return self._modified

    def filename(self) -> str:
        """
        返回当前文件名

        :rtype: str
        :return: 返回当前文件名
        """
        return os.path.basename(self._path)

    def path(self) -> str:
        """
        返回当前文件路径

        :rtype: str
        :return: 返回当前文件路径
        """
        return self._path

    def set_path(self, path: str) -> None:
        """
        设置文件路径

        :param path: 设置文件路径
        :type path: str
        :return: None
        """
        self._path = path

        title = self.windowTitle()
        new_title = os.path.basename(self._path)
        if title.startswith('*'):
            self.setWindowTitle('*' + new_title)
        else:
            self.setWindowTitle(new_title)

    def text(self, selected: bool = False) -> str:
        """
        返回编辑器选中或者全部内容
        Args:
            selected:

        Returns:

        """
        if not selected:
            return self.text_edit.toPlainText()
        else:
            pass

    def slot_file_modified_externally(self):
        return

    def _init_actions(self) -> None:
        """
        初始化额外菜单项

        :return:
        """
        # QCoreApplication.translate = QCoreApplication.translate
        self.icon_path = "/JuResource/"   # 图标文件路径
        # self.icon_path = os.path.dirname(os.path.dirname(__file__))  # 图标文件路径
        # self._action_format = QAction(QIcon(os.path.join(self.icon_path, 'icons/format.svg')),
        #                               QCoreApplication.translate("PMGBaseEditor", 'Format Code'),
        #                               self.text_edit)
        self._action_run_code = QAction(QIcon('/JuResource/icons/run.svg'),
                                        QCoreApplication.translate("PMGBaseEditor", 'Run Code'),
                                        self.text_edit)
        # self._action_run_sel_code = QAction(QIcon(os.path.join(self.icon_path, 'icons/python.svg')),
        #                                     QCoreApplication.translate("PMGBaseEditor", 'Run Selected Code'),
        #                                     self.text_edit)
        self._action_save = QAction(QIcon('/JuResource/icons/save.svg'),
                                    QCoreApplication.translate("PMGBaseEditor", 'Save'),
                                    self.text_edit)
        self._action_find = QAction(QCoreApplication.translate("PMGBaseEditor", 'Find'), self.text_edit)
        self._action_replace = QAction(QCoreApplication.translate("PMGBaseEditor", 'Replace'), self.text_edit)

        self._action_find_in_path = QAction(QCoreApplication.translate('PMGBaseEditor', 'Find In Path'), self.text_edit)
        self._action_autocomp = QAction(QCoreApplication.translate("PMGBaseEditor", 'AutoComp'), self.text_edit)

        # 设置快捷键
        # self._shortcut_format = QShortcut(QKeySequence('Ctrl+Alt+F'), self.text_edit, context=Qt.WidgetShortcut)
        # self._action_format.setShortcut(QKeySequence('Ctrl+Alt+F'))

        self._shortcut_autocomp = QShortcut(QKeySequence('Ctrl+P'), self.text_edit, context=Qt.WidgetShortcut)
        self._action_autocomp.setShortcut(QKeySequence("Ctrl+P"))

        self._shortcut_run = QShortcut(QKeySequence('F9'), self.text_edit, context=Qt.WidgetShortcut)
        self._action_run_code.setShortcut(QKeySequence('F9'))

        # self._shortcut_run_sel = QShortcut(QKeySequence('F9'), self.text_edit, context=Qt.WidgetShortcut)
        # self._action_run_sel_code.setShortcut(QKeySequence('F9'))

        self._action_save.setShortcut(QKeySequence('Ctrl+S'))
        self._shortcut_save = QShortcut(QKeySequence('Ctrl+S'), self.text_edit, context=Qt.WidgetShortcut)

        self._action_find.setShortcut(QKeySequence('Ctrl+F'))
        self._shortcut_find = QShortcut(QKeySequence('Ctrl+F'), self.text_edit, context=Qt.WidgetShortcut)

        self._action_replace.setShortcut(QKeySequence('Ctrl+H'))
        self._shortcut_replace = QShortcut(QKeySequence('Ctrl+H'), self.text_edit, context=Qt.WidgetShortcut)

        self._action_find_in_path.setShortcut(QKeySequence('Ctrl+Shift+F'))
        self._shortcut_find_in_path = QShortcut(QKeySequence('Ctrl+Shift+F'), self.text_edit, context=Qt.WidgetShortcut)

        self._shortcut_goto = QShortcut(QKeySequence('Ctrl+G'), self.text_edit, context=Qt.WidgetShortcut)

        # self._action_add_breakpoint = QAction(QIcon(os.path.join(self.icon_path, 'icons/breakpoint.svg')),
        #                                       QCoreApplication.translate("PMGBaseEditor", 'Add Breakpoint'),
        #                                       self.text_edit)
        # self._action_remove_breakpoint = QAction(QCoreApplication.translate("PMGBaseEditor", 'Remove Breakpoint'),
        #                                          self.text_edit)
        #
        # self._action_view_breakpoints = QAction(QCoreApplication.translate("PMGBaseEditor", 'View BreakPoints'),
        #                                         self.text_edit)

    def _init_signals(self):
        """
        初始化信号绑定

        :return: None
        """

        # 绑定获得焦点信号
        self.text_edit.signal_focused_in.connect(self.slot_text_edit_focusedin)
        # 绑定光标变化信号
        self.text_edit.cursorPositionChanged.connect(self.slot_cursor_position_changed)
        # 绑定内容改变信号
        self.text_edit.textChanged.connect(self.slot_text_changed)
        # 绑定选中变化信号
        self.text_edit.selectionChanged.connect(self.slot_selection_changed)
        # 绑定是否被修改信号
        # self.text_edit.signal_modification)_Changed.connect(self.slot_modification_changed)
        # 绑定右键菜单信号
        self.text_edit.customContextMenuRequested.connect(self.slot_custom_context_menu_requested)
        # 绑定快捷键信号
        # self._action_format.triggered.connect(self.slot_code_format)
        # self._shortcut_format.activated.connect(self.slot_code_format)
        self._action_run_code.triggered.connect(self.slot_code_run)
        self._shortcut_run.activated.connect(self.slot_code_run)
        # self._action_run_sel_code.triggered.connect(self.slot_code_sel_run)
        # self._shortcut_run_sel.activated.connect(self.slot_code_sel_run)

        self._shortcut_save.activated.connect(self.slot_save)
        self._action_save.triggered.connect(self.slot_save)

        self._action_find.triggered.connect(self.slot_find)
        self._action_replace.triggered.connect(self.slot_replace)

        self._shortcut_find.activated.connect(self.slot_find)
        self._shortcut_replace.activated.connect(self.slot_replace)

        self._action_find_in_path.triggered.connect(self.slot_find_in_path)
        self._shortcut_find_in_path.activated.connect(self.slot_find_in_path)

        self._action_autocomp.triggered.connect(self.autocomp)
        self._shortcut_autocomp.activated.connect(self.autocomp)

        self._shortcut_goto.activated.connect(self.slot_goto_line)

        # self._action_add_breakpoint.triggered.connect(self.slot_add_breakpoint_triggered)
        # self._action_remove_breakpoint.triggered.connect(self.slot_remove_breakpoint_triggered)

        # self._action_view_breakpoints.triggered.connect(self.view_break_points)

    def slot_cursor_position_changed(self):
        pass

    def slot_selection_changed(self) -> None:
        """
        选中内容变化槽函数

        :return: None
        """

    def create_context_menu(self) -> 'QMenu':
        """
        创建上下文菜单。
        :return:
        """
        menu = self.text_edit.createStandardContextMenu()

        # 遍历本身已有的菜单项做翻译处理
        # 前提是要加载了Qt自带的翻译文件
        for action in menu.actions():
            action.setText(QCoreApplication.translate('QTextControl', action.text()))
        # 添加额外菜单
        menu.addSeparator()
        # menu.addAction(self._action_format)
        # menu.addAction(self._action_run_code)
        # menu.addAction(self._action_run_sel_code)
        menu.addAction(self._action_save)
        menu.addAction(self._action_find)
        menu.addAction(self._action_replace)
        # menu.addAction(self._action_find_in_path)
        # menu.addAction(self._action_add_breakpoint)
        # menu.addAction(self._action_remove_breakpoint)
        # menu.addAction(self._action_view_breakpoints)
        # menu.addAction(self)
        return menu

    def slot_custom_context_menu_requested(self, pos: QPoint) -> None:
        """
        右键菜单修改

        :param pos:
        :type pos: QPoint
        :return: None
        """
        menu = self.create_context_menu()
        # 根据条件决定菜单是否可用
        enabled = len(self.text().strip()) > 0
        # self._action_format.setEnabled(enabled)
        self._action_run_code.setEnabled(enabled)
        # self._action_run_sel_code.setEnabled(self.textEdit.hasSelectedText())
        # self._action_run_sel_code.setEnabled(enabled)
        menu.exec_(self.text_edit.mapToGlobal(pos))
        del menu

    def slot_find_in_path(self):
        sel = self.text_edit.getSelectedText()
        self.signal_request_find_in_path.emit(sel)

    def slot_find(self):
        self.find_dialog.show_replace_actions(replace_on=False)
        self.find_dialog.show()

    def slot_replace(self):
        self.find_dialog.show_replace_actions(replace_on=True)
        self.find_dialog.show()

    def slot_goto_line(self):
        self.goto_line_dialog.set_current_line(self.text_edit.textCursor().blockNumber())
        self.goto_line_dialog.set_max_row_count(self.text_edit.blockCount())
        ret = self.goto_line_dialog.exec_()
        if ret:
            self.goto_line(self.goto_line_dialog.get_line())

    def set_indicators(self, msg, clear=True):
        """
        qtextedit 的indicators ,但是目前还不支持。
        :return:
        """
        pass

    def change_color_scheme(self, color_scheme_name: str):
        if color_scheme_name == 'dark':
            self.text_edit.load_color_scheme({'keyword': '#b7602f'})
        elif color_scheme_name == 'light':
            self.text_edit.load_color_scheme({'keyword': '#101e96'})
        else:
            raise ValueError('unrecognized input color scheme name %s' % color_scheme_name)
