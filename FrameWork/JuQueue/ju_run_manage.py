#!/usr/bin/env python3
# -*- coding: utf-8 -*-

r"""
"""

__author__ = "Jiang Jun"

import subprocess
import sys
from multiprocessing import Process
from ju_cfg import JuConfig


class Ju_Run_Manage(Process):
    def __init__(self, receive=None, python_path=None, file_path=None):
        super().__init__()
        self.envs = python_path
        self.location = file_path
        self.receive = receive
        # sleep(2)
        # self.receive.put({"func": "ui_log", "args": ("==================", )})
        # self.send = send

    def run(self):
        sys.path.append(JuConfig.RECENT_PROJECT_PATH)
        # location = r"E:\project\manage_platform_v2.1\code_editer\1.py"
        # sys.path.append(base_loc)
        # print(sys.path)
        self.receive.put({"func": "ui_log", "args": ("{}文件开始运行".format(self.location.split('/')[-1]),)})
        # self.Ju_Ui_Main.info_show.emit("{}文件开始运行".format(self.location.split('/')[-1]))
        # envs = os.getcwd().replace('\\', '/') + '/envs/python'
        envs = self.envs
        cmd = "cd /d {} & {} -u {}".format(JuConfig.RECENT_PROJECT_PATH, envs, self.location)
        code = "utf8"
        self.process = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                        stderr=subprocess.STDOUT)
        while self.process.poll() is None:
            line = self.process.stdout.readline()
            line = line.strip()
            if line:
                info = self.location.split('/')[-1] + "-->  " + line.decode(code, 'ignore')
                print(info)
                self.receive.put({"func": "ui_log", "args": (info,)})
                # sleep(0.05)
                # self.Ju_Ui_Main.info_show.emit(line.decode(code, 'ignore'))
                # print(line.decode(code, 'ignore'))
        self.receive.put({"func": "ui_log", "args": ("{} 文件运行结束".format(self.location.split('/')[-1]),)})
        # self.Ju_Ui_Main.info_show.emit("{} 文件运行结束".format(self.location.split('/')[-1]))
        self.receive.put({"func": "set_thread_run", "args": (False,)})
        # self.Ju_Ui_Main.thread_run = False