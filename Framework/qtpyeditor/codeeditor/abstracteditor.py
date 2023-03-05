# -*- coding:utf-8 -*-
# @Time: 2021/2/6 10:29
# @Author: Zhanyi Hou
# @Email: 1295752786@qq.com
# @File: abstracteditor.py
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

import os
from typing import TYPE_CHECKING, List, Iterable, Dict, Set, Tuple, Any

from PySide2.QtWidgets import QWidget, QMessageBox


class PMAbstractEditor(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.last_save_time = 0
        self.extension_lib = None

    def set_shortcut(self):
        pass

    def update_settings(self, settings: Dict[str, Any]):
        pass

    def slot_textedit_focusedin(self, e):
        pass

    def goto_line(self, line_no: int):
        """
        跳转到对应行列
        :return:
        """
        pass

    def _init_lexer(self, lexer: 'QsciLexer') -> None:
        """
        初始化语法解析器

        :return: None
        """
        pass

    def _init_signals(self) -> None:
        """
        初始化信号绑定

        :return: None
        """
        pass

    def _init_actions(self) -> None:
        """
        初始化额外菜单项

        :return:
        """
        pass

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
        pass

    def set_modified(self, modified: bool) -> None:
        """
        设置内容是否被修改

        :param modified: 是否被修改 True or False
        :type: bool
        :return: None
        """
        pass

    def load_file(self, path: str) -> None:
        """
        加载文件

        :param path: 文件路径
        :type path: str
        :return: None
        """
        pass

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
        if not self.modified():
            return QMessageBox.Discard
        buttons = QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
        if save_all:
            buttons |= QMessageBox.SaveAll  # 保存全部
            buttons |= QMessageBox.NoToAll  # 放弃所有
        ret = QMessageBox.question(self, self.tr('Save'), self.tr('Save file "{0}"?').format(self.filename()), buttons,
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

    def default_save_path(self) -> str:
        """
        获取当前默认存储为的路径
         Default directory.
        :return:
        """
        return ''

    def slot_text_changed(self) -> None:
        pass

    def save(self) -> bool:
        """
        保存文件时调用的方法
        :return:
        """

    def modified(self) -> bool:
        """
        返回内容是否被修改

        :rtype: bool
        :return: 返回内容是否被修改
        """
        return self.textEdit.isModified()

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
        return ''

    def slot_file_modified_externally(self):
        return

    def change_color_scheme(self, color_scheme_name: str):
        pass

    def slot_code_format(self):
        pass

    def slot_code_run(self):
        pass

    def slot_code_sel_run(self):
        pass
