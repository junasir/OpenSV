#!/usr/bin/env python3
# cython: language_level=3
# -*- coding: utf-8 -*-

r"""
mode
type
ip
mac
deadline
logouttime
"""

__author__ = "Jiang Jun"

from binascii import b2a_base64, a2b_base64
from json import loads
from os import path
from Crypto.Cipher import AES
from ju_cfg import JuConfig


class JuAESEncrypt(object):

    def __init__(self):
        self._key = JuConfig.SECRET_KEY
        self._key_byte = JuConfig.SECRET_KEY_BYTE
        self._mode = AES.MODE_CBC

    def encrypt_file(self, url, text):
        """
        Write data to file after encryption
        """
        with open(url, "w+") as f:
            f.write(self._encrypt(text))

    def decrypt_file(self, url):
        """
        Decrypt the data after reading the file
        """
        if path.exists(url) is True:
            with open(url, "r+") as f:
                return True, loads(str(self._decrypt(f.read())).replace("'", '"'))
        return False, None

    def _encrypt(self, text):
        """
        Data encryption
        """
        text = text.encode()
        aes = AES.new(self._key, self._mode, self._key)
        length = 16
        count = len(text)
        add = 0
        if count % length != 0:
            add = length - (count % length)
        text = text + (b"\0" * add)
        return b2a_base64(aes.encrypt(text)).decode()

    def encrypt(self, text):
        return self._encrypt(text)

    def decrypt(self, text):
        return self._decrypt(text)

    def _decrypt(self, text):
        """
        Data decryption
        """
        aes = AES.new(self._key, self._mode, self._key)
        text = self._add_to_16(text)
        return aes.decrypt(a2b_base64(text)).decode().rstrip("\0")

    def _add_to_16(self, text):
        if len(text.encode('utf-8')) % 16:
            add = 16 - (len(text.encode('utf-8')) % 16)
        else:
            add = 0
        text = text + ('\0' * add)
        return text.encode('utf-8')


if __name__ == '__main__':
    pass
