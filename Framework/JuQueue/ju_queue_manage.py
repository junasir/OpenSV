#!/usr/bin/env python3
# -*- coding: utf-8 -*-

r"""
"""

__author__ = "Jiang Jun"

from datetime import datetime
from json import loads
from multiprocessing import Process
from os import path, remove
from time import sleep
from shutil import copyfile
from pymysql import connect
from requests import post

from JuFileOperate.ju_aes_encrypt import JuAESEncrypt
from JuFileOperate.ju_check_license import Ju_Check_License
from ju_cfg import JuConfig


class Ju_Process_Manage(Process):
    def __init__(self, receive=None, send=None):
        super().__init__()
        self.receive = receive
        self.send = send

    def _init_license(self):
        if path.exists("JuResource/License/manage_platform.license"):
            try:
                license_list = JuAESEncrypt().decrypt_file(url="JuResource/License/manage_platform.license")
                if license_list[0]:
                    ju_check_license = Ju_Check_License()
                    _ = ju_check_license.ju_check_license(license_text_dic=license_list[1])
                    self.send.put({"func": "_init_license", "args": _})
                else:
                    error_info = "无法解析license，请导入正确的license"
                    self.send.put({"func": "_init_license", "args": ([False, error_info])})
            except Exception:
                error_info = "无法解析license，请导入正确的license"
                self.send.put({"func": "_init_license", "args": ([False, error_info])})
        else:
            self.send.put({"func": "_init_license", "args": ([False])})

    def _load_license(self, license_path):
        if path.exists("JuResource/License/manage_platform.license"):
            remove("JuResource/License/manage_platform.license")
        copyfile(license_path, "JuResource/License/manage_platform.license")
        try:
            license_list = JuAESEncrypt().decrypt_file(url="JuResource/License/manage_platform.license")
            if license_list[0]:
                ju_check_license = Ju_Check_License()
                _ = ju_check_license.ju_check_license(license_text_dic=license_list[1])
                self.send.put({"func": "_load_license", "args": _})
            else:
                error_info = "无法解析license，请导入正确的license"
                self.send.put({"func": "_load_license", "args": ([False, error_info])})
        except Exception:
            error_info = "无法解析license，请导入正确的license"
            self.send.put({"func": "_load_license", "args": ([False, error_info])})
        print(path)

    def _get_mysql_info(self, title):
        _conn = connect(user=JuConfig.MYSQL_USER, password=JuConfig.MYSQL_PASSWORD,
                        host=JuConfig.MYSQL_HOST, database=JuConfig.MYSQL_DATABASE)
        _cursor = _conn.cursor()
        cmd = """select unshow_flag from all_info where title='{}';""".format(title)
        _cursor.execute(cmd)
        res = _cursor.fetchall()
        print(res)
        result = True
        if len(res) > 0:
            if res[0][0] == 1:
                result = True
            elif res[0][0] == 0:
                result = False
        self.send.put({"func": "_get_mysql_info", "args": (result, )})

    def upload_login_record(self, user_name):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        version = JuConfig.VERSION
        user_name = user_name
        dic_text = {"operation": "upload_login_record", "value": [user_name, current_time, version]}
        data = JuAESEncrypt().encrypt(str(dic_text))
        response = post(url=JuConfig.URL, data=data)
        de_data = JuAESEncrypt().decrypt(response.text)
        if loads(de_data)["flag"]:
            self.send.put({"func": "ui_log", "args": ("Login Ok", )})

    def run(self):
        # self.send_queue.put({"func": "modify_use_item_status", "args": ("paused",)})
        while True:
            if not self.receive.empty():
                msg = self.receive.get(timeout=0.1)
                if isinstance(msg, dict) is True and hasattr(self, msg.get("func")) is True:
                    getattr(self, msg.get("func"))(*msg.get("args", ()), **msg.get("kwargs", {}))
                elif isinstance(msg, str):
                    if msg == "break":
                        break
            sleep(0.1)
            pass
