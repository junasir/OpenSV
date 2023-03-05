#!/usr/bin/env python3
# -*- coding: utf-8 -*-

r"""
ju_json_operate.py
This file is about json file operate.
"""

__author__ = "Jiang Jun"

from json import dumps, loads
from os import path


class JuJsonOperate(object):

    def __init__(self):
        pass

    @staticmethod
    def ju_write_to_json(data=None, url=None):
        if data is not None and url is not None:
            with open(url, mode="w", encoding="utf-8") as f:
                json_str = dumps(data, ensure_ascii=False, separators=(',', ':'))  # , indent=5)
                f.write(json_str)
                return True, 'write json success.'
        return False, 'write json failed.'

    @staticmethod
    def ju_load_json(url=None):
        if url is not None and path.exists(url) is True:
            with open(url, "r", encoding="UTF-8") as f:
                res = f.read()
                return loads(res), True, 'load json success.'
        return None, False, 'load json failed.'

#
# if __name__ == '__main__':
#     dic = {'1.1': 1, '1.2': 2}
#     json = JuJsonOperate()
#     json.ju_write_to_json(dic, "1.json")
#     data, flag, msg = json.ju_load_json("1.json")
#     # print(data)
