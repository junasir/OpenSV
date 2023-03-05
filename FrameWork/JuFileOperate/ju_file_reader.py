#!/usr/bin/env python3
# -*- coding: utf-8 -*-

r"""
ju_file_reader.py
This file is used to read file.
"""

__author__ = "Jiang Jun"

from os import path
from copy import deepcopy


class JuFileRead(object):
    def __init__(self):
        pass

    @staticmethod
    def read_file(fpath):
        if path.exists(fpath):
            with open(fpath, 'r') as f:
                return f.read()

    @staticmethod
    def read_bin_file(fpath):
        if path.exists(fpath):
            with open(fpath, 'rb') as f:
                return f.read()
        else:
            return None

    @staticmethod
    def write_bin_file(fpath, w_data):
        if w_data is not None:
            with open(fpath, "wb") as f:
                f.write(w_data)
            return True
        return False

    @staticmethod
    def read_ju_chip_cfg_bin(fpath, addr_width=1, data_width=2):
        reg_cfg_list = []
        old_format = False
        reg_addr_len = 1
        reg_data_len = 2
        read_file_data = JuFileRead().read_bin_file(fpath)
        if read_file_data is not None:
            calcu_check_sum = 0
            if len(read_file_data) > 64:
                for one_byte in read_file_data[4:]:
                    calcu_check_sum += one_byte
                calcu_check_sum %= 0x100000000
                check_sum = (read_file_data[3] << 24) | (read_file_data[2] << 16) | \
                            (read_file_data[1] << 8) | (read_file_data[0])
                data_type = (read_file_data[11] << 24) | (read_file_data[10] << 16) | \
                            (read_file_data[9] << 8) | (read_file_data[8])
                reg_addr_len = (read_file_data[35] << 24) | (read_file_data[34] << 16) | \
                               (read_file_data[33] << 8) | (read_file_data[32])
                reg_data_len = (read_file_data[39] << 24) | (read_file_data[38] << 16) | \
                               (read_file_data[37] << 8) | (read_file_data[36])
                if check_sum == calcu_check_sum:
                    reg_cfg_list = JuFileRead().read_ju_chip_bin_reg_data(data_type=data_type,
                                                                          data_area=read_file_data[60:],
                                                                          reg_addr_len=reg_addr_len,
                                                                          reg_data_len=reg_data_len)
                else:
                    old_format = True
            else:
                old_format = True
            if old_format is True:
                if type(addr_width) is int and type(data_width) is int:
                    reg_addr_len = addr_width
                    reg_data_len = data_width
                for i in range(int(len(read_file_data) / (reg_data_len * 2))):
                    reg = 0
                    value = 0
                    for j in range(reg_data_len - 1, -1, -1):
                        reg <<= 8
                        reg += read_file_data[i * (reg_data_len * 2) + j]
                    for j in range(reg_data_len - 1, -1, -1):
                        value <<= 8
                        value += read_file_data[i * (reg_data_len * 2) + reg_data_len + j]
                    reg_cfg_list.append([deepcopy(str(hex(reg))), deepcopy(str(hex(value)))])
        return reg_cfg_list

    @staticmethod
    def read_ju_chip_cfg_txt(fpath):
        result = []
        cfg_content = JuFileRead().read_bin_file(fpath)
        if cfg_content is not None:
            temp_str = str(cfg_content)[2:-1]
            for item in temp_str.split("\\r\\n"):
                result.append(item.split(":"))
        return result

    @staticmethod
    def read_ju_chip_bin_reg_data(data_type=0x00, data_area=None, reg_addr_len=2, reg_data_len=2):
        reg_cfg_list = []
        try:
            if len(data_area) >= 4:
                if data_type == 0x00:
                    reg_count = (data_area[3] << 24) | (data_area[2] << 16) | \
                                (data_area[1] << 8) | (data_area[0])
                    if reg_count * (reg_addr_len + reg_data_len) == len(data_area) - 4:
                        for i in range(0, reg_count):
                            reg_addr = 0
                            reg_write_data = 0
                            for j in range(reg_addr_len - 1, -1, -1):
                                reg_addr <<= 8
                                reg_addr += data_area[i * (reg_addr_len + reg_data_len) + j + 4]
                            for j in range(reg_data_len - 1, -1, -1):
                                reg_write_data <<= 8
                                reg_write_data += data_area[i * (reg_addr_len + reg_data_len) + reg_addr_len + j + 4]
                            reg_cfg_list.append([deepcopy(hex(reg_addr)), deepcopy(hex(reg_write_data))])
                elif data_type == 0x2000:
                    muli_bin_count = (data_area[3] << 24) | (data_area[2] << 16) | \
                                     (data_area[1] << 8) | (data_area[0])
                    muli_bin_info = []
                    for i in range(0, muli_bin_count):
                        bin_offset_addr = 0
                        bin_data_len = 0
                        for j in range(3, -1, -1):
                            bin_offset_addr <<= 8
                            bin_offset_addr += data_area[8 * i + j + 4]
                        for j in range(3, -1, -1):
                            bin_data_len <<= 8
                            bin_data_len += data_area[8 * i + j + 8]
                        muli_bin_info.append([bin_offset_addr, bin_data_len])
                    for one_bin_info in muli_bin_info:
                        data_type = (data_area[one_bin_info[0] + 11] << 24) | \
                                    (data_area[one_bin_info[0] + 10] << 16) | \
                                    (data_area[one_bin_info[0] + 9] << 8) | (data_area[one_bin_info[0] + 8])
                        reg_addr_len = (data_area[one_bin_info[0] + 35] << 24) | \
                                       (data_area[one_bin_info[0] + 34] << 16) | \
                                       (data_area[one_bin_info[0] + 33] << 8) | (data_area[one_bin_info[0] + 32])
                        reg_data_len = (data_area[one_bin_info[0] + 39] << 24) | \
                                       (data_area[one_bin_info[0] + 38] << 16) | \
                                       (data_area[one_bin_info[0] + 37] << 8) | (data_area[one_bin_info[0] + 36])
                        if data_type == 0:
                            temp_data = data_area[one_bin_info[0] + 60:one_bin_info[0] + one_bin_info[1]]
                            reg_cfg_list = JuFileRead().read_ju_chip_bin_reg_data(data_type=0,
                                                                                  data_area=temp_data,
                                                                                  reg_addr_len=reg_addr_len,
                                                                                  reg_data_len=reg_data_len)
                            break
        except Exception:
            pass
        return reg_cfg_list
#
#
# if __name__ == '__main__':
#     pass
