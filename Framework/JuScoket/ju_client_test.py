# 客户端
import tkinter
from tkinter import font
import tkinter.messagebox
import socket
import threading
import time

string = ''


def my_string(s_input):
    string = s_input.get()


def Send(sock):
    '''
        发送数据的方法
        参数：
            sock：定义一个实例化socket对象
            server：传递的服务器IP和端口
    '''
    if string != '':
        message = name + ' : ' + string
        data = message.encode('utf-8')
        sock.send(data)
        if string.lower() == 'EXIT'.lower():
            exit()


def recv(sock):
    sock.send(name.encode('utf-8'))
    while True:
        data = sock.recv(1024)
        # 加一个时间戳
        time_tuple = time.localtime(time.time())
        str = ("{}点{}分".format(time_tuple[3], time_tuple[4]))
        rrecv = tkinter.Label(t, text=data.decode('utf-8'), width=40, anchor='w', bg='pink')  # 接收的消息靠左边
        rrecv.pack()


def left():
    global string
    string = rv1.get()
    Send(s)
    if string != '':
        rleft = tkinter.Label(t, text=string, width=40, anchor='e')  # 发送的消息靠右边
        rleft.pack()
        rv1.set('')


def Creat():
    global name
    name = n.get()

    # 接收进程
    tr = threading.Thread(target=recv, args=(s,), daemon=True)
    # daemon=True 表示创建的子线程守护主线程，主线程退出子线程直接销毁
    tr.start()

    l.destroy()
    e.destroy()
    b.destroy()
    t.title("聊天室")
    t.geometry("500x600")
    rL0 = tkinter.Label(t, text='%s的聊天室' % name, width=40)
    rL0.pack()
    rL1 = tkinter.Label(t, text='请输入消息：', width=20, height=1)
    rL1.place(x=0, y=450)
    rE1 = tkinter.Entry(t, textvariable=rv1)
    rE1.place(x=200, y=450)
    rB1 = tkinter.Button(t, text="发送", command=left)
    rB1.place(x=380, y=450)
    # 发送进程


def JieShu():
    tkinter.messagebox.showwarning(title='你确定退出吗？', message='刚才你点击了关闭按钮')
    s.send("error1".encode('utf-8'))
    exit(0)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server = ('127.0.0.1', 9999)
s.connect(server)  # 建立连接
t = tkinter.Tk()
t.title("多人聊天室")
t.geometry("300x200+500+200")
l = tkinter.Label(t, text='多人聊天室欢迎您，请输入你的名称', width=40, height=8)
l.pack()
n = tkinter.StringVar()
e = tkinter.Entry(t, width=15, textvariable=n)
e.pack()
rv1 = tkinter.StringVar()
name = n.get()

b = tkinter.Button(t, text="登录", width=40, height=10, command=Creat)

b.pack()
t.protocol("WM_DELETE_WINDOW", JieShu)
t.mainloop()

s.close()
