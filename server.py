import socket,pymysql
from tkinter import Tk,ttk,Canvas,Button,Entry,Checkbutton,Label,PhotoImage,NW,END,scrolledtext,BooleanVar,StringVar,messagebox
from queue import Queue
from time import strftime,sleep,time,localtime
import threading
import user1

#连接数据库
def connect_to_mysql():
    db = pymysql.connect(
        host='127.0.0.1',  # 连接主机, 默认127.0.0.1
        user='root',  # 用户名
        passwd='021128',  # 密码
        port=3306,  # 端口，默认为3306
        db='test',  # 数据库名称
        charset='utf8')
    print('数据库连接成功')
    return db

#服务器程序
class service:
    def __init__(self,group_id):
        self.group_id=group_id[0]
        #获取群端口
        db=connect_to_mysql()
        cursor = db.cursor()
        sql1 = 'SELECT distinct port FROM group_info where group_id=%s' % self.group_id
        cursor.execute(sql1)
        self.group_port=cursor.fetchone()[0]#群端口
        sql2='select member_id from group_info where group_id=%s' % self.group_id
        cursor.execute(sql2)
        self.group_member_list=cursor.fetchall()#群聊中的成员列表
        print(self.group_member_list)
        # 创建服务器socket
        self.server_socket = socket.socket()
        # self.server_socket.setblocking(False)#设置socket为非阻塞模式
        # 绑定监听端口
        self.server_socket.bind(('127.0.0.1', int(self.group_port)))
        self.server_socket.listen(50)
        # 开始监听
        threading.Thread(target=self.recv_message).start()#接收信息线程
    # 接收信息
    def recv_message(self):
        while True:
            try:
                print('群聊' + str(self.group_id) + '正在监听')
                conn,addr=self.server_socket.accept()#接收连接
                print(str(addr)+'已连接')
                message = conn.recv(1024).decode()
                #将信息数据拆分
                send_user_id=message.split(',')[0]#发送者id
                msg=message.split(',')[1]#发送的消息内容
                # 给群里的成员每一个都发信息
                for j in range(len(self.group_member_list)):
                    self.send_msg_to_group(self.group_member_list[j][0],send_user_id,msg)
            except:
                continue
    #群发消息
    def send_msg_to_group(self,recv_id,send_user_id,msg):
        db = connect_to_mysql()
        cursor = db.cursor()
        sql1 = 'SELECT port FROM user_info where id=%s' % recv_id#得到接收者的端口
        cursor.execute(sql1)
        recv_port=cursor.fetchone()[0]
        if recv_id !=send_user_id:
            #根据群聊成员端口发送信息
            self.send_socket=socket.socket()
            self.send_socket.connect(('127.0.0.1', recv_port))
            self.send_socket.send(bytes(str(send_user_id)+','+str(msg),encoding='utf-8'))#发送者id和消息内容


if __name__ == '__main__':
     db=connect_to_mysql()
     cursor=db.cursor()
     sql1='SELECT DISTINCT group_id FROM group_info GROUP BY group_id'
     cursor.execute(sql1)
     group_list = cursor.fetchall()#群id
     sql2='SELECT COUNT(distinct group_id) from group_info'
     cursor.execute(sql2)
     group_count=cursor.fetchone()[0]#群组数量
     db.close()
     for i in range(group_count):#为每个群聊开线程
         server=service(group_list[i])
         threading.Thread(target=server.recv_message).start()

