#!/usr/bin/env python3
# -*- coding: utf-8 -*-

r"""
"""

__author__ = "Jiang Jun"

from pymysql import connect
from ju_cfg import JuConfig


class JuSqlInfo(object):

    def sql_connect():
        flag = True
        try:
            conn = connect(user=JuConfig.MYSQL_USER, password=JuConfig.MYSQL_PASSWORD,
                           host=JuConfig.MYSQL_HOST, database=JuConfig.MYSQL_DATABASE)
            conn.close()
        except Exception:
            flag = False
        return flag


