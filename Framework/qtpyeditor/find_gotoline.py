# -*- coding:utf-8 -*-
# @Time: 2021/1/20 8:23
# @Author: Zhanyi Hou
# @Email: 1295752786@qq.com
# @File: find_gotoline.py
from PySide2.QtWidgets import QDialog, QVBoxLayout, QPushButton, QHBoxLayout
from pmgwidgets import PMGPanel


class FindDialog(QDialog):
    def __init__(self, parent=None, text_edit: 'PMCodeEditor' = None):
        super(FindDialog, self).__init__(parent)
        self.text_editor = text_edit
        self.qsci_text_edit: 'QsciScintilla' = text_edit.textEdit
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
        line, index = self.text_editor.textEdit.getSelection()[:2]
        self.text_editor.search_word(forward=False, **settings, line=line, index=index)

        pass

    def replace_current(self):
        text: str = self.settings_panel.widgets_dic['text_to_replace'].get_value()
        if self.qsci_text_edit.hasSelectedText():
            self.qsci_text_edit.replace(text)

    def replace_all(self):
        settings = self.settings_panel.get_value()
        text_to_replace = self.settings_panel.widgets_dic['text_to_replace'].get_value()
        while (1):
            b = self.text_editor.search_word(forward=True, **settings)
            if b:
                self.qsci_text_edit.replace(text_to_replace)
            else:
                break

    def show(self) -> None:
        super().show()
        if self.qsci_text_edit.hasSelectedText():
            self.settings_panel.set_value({'text_to_find': self.qsci_text_edit.selectedText()})

    def closeEvent(self, a0: 'QCloseEvent') -> None:
        sel = self.qsci_text_edit.getCursorPosition()
        self.qsci_text_edit.setSelection(sel[0], sel[1], sel[0], sel[1])

    def close(self) -> bool:
        return False

# class GotoLineDialog(QDialog, Ui_DialogGoto):
#     """跳转指定行"""
#
#     def __init__(self, editor: 'PMCodeEditor', *args, **kwargs):
#         super(GotoLineDialog, self).__init__(*args, **kwargs)
#         self.setupUi(self)
#         self.editor = editor
#         self.buttonBox.accepted.connect(self.slot_accepted)
#         line, column = editor.getCursorPosition()
#         self.lineEdit.setText('%s:%s' % (line + 1, column + 1))
#         self.lineEdit.setFocus()
#         self.lineEdit.selectAll()
#
#     def slot_accepted(self):
#         """
#         跳转到对应行列
#         :return:
#         """
#         text = re.findall(r'^\d+$|^\d+:\d+$', self.lineEdit.text().strip())
#         if not text:
#             return
#         text = text[0]
#         if text.find(':') == -1:
#             text += ':0'
#         try:
#             line, column = text.split(':')
#             self.editor.setCursorPosition(max(0, int(line) - 1), max(0, int(column) - 1))
#             self.accept()
#         except Exception as e:
#             logger.warning(str(e))
