#!/usr/bin/env python3
# cython: language_level=3
# -*- coding: utf-8 -*-

r"""
"""
from time import sleep

__author__ = "Jiang Jun"

from datetime import datetime
from multiprocessing import Process
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from loguru import logger
from ju_cfg import JuConfig

now = (datetime.now()).strftime("%Y-%m-%d %H_%M_%S")
logger.add(JuConfig.LOG_SAVE_PATH + "/runtime_" + str(now) + ".log", retention='10 days')


class Ju_Socket_Manage_Server(Process):

    def __init__(self, receive=None, send=None, addr=None):
        super().__init__()
        self.receive = send
        self.send = receive
        self.current_user = {}
        self.num = 0
        self.serv_clie_socket = {}

    def chat_thread(self, service_client_socket, addr, data):
        # 等待接收客户端消息存放在2个变量service_client_socket和addr里
        print(self.current_user, addr)
        if not addr in self.current_user:
            logger.debug('Accept new connection from %s:%s...' % addr)
            # 如果addr不在user字典里则执行以下代码
            for scs in self.serv_clie_socket:

                self.serv_clie_socket[scs].send(data + ' 进入聊天室...'.encode('utf-8'))
                # 发送user字典的data和address到客户端
            self.current_user[addr] = data.decode('utf-8')  # data 是最新进入聊天室的客户，解压后放入user
            self.serv_clie_socket[addr] = service_client_socket  # 将服务器与服务器端口号为addr的套接字放入字典
            # 接收的消息解码成utf-8并存在字典user里,键名定义为addr
        # print("可以开始聊天了>>>>>>")
        # 如果addr在user字典里，跳过本次循环
        print(self.current_user)
        while True:
            try:
                d = service_client_socket.recv(1024)
                if ('EXIT'.lower() in d.decode('utf-8')) | (d.decode('utf-8') == 'error1'):
                    # 如果EXIT在发送的data里
                    name = self.current_user[addr]
                    dic = {"info": self.current_user[addr], "add0": addr}
                    self.send.put(dic)
                    # user字典addr键对应的值赋值给变量name
                    self.current_user.pop(addr)
                    print(self.current_user, "========")
                    self.serv_clie_socket.pop(addr)
                    # 删除user里的addr
                    for scs in self.serv_clie_socket:
                        # 从user取出address
                        self.serv_clie_socket[scs].send((name + ' 离开了聊天室...').encode('utf-8'))
                        # 发送name和address到客户端
                    logger.debug('Connection from %s:%s closed.' % addr)
                    self.num = self.num - 1
                    break
                else:
                    # print('"%s" from %s:%s' % (d.decode('utf-8'), addr[0], addr[1]))
                    dic = {"info": d.decode('utf-8'), "add0": addr}
                    self.send.put(dic)
                    for scs in self.serv_clie_socket:
                        # 从user遍历出address
                        if self.serv_clie_socket[scs] != service_client_socket:
                            # address不等于addr时，执行下面的代码
                            self.serv_clie_socket[scs].send(d)
                            # 发送data到客户端
            except BaseException as e:
                # print(e)
                logger.debug(e)
                dic = {"info": {"close", self.current_user[addr]}, "add0": addr}
                self.send.put(dic)
                self.current_user.pop(addr)
                self.serv_clie_socket.pop(addr)
                # print(self.current_user[addr])
                break
            sleep(0.1)

    def queue_receive(self):
        while True:
            if not self.receive.empty():
                msg = self.receive.get(timeout=0.1)
                for scs in self.serv_clie_socket:
                    self.serv_clie_socket[scs].send(msg)
            sleep(0.1)

    def run(self):
        q_receive = Thread(target=self.queue_receive, args=(), daemon=True)
        q_receive.start()
        s = socket(AF_INET, SOCK_STREAM)  # 创建socket对象
        addr = ('127.0.0.1', 9999)
        s.bind(addr)  # 绑定地址和端口
        s.listen(128)
        logger.debug('TCP Server on{},{},{}'.format(addr[0], addr[1], "......"))
        while True:
            try:
                logger.debug("等待接收客户端的连接请求....")
                service_client_socket, addr = s.accept()  # 等待接收客户端的连接请求
                logger.debug("接收到客户端的连接请求....")
            except ConnectionResetError:
                logger.debug('Someone left unexcept.')
            data = service_client_socket.recv(1024)
            if data.decode() == 'error1':
                logger.debug(str(addr) + "关闭了登录窗口。。。")
                continue
            logger.debug("data = " + data.decode())

            # 为服务器分配线程
            self.num = self.num + 1
            r = Thread(target=self.chat_thread, args=(service_client_socket, addr, data), daemon=True)
            # 线程ID
            # print('Thread id : ',  r.ident)
            # 线程NAME
            # print('Thread name :',  r.getName())
            r.start()
            # print("聊天室人数：", self.num)


if __name__ == "__main__":
    th = Ju_Socket_Manage_Server()
    th.daemon = True
    th.start()
    th.join()
    # print(2222)
    pass
