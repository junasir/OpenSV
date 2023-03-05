#!/usr/bin/env python3
# -*- coding: utf-8 -*-

r"""
aw_logger.py
This file is used to output log.
"""

__author__ = "Li JunJie"

from queue import Queue
from cgitb import enable
from datetime import datetime
from logging import StreamHandler, Formatter, Logger
from logging.handlers import RotatingFileHandler
from os import path, mkdir, makedirs
from sys import stdout
from time import time, localtime, strftime

from PySide2.QtCore import Signal, QObject
from numpy import long

from ju_cfg import JuConfig


class JuLogger(QObject):
    s_log = Signal(str)

    def __init__(self, logtype='ui_log'):
        super(JuLogger, self).__init__()
        self._msg_queue = None
        if logtype == "test_log":
            self._msg_queue = Queue(maxsize=1000)
        self._logtype = logtype
        self.creat_new_file_handle()

    def creat_new_file_handle(self):
        # curr_time = datetime.now()
        # time_str = datetime.strftime(curr_time, '%Y-%m-%d_%H-%M-%S_log.txt')
        ct = time()
        local_time = localtime(ct)
        data_head = strftime("%Y-%m-%d_%H-%M-%S", local_time)
        data_secs = (ct - long(ct)) * 1000
        time_stamp = "%s_%03d" % (data_head, data_secs)
        time_str = "{}_log.txt".format(time_stamp)
        data_path = JuConfig.FIX_LOG_SAVE_PATH
        if not path.exists(data_path):
            makedirs(data_path)
        data_path = path.join(data_path, self._logtype)
        if not path.exists(data_path):
            mkdir(data_path)
        self._fpath = path.join(data_path, time_str)
        file_handler = RotatingFileHandler(self._fpath, maxBytes=1024 * 1024 * 10, backupCount=10, encoding='utf-8')
        # file_handler = FileHandler(fpath, 'a')  # out to file
        console_handler = StreamHandler(stream=stdout)  # out to console
        file_handler.setLevel('DEBUG')  # out to file when leve over debug
        console_handler.setLevel('DEBUG')  # out to console when leve over debug

        # fmt = '%(asctime)s - %(file_name)s - %(funcName)s - %(lineno)s - %(levelname)s - %(message)s'
        fmt = '%(asctime)s - %(levelname)s - %(message)s'
        formatter = Formatter(fmt)
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        # self._log = getLogger('updateSecurity')
        self._log = Logger(self._logtype)
        self._log.setLevel('DEBUG')  # out over debug level log when set

        self._log.addHandler(file_handler)  # add handler
        self._log.addHandler(console_handler)
        enable(logdir=data_path, format='text')

    def info(self, *args):
        s = ''
        for i in args:
            s += (str(i) + ' ')
        self._log.info(s)
        self.emit_log(msg=s, level=' - INFO - ')

    def error(self, *args):
        s = ''
        for i in args:
            s += (str(i) + ' ')
        self._log.error(s)
        self.emit_log(msg=s, level=' - ERROR - ')

    def warning(self, *args):
        s = ''
        for i in args:
            s += (str(i) + ' ')
        self._log.warning(s)
        self.emit_log(msg=s, level=' - WARN - ')

    def debug(self, *args):
        s = ''
        for i in args:
            s += (str(i) + ' ')
        self._log.debug(s)
        self.emit_log(msg=s, level=' - DEBUG - ')

    def emit_log(self, msg=None, level=' - INFO - '):
        if msg is not None:
            curr_time = datetime.now()
            time_str = datetime.strftime(curr_time, '%Y-%m-%d %H:%M:%S:%f')
            self.s_log.emit(time_str + level + msg)
            if self._msg_queue is not None:
                self._msg_queue.put(time_str + level + msg)

    def msg_queue_get(self):
        if self._msg_queue is not None:
            msg = self._msg_queue.get()
            return msg
        return None


if __name__ == "__main__":
    loger1 = JuLogger('ui_log')
    loger2 = JuLogger('test_log')
    loger1.info('ui log ok', "2222")
    loger2.info('test log ok')
