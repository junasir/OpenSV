#!/usr/bin/env python3
# cython: language_level=3
# -*- coding: utf-8 -*-

r"""
"""

__author__ = "Jiang Jun"

from logging import (Handler, FileHandler, StreamHandler, DEBUG, INFO, WARNING, ERROR, CRITICAL, getLogger, Formatter,
                     handlers)
from os import path, makedirs, listdir, remove
from time import strftime, localtime
from PySide2.QtCore import QObject, Signal
from ju_cfg import JuConfig


class JuLogger(QObject):
    level_relations = {
        'debug': DEBUG, 'info': INFO, 'warning': WARNING,
        'error': ERROR, 'critical': CRITICAL
    }
    register_log_signal = Signal(str)

    def __init__(self, filename='{date}.log'.format(date=strftime("%Y-%m-%d_%H_%M_%S", localtime())), level='debug',
                 fmt="[%(asctime)s] [%(filename)s line:%(lineno)d] [%(levelname)s]: %(message)s"):
        super().__init__()
        self._logger = getLogger()
        self._register_info = []
        self._folder_name = JuConfig.LOG_SAVE_PATH
        if path.exists(self._folder_name) is False:
            makedirs(self._folder_name)
        self._file_name = path.join(self._folder_name, filename)
        format_str = Formatter(fmt)
        file_format = Formatter(fmt)
        self._logger.setLevel(self.level_relations.get(level))
        # self._file_handler = PathFileHandler(folder_path=JuConfig.LOG_SAVE_PATH, filename=filename, mode='a')
        self._file_handler = handlers.RotatingFileHandler(
            self._file_name, maxBytes=1024 * 1024 * 5, backupCount=1000, encoding="utf-8")
        self._file_handler.setFormatter(file_format)
        if JuConfig.CONSOLE_SWITCH is True:
            stream_handler = StreamHandler()
            stream_handler.setFormatter(format_str)
            self._logger.addHandler(stream_handler)
        self._logger.addHandler(self._file_handler)

    def __del__(self):
        self._file_handler.close()

    def get_logger(self):
        return self._logger

    def register(self, msg):
        self.register_log_signal.emit("[{}] [REGISTER]: {}".format(strftime("%Y-%m-%d_%H_%M_%S", localtime()), msg))
        if len(self._register_info) > 99:
            self._register_info.pop(0)
        self._register_info.append("[{}] [REGISTER]: {}".format(strftime("%Y-%m-%d_%H_%M_%S", localtime()), msg))

    def get_register_info(self):
        return self._register_info

    def clear_register_info(self):
        self._register_info = []

    def get_log_file_name(self):
        return path.join(JuConfig.LOG_SAVE_PATH, self._file_name)


class PathFileHandler(FileHandler):
    def __init__(self, folder_path, filename, mode='a', encoding=None, delay=False):
        if path.exists(folder_path) is False:
            makedirs(folder_path)
        file_list = sorted(listdir(folder_path))
        if len(file_list) > JuConfig.LOG_FILE_NUMBER - 1:
            try:
                remove(path.join(folder_path, file_list[0]))
            except Exception:
                pass
        self.baseFilename = path.join(folder_path, filename)
        self.mode = mode
        self.encoding = encoding
        self.delay = delay
        if delay:
            Handler.__init__(self)
            self.stream = None
        else:
            StreamHandler.__init__(self, self._open())
