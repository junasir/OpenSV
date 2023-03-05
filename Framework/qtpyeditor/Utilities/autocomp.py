# -*- coding:utf-8 -*-
# @Time: 2021/1/30 11:40
# @Author: Zhanyi Hou
# @Email: 1295752786@qq.com
# @File: autocomp.py
import re
import time
from PySide2.QtCore import QThread, Signal
import jedi


class AutoCompThread(QThread):
    '''
    当一段时间没有补全需求之后，后台自动补全线程会进入休眠模式。下一次补全请求则会唤醒该后台线程。
    '''
    trigger = Signal(tuple, list)

    def __init__(self, log=None):
        super(AutoCompThread, self).__init__()
        self.user_logger = log
        self.text = ''
        self.envs = None
        self.text_cursor_pos = (0, 1)
        self.activated = True
        self.stop_flag = False
        self.path = None

    def set_envs(self, path):
        self.path = path
        # self.envs = jedi.create_environment(path=path, safe=True)

    def run(self):
        if self.path is not None:
            self.envs = jedi.create_environment(path=self.path, safe=True)
        text = ''
        last_complete_time = time.time()
        # try:
        #     # if self.path != "":
        #     #     a = jedi.create_environment(path=r"C:/Users/Jun/AppData/Local/Programs/Python/Python38/test")
        # except ImportError:
        #     print('Jedi not installed.install jedi for better auto-completion!')
        #     return
        while 1:
            if self.stop_flag:
                return

            if self.text == text:
                if time.time() - last_complete_time >= 30:
                    self.activated = False
                time.sleep(0.02 if self.activated else 0.1)
                continue

            try:
                row_text = self.text.splitlines()[self.text_cursor_pos[0] - 1]
                hint = re.split(
                    '[.:;,?!\s \+ \- = \* \\ \/  \( \)\[\]\{\} ]', row_text)[-1]
                content = (
                    self.text_cursor_pos[0], self.text_cursor_pos[1], hint
                )
                self.user_logger.info('Text of current row:%s' % content[2])
                if self.path != "":
                    if self.envs is not None:
                        script = jedi.Script(self.text, environment=self.envs)
                    else:
                        script = jedi.Script(self.text)
                else:
                    script = jedi.Script(self.text)
                l = script.complete(*self.text_cursor_pos)

            except:
                import traceback
                traceback.print_exc()
                l = []
            self.trigger.emit(content, l)
            last_complete_time = time.time()

            self.activated = True
            text = self.text

    def on_exit(self):
        self.stop_flag = True
        self.exit(0)
        if self.isRunning():
            self.quit()
        self.wait(500)
