#!/usr/bin/env python3
# -*- coding: utf-8 -*-

r"""
"""

__author__ = "Jiang Jun"

from datetime import datetime
from socket import socket, AF_INET, SOCK_DGRAM
from uuid import UUID, getnode
from JuLog.ju_logger import JuLogger
from ju_cfg import JuConfig
from JuFileOperate.ju_aes_encrypt import JuAESEncrypt


class Ju_Check_License(object):

    def __init__(self):
        self.logger = JuLogger(level=JuConfig.LOG_LEVEL).get_logger()

    def ju_check_license(self, license_text_dic):
        license_text_dic = license_text_dic
        mode = license_text_dic["mode"]
        person_type = license_text_dic["person_type"]
        ip = license_text_dic["ip"]
        mac = license_text_dic["mac"]
        deadline = license_text_dic["deadline"]
        logout = license_text_dic["logout"]
        print(mode, person_type, ip, mac, deadline, logout)
        flag_mac, _mac = self._check_mac(mac_address=mac)
        flag_date, _date = self._check_datetime(deadline=deadline)
        flag_date_, _logout = self._check_logout_datetime(deadline=logout)
        if flag_mac is False:
            return [False, _mac]
        elif flag_date is False:
            return [False, _date]
        elif flag_date_ is False:
            return [False, _logout]
        else:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            license_text_dic["logout"] = current_time
            print(license_text_dic)
            JuAESEncrypt().encrypt_file(JuConfig.LICENSE_PATH, str(license_text_dic))
            if mode == "mode1":
                if person_type == "student":
                    flag_ip = self._check_ip()
                    if flag_ip:
                        return [True, person_type, ip]
                    else:
                        return [True, person_type]
                elif person_type == "teacher":
                    return [True, person_type]
            elif mode == "mode2":
                return [True, person_type]

    def _check_mac(self, mac_address):
        mac = UUID(int=getnode()).hex[-12:]
        mac = ":".join([mac[e:e + 2] for e in range(0, 11, 2)])
        if mac == mac_address:
            return True, None
        else:
            return False, "license不属于本机！！"

    def _check_datetime(self, deadline):
        overdate = datetime.strptime(deadline, '%Y-%m-%d %H:%M:%S')
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        current_time = datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S')
        delta = (overdate - current_time).seconds
        delta_days = (overdate - current_time).days
        self.logger.info(str(delta))
        if delta_days < 0:
            return False, "license超过使用期限！！"
        else:
            if delta > 0:
                return True, None
            else:
                return False, "license超过使用期限！！"

    def _check_logout_datetime(self, deadline):
        overdate = datetime.strptime(deadline, '%Y-%m-%d %H:%M:%S')
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        current_time = datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S')
        delta = (overdate - current_time).seconds
        delta_days = (overdate - current_time).days
        self.logger.info(str(delta))
        if delta_days < 0:
            if delta > 0:
                return True, None
            else:
                return False, "本地时间不正确！！"
        else:
            return False, "本地时间不正确！！"

    def _check_ip(self, ip=None):
        ip_list = ip.split(".")
        ip_text = str(ip_list[0]) + str(ip_list[1]) + str(ip_list[2])
        local_ip, local_gateway = self._get_host_ip()
        print(local_ip, local_gateway)
        if ip_text == local_gateway:
            return True
        else:
            return False

    def _get_host_ip(self):
        try:
            s = socket(AF_INET, SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
            ip_list = ip.split(".")
            ip_text = str(ip_list[0]) + str(ip_list[1]) + str(ip_list[2])
        finally:
            s.close()
        return ip, ip_text
