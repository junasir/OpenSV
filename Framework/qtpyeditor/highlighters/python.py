# -*- coding:utf-8 -*-
# @Time: 2021/1/18 8:53
# @Author: Zhanyi Hou
# @Email: 1295752786@qq.com
# @File: python.py
import sys
import time
from typing import Dict, Tuple, List, Set

from PySide2.QtCore import QRegExp, Qt
from PySide2.QtWidgets import QApplication
from PySide2.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont, QCursor, QBrush, QTextBlock

color_scheme_intellij = {'keyword': '#101e96'}
color_scheme_dark = {'keyword': '#b7602f'}


class FontConfig():
    def __init__(self):
        """
        color是16位标准的。
        bold有以下几种选择。
        QFont::Thin	0	0
        QFont::ExtraLight	12	12
        QFont::Light	25	25
        QFont::Normal	50	50
        QFont::Medium	57	57
        QFont::DemiBold	63	63
        QFont::Bold	75	75
        QFont::ExtraBold	81	81
        QFont::Black
        """
        self.font_size = 13
        # self.settings = {'normal': {'color': "#ffffff", 'bold': QFont.Normal},
        #                  'keyword': {'color': "#CC7832", 'bold': QFont.ExtraBold},
        #                  'builtin': {'color': "#8787B0", 'bold': QFont.Normal},
        #                  'constant': {'color': "#CC7832", 'bold': QFont.Normal},
        #                  'decorator': {'color': Qt.darkBlue, 'bold': QFont.Normal},
        #                  'comment': {'color': "#808080", 'bold': QFont.Normal},
        #                  'string': {'color': "#558658", 'bold': QFont.Normal},
        #                  'number': {'color': "#6897BB", 'bold': QFont.Normal},
        #                  'error': {'color': Qt.darkRed, 'bold': QFont.Normal},
        #                  'pyqt': {'color': "#2B2B2B", 'bold': QFont.Normal},
        #                  'class': {'color': "#94558D", 'bold': QFont.Normal}
        #                  }
        self.settings = {'normal': {'color': "#abb2bf", 'bold': QFont.Bold},
                         'keyword': {'color': "#c678dd", 'bold': QFont.ExtraBold},
                         'builtin': {'color': "#8787B0", 'bold': QFont.Bold},
                         'constant': {'color': "#d19a5e", 'bold': QFont.Bold},
                         'decorator': {'color': Qt.darkBlue, 'bold': QFont.Bold},
                         'comment': {'color': "#777777", 'bold': QFont.Bold},
                         'string': {'color': "#98c379", 'bold': QFont.Bold},
                         'number': {'color': "#6897BB", 'bold': QFont.Bold},
                         'error': {'color': Qt.darkRed, 'bold': QFont.Bold},
                         'pyqt': {'color': "#2B2B2B", 'bold': QFont.Bold},
                         'class': {'color': "#C68F55", 'bold': QFont.Bold},
                         'kuo': {'color': "#c678dd", 'bold': QFont.Bold},
                         }
        # self.load_color_scheme(color_scheme_intellij)

    def load_color_scheme(self, scheme: Dict[str, str]):
        for name in scheme:
            assert name in self.settings.keys()
            self.set_font_color(name, scheme[name])

    def set_font_color(self, font_name: str, font_color: str):
        assert font_name in self.settings.keys()
        self.settings[font_name]['color'] = font_color

    def get_font_color(self, font_name: str):
        return self.settings[font_name]['color']

    def get_font_bold(self, font_name: str):
        return self.settings[font_name]['bold']

    def get_font_size(self) -> int:
        return self.font_size


class BaseHighlighter(QSyntaxHighlighter):
    ERROR = 1
    WARNING = 2
    HINT = 3
    DEHIGHLIGHT = 4

    HIGHLIGHT_COLOR = {ERROR: QColor(255, 65, 65, 200), WARNING: QColor(255, 255, 65, 100),
                       HINT: QColor(155, 155, 155, 100), DEHIGHLIGHT: QColor(155, 155, 155, 100)}


class PythonHighlighter(BaseHighlighter):
    Rules = []
    Formats = {}
    font_cfg = FontConfig()

    # _normal_font_cfg = FontConfig('#000000', QFont.Normal)  # 含义分别为颜色和大小
    # _keyword_font_cfg = FontConfig('#000000', QFont.Bold]  # 含义分别为颜色和大小
    # _builtins_font_cfg = ['#000000', QFont.Normal]
    # _constant_font_cfg = ['#000000',QFont.Normal]
    # _comment_font_cfg = ['#000000',QFont.Normal]

    def __init__(self, parent=None):
        super(PythonHighlighter, self).__init__(parent)

        self.counter = time.time()
        self.initializeFormats()
        self._rehighlight_hint = True
        self._rehighlight_syntax = True
        self.KEYWORDS = ["and", "as", "assert", 'async', 'await', "break", "class",
                         "continue", "def", "del", "elif", "else", "except",
                         "exec", "finally", "for", "from", "global", "if",
                         "import", "in", "is", "lambda", "not", "or", "pass",
                         "raise", "return", "try", "while", "with", "yield"]
        BUILTINS = ["abs", "all", "any", "basestring", "bool",
                    "callable", "chr", "classmethod", "cmp", "compile",
                    "complex", "delattr", "dict", "dir", "divmod",
                    "enumerate", "eval", "execfile", "exit", "file",
                    "filter", "float", "frozenset", "getattr", "globals",
                    "hasattr", "hex", "name", "int", "isinstance",
                    "issubclass", "iter", "len", "list", "locals", "map",
                    "max", "min", "object", "oct", "open", "ord", "pow",
                    "property", "range", "reduce", "repr", "reversed",
                    "round", "set", "setattr", "slice", "sorted",
                    "staticmethod", "str", "sum", "super", "tuple", "type",
                    "vars", "zip"]
        CONSTANTS = ["False", "True", "None", "NotImplemented",
                     "Ellipsis"]

        PythonHighlighter.Rules.append((QRegExp(
            "|".join([r"\b%s\b" % keyword for keyword in self.KEYWORDS])),
                                        "keyword"))
        PythonHighlighter.Rules.append((QRegExp(
            "|".join([r"\b%s\b" % builtin for builtin in BUILTINS])),
                                        "builtin"))
        PythonHighlighter.Rules.append((QRegExp(
            "|".join([r"\b%s\b" % constant
                      for constant in CONSTANTS])), "constant"))
        PythonHighlighter.Rules.append((QRegExp(
            r"\b[+-]?[0-9]+[lL]?\b"
            r"|\b[+-]?0[xX][0-9A-Fa-f]+[lL]?\b"
            r"|\b[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\b"),
                                        "number"))
        PythonHighlighter.Rules.append((QRegExp(
            r"self"),
                                        "class"))
        # PythonHighlighter.Rules.append((QRegExp(
        #     r"self123"),
        #                                 "kuo"))
        # PythonHighlighter.Rules.append((QRegExp(
        #     r"\bPyQt4\b|\bQt?[A-Z][a-z]\w+\b"), "pyqt"))
        PythonHighlighter.Rules.append((QRegExp(r"\b@\w+\b"),
                                        "decorator"))
        stringRe = QRegExp(r"""(?:'[^']*'|"[^"]*")""")
        stringRe.setMinimal(True)
        PythonHighlighter.Rules.append((stringRe, "string"))
        self.stringRe = QRegExp(r"""(:?"["]".*"["]"|'''.*''')""")
        self.stringRe.setMinimal(True)
        PythonHighlighter.Rules.append((self.stringRe, "string"))
        self.tripleSingleRe = QRegExp(r"""'''(?!")""")
        self.tripleDoubleRe = QRegExp(r'''"""(?!')''')

        self.matched_format = QTextCharFormat()  # 定义高亮格式
        brush = QBrush(Qt.yellow, Qt.SolidPattern)
        self.matched_format.setBackground(brush)

        self.highlight_marks: Dict[int, List[Set[int, int, int, str]]] = {}  # Dict[行号，Tuple[Set[起始，长度，类型,提示内容]]]

    # @staticmethod
    def initializeFormats(self):
        baseFormat = QTextCharFormat()
        baseFormat.setFontFamily("Consolas")
        font_cfg = self.font_cfg
        baseFormat.setFontPointSize(font_cfg.get_font_size())
        for name in ("normal", "keyword", "builtin", "constant", "decorator", "comment",
                     "string", "number", "error", "pyqt", "class", "kuo"):
            color = font_cfg.get_font_color(name)
            format = QTextCharFormat(baseFormat)
            format.setForeground(QColor(color))
            format.setFontWeight(font_cfg.get_font_bold(name))
            if name == "comment":
                format.setFontItalic(False)
            PythonHighlighter.Formats[name] = format

    def highlightBlock(self, text):

        format = QTextCharFormat()
        self.setFormat(0, len(text), format)
        if self._rehighlight_syntax:
            NORMAL, TRIPLESINGLE, TRIPLEDOUBLE, ERROR = range(4)
            # print(text[0])
            textLength = len(text)
            # print(textLength)
            prevState = self.previousBlockState()
            self.setFormat(0, textLength,
                           PythonHighlighter.Formats["normal"])

            if text.startswith("Traceback") or text.startswith("Error: "):
                self.setCurrentBlockState(ERROR)
                self.setFormat(0, textLength,
                               PythonHighlighter.Formats["error"])
                return
            if (prevState == ERROR and not (text.startswith(sys.ps1) or text.startswith("#"))):
                self.setCurrentBlockState(ERROR)
                self.setFormat(0, textLength,
                               PythonHighlighter.Formats["error"])
                return
            for regex, format in PythonHighlighter.Rules:
                # print(format)
                # print(regex)
                i = regex.indexIn(text)
                # print(i)
                while i >= 0:
                    length = regex.matchedLength()
                    # print('length', length)
                    self.setFormat(i, length,
                                   PythonHighlighter.Formats[format])
                    i = regex.indexIn(text, i + length)

            # Slow but good quality highlighting for comments. For more
            # speed, comment this out and add the following to __init__:
            # PythonHighlighter.Rules.append((QRegExp(r"#.*"), "comment"))
            if not text:
                pass
            elif text[0] == "#":
                self.setFormat(0, len(text), PythonHighlighter.Formats["comment"])
            elif text[0:5] == 'class':
                index_1 = text.index('(')

                # print(text.index('('))
                self.setFormat(6, index_1 - 6, PythonHighlighter.Formats["class"])
                # print('======')
            else:
                stack = []
                for i, c in enumerate(text):
                    if c in ('"', "'"):
                        if stack and stack[-1] == c:
                            stack.pop()
                        else:
                            stack.append(c)
                    elif c == "#" and len(stack) == 0:
                        self.setFormat(i, len(text), PythonHighlighter.Formats["comment"])
                        break
            # if "(" in text:
            #     # print(222)
            #     # print('===', PythonHighlighter.Formats["kuo"])
            #     try:
            #         index_1 = text.index('(')
            #         index_2 = text.index(')')
            #     except Exception:
            #         pass
                # self.setFormat(index_1, index_1 + 1, PythonHighlighter.Formats["class"])
                # self.setFormat(index_2, index_2 + 1, PythonHighlighter.Formats["class"])
            # class
            #     index_1 = text.index('(')
            #     # print('===', PythonHighlighter.Formats["kuo"])
            #     self.setFormat(index_1, index_1 + 1, PythonHighlighter.Formats["kuo"])
            self.setCurrentBlockState(NORMAL)

            if self.stringRe.indexIn(text) != -1:
                return
            # This is fooled by triple quotes inside single quoted strings
            for i, state in ((self.tripleSingleRe.indexIn(text), TRIPLESINGLE),
                             (self.tripleDoubleRe.indexIn(text), TRIPLEDOUBLE)):
                if self.previousBlockState() == state:
                    if i == -1:
                        i = len(text)
                        self.setCurrentBlockState(state)
                    self.setFormat(0, i + 3, PythonHighlighter.Formats["string"])
                elif i > -1:
                    self.setCurrentBlockState(state)
                    self.setFormat(i, len(text), PythonHighlighter.Formats["string"])
        if self._rehighlight_hint:
            block_number = self.currentBlock().blockNumber()
            t0 = time.time()
            if block_number in self.highlight_marks.keys():
                marks_set = self.highlight_marks[block_number]
                for mark in marks_set:
                    highlight_marker = mark[2]
                    start_col = mark[0]
                    color = self.HIGHLIGHT_COLOR[highlight_marker]
                    if mark[1] != -1:
                        to_col = mark[0] + mark[1]
                    else:
                        to_col = len(text)

                    if 0 < highlight_marker <= 3:
                        brush = QBrush(color, Qt.SolidPattern)
                        for i in range(start_col, to_col):
                            format = self.format(i)
                            format.setBackground(brush)
                            self.setFormat(i, 1, format)
                    elif highlight_marker == self.DEHIGHLIGHT:
                        for i in range(start_col, to_col):
                            format = self.format(i)
                            format.setForeground(self.HIGHLIGHT_COLOR[highlight_marker])
                            self.setFormat(i, 1, format)
                    else:
                        raise ValueError
        t1 = time.time()
        self.counter += t1 - t0

    def rehighlight(self):
        t0 = time.time()
        self.counter = 0
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        QSyntaxHighlighter.rehighlight(self)
        QApplication.restoreOverrideCursor()
        t1 = time.time()
        print(t1 - t0, 'time.time,elapsed for rendering code', self.counter)

    def registerHighlight(self, line_no: int, start: int, length: int, marker: int, hint: str):
        """
        内置的集合数据结构支持整体去重。
        :param line_no:
        :param start:
        :param length:
        :param marker:
        :return:
        """
        if not isinstance(self.highlight_marks.get(line_no), list):
            self.highlight_marks[line_no] = set()
        self.highlight_marks[line_no].add((start, length, marker, hint))
        # print(start, length)
        # print(self.highlight_marks)
