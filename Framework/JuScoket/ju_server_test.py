import socket
import threading

num = 0


def chat(service_client_socket, addr, data):
    # 等待接收客户端消息存放在2个变量service_client_socket和addr里
    if not addr in user:
        print('Accept new connection from %s:%s...' % addr)
        # 如果addr不在user字典里则执行以下代码
        for scs in serv_clie_socket:
            serv_clie_socket[scs].send(data + ' 进入聊天室...'.encode('utf-8'))
            # 发送user字典的data和address到客户端
        user[addr] = data.decode('utf-8')  # data 是最新进入聊天室的客户，解压后放入user
        serv_clie_socket[addr] = service_client_socket  # 将服务器与服务器端口号为addr的套接字放入字典
        # 接收的消息解码成utf-8并存在字典user里,键名定义为addr
    # print("可以开始聊天了>>>>>>")
    # 如果addr在user字典里，跳过本次循环
    while True:
        try:
            d = service_client_socket.recv(1024)
            if (('EXIT'.lower() in d.decode('utf-8')) | (d.decode('utf-8') == 'error1')):
                # 如果EXIT在发送的data里
                name = user[addr]
                # user字典addr键对应的值赋值给变量name
                user.pop(addr)
                serv_clie_socket.pop(addr)
                # 删除user里的addr
                for scs in serv_clie_socket:
                    # 从user取出address
                    serv_clie_socket[scs].send((name + ' 离开了聊天室...').encode('utf-8'))
                    # 发送name和address到客户端
                print('Connection from %s:%s closed.' % addr)
                global num
                num = num - 1
                break
            else:
                print('"%s" from %s:%s' % (d.decode('utf-8'), addr[0], addr[1]))
                for scs in serv_clie_socket:
                    # 从user遍历出address
                    if serv_clie_socket[scs] != service_client_socket:
                        # address不等于addr时，执行下面的代码
                        serv_clie_socket[scs].send(d)
                        # 发送data到客户端
        except BaseException as e:
            print(e)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建socket对象

addr = ('127.0.0.1', 9999)
s.bind(addr)  # 绑定地址和端口

s.listen(128)

print('TCP Server on', addr[0], ":", addr[1], "......")

user = {}  # 存放字典{addr:name}
serv_clie_socket = {}  # 存放{socket:不同线程的套接字}
while True:
    try:
        print("等待接收客户端的连接请求....")
        service_client_socket, addr = s.accept()  # 等待接收客户端的连接请求
        print("接收到客户端的连接请求....")
    except ConnectionResetError:
        print('Someone left unexcept.')
    data = service_client_socket.recv(1024)
    if data.decode() == 'error1':
        print(addr, "关闭了登录窗口。。。")
        continue
    print("data = ", data.decode())

    # 为服务器分配线程
    num = num + 1
    r = threading.Thread(target=chat, args=(service_client_socket, addr, data), daemon=True)
    r.start()
    print("聊天室人数：", num)
