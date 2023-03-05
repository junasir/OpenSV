#!/usr/bin/env python3
# cython: language_level=3
# -*- coding: utf-8 -*-

r"""
ju_cfg.py
"""

__author__ = "Jun"

from os import path, environ


class JuConfig(object):
    CURRENT_FILE_PATH = path.dirname(__file__).replace("\\", "/")
    USER_ENVIRON_PATH = environ['USERPROFILE'].replace("\\", "/")
    USER_PATH = USER_ENVIRON_PATH + '/AppData/Roaming/OpenSV'
    CONSOLE_SWITCH = True
    LOG_LEVEL = "debug"
    LOG_SAVE_PATH = path.join(USER_PATH, "Log")
    LOG_FILE_NUMBER = 3
    PROGRAME_NAME = "OpenSV"
    WINDOWS_TITLE = "OpenSV Version 0.2023.2-1"
    RECENT_PROJECT_PATH = USER_ENVIRON_PATH + '/AppData/Roaming/manage_platform_v3/recent_project'
    VERSION = "0.2023.2-1"
    FIX_LOG_SAVE_PATH = USER_PATH + r'\log'
