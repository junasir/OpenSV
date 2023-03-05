#!/usr/bin/env python3
# cython: language_level=3
# -*- coding: utf-8 -*-

r"""
"""

__author__ = "Jiang Jun"

from multiprocessing import Process
from socket import socket, AF_INET, SOCK_STREAM
from time import sleep


class Ju_Socket_Manage_Client(Process):

    def __init__(self, receive=None, send=None, addr=None, port=None):
        super().__init__()
        self.receive = send
        self.send = receive
        self.addr = addr
        self.port = port

    def queue_receive(self):
        while True:
            if not self.receive.empty():
                msg = self.receive.get(timeout=0.1)
                self.s.send(msg)

    def run(self):
        self.s = socket(AF_INET, SOCK_STREAM)
        server = (self.addr, self.port)
        self.s.connect(server)  # 建立连接
        name = "急急急"
        self.s.send(name.encode('utf-8'))
        sleep(1)
        self.s.send(name.encode('utf-8'))
        print(2)
        while True:
            data = self.s.recv(1024)
            print(data)


if __name__ == "__main__":
    th = Ju_Socket_Manage_Client(addr='127.0.0.1', port=9999)
    th.daemon = True
    th.start()
    th.join()
    # print(2222)
    pass
