import socket
import threading
from tkinter import Tk,ttk,Canvas,Button,Entry,Checkbutton,Label,PhotoImage,NW,END,scrolledtext,BooleanVar,StringVar,messagebox,Menu
from threading import Thread
from time import strftime,sleep,time,localtime
import  time
import random
import  tkinter
import pymysql
import server


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

#登录
class LoginPanel:
    def run(self):
        self.root.mainloop()

    def __init__(self):
        # 图形界面区域
        self.root = Tk()
        self.root.title('登录')
        self.root.geometry('450x220+700+400')

        # 输入区域
        self.input = Canvas(self.root, bg='#ffffff')
        self.input.place(x=0, y=0, heigh=350, width=450)

        # 账号输入框标签
        Label(self.root, text="账号:", background='white').place(x=75, y=53)
        Label(self.root, text="密码:", background='white').place(x=75, y=90)
        db=connect_to_mysql()
        cursor = db.cursor()
        sql1 = 'select id from user_info'
        cursor.execute(sql1)
        print('执行成功!')
        id_data = cursor.fetchall()
        print(id_data)

        # 账号输入框  账号输入框
        xVariable = tkinter.StringVar()  # #创建变量，便于取值
        self.accountinput = ttk.Combobox(self.root, textvariable=xVariable)  # 创建下拉菜单
        self.accountinput.pack()  # #将下拉菜单绑定到窗体
        self.accountinput.place(x=130, y=50, heigh=30, width=210)
        self.accountinput["value"] = id_data  # #给下拉菜单设定值
        self.accountinput.current(0)  # 设定下拉菜单的默认值为第1个

        # 密码输入框
        self.passwordinput = Entry(self.input, font=("宋体", 16, "bold"), show='*')
        self.passwordinput.place(x=130, y=85, heigh=30, width=210)

        # 登陆按钮
        self.loginbutton = Button(self.input, text='登录', bg='#4fcffd',command=self.loginbutton_clicked)
        self.loginbutton.place(x=100, y=160, heigh=40, width=240)

        # 注册账号按钮
        self.registerbutton = Button(self.input, text='注册账号', bg='white',command=RegisterPanel)
        self.registerbutton.place(x=10, y=190, heigh=20, width=70)
        sql3 = 'select id from user_info where id=%s' % (self.accountinput.get())
        cursor.execute(sql3)
        self.account_id=cursor.fetchone()
        db.close()  #关闭数据库
        print('数据库连接断开')
        # 登录按钮点击事件

    def loginbutton_clicked(self):
        # 输入过滤
        account = self.accountinput.get().strip().replace(' ', '')
        self.accountinput.delete(0, END)
        self.accountinput.insert(END, account)
        print(account)
        password = self.passwordinput.get().strip().replace(' ', '')
        self.passwordinput.delete(0, END)
        self.passwordinput.insert(END, password)
        print(password)
        print('等待连接数据库。。。')
        db = connect_to_mysql()
        cursor = db.cursor()
        sql1 = "select * from user_info where id=%s" % account  # 数据库中查询与账号对应的元组
        sql2 = 'select id from user_info'
        # 获取数据库中的信息
        cursor.execute(sql1)
        result1 = cursor.fetchone()
        # cursor.execute(sql2)
        # result2=cursor.fetchone()
        print(account)
        password = self.passwordinput.get().replace(' ', '')
        print(password)

        if len(account) < 8 or not account.isdigit():
            messagebox.showinfo('登录失败', '查无此号')
        for c in password:
            if ord(c) > 255:
                messagebox.showinfo('登录失败', '密码错误\n( ⊙ o ⊙ )')
        try:
            print('results', result1)
            if result1[1] == password:
                messagebox.showinfo('登录成功', '登录成功')
                db.close()
                self.root.destroy()
                mainpanel = MainPanel(result1[0])
                mainpanel.run()
                return 1
            messagebox.showinfo('登录失败', '账号密码不匹配')
        except:
            print('登录抛出异常')
            db.rollback()
        return -1

#注册
class RegisterPanel:
    def run(self):
        self.root.mainloop()
    #图形界面
    def __init__(self):
        self.root = Tk()
        self.root.title('用户注册')
        self.root.geometry('450x220+700+450')

        # 输入区域
        self.input = Canvas(self.root, bg='#ffffff')
        self.input.place(x=0, y=0, heigh=220, width=450)

        # 昵称账号密码输入提醒
        Label(self.root, text="账号:", background='white').place(x=77, y=63)
        Label(self.root, text="密码:", background='white').place(x=77, y=97)

        # 账号输入框
        self.accountinput = Entry(self.input, font=("宋体", 16, "bold"))
        self.accountinput.place(x=130, y=60, heigh=30, width=210, )

        # 密码输入框
        self.passwordinput = Entry(self.input, font=("宋体", 16, "bold"), show='*')
        self.passwordinput.place(x=130, y=95, heigh=30, width=210)

        # 注册按钮
        self.registerbutton = Button(self.input, text='立即注册', bg='#4fcffd', command=self.register_button_clicked)
        self.registerbutton.place(x=100, y=160, heigh=40, width=240)

    #注册按钮点击
    def register_button_clicked(self):
        # 输入
        account = self.accountinput.get().strip().replace(' ', '')
        self.accountinput.delete(0, END)
        self.accountinput.insert(END, account)
        print(account)
        password = self.passwordinput.get().strip().replace(' ', '')
        self.passwordinput.delete(0, END)
        self.passwordinput.insert(END, password)
        print(password)
        # 输入过滤
        if len(account) < 8 or len(password) < 8:
            messagebox.showinfo('注册失败', '账号或密码至少8位\no(︶︿︶)o')
            return -1
        if not account.isdigit():
            messagebox.showinfo('注册失败', '账号必须全为数字\n(╯﹏╰）')
            return -2
        for c in password:
            if ord(c) > 255:
                messagebox.showinfo('注册失败', '密码不能包含非法字符\n( ⊙ o ⊙ )')
                return -3
        port=int(random.randint(1,1000000)%65535)
        db=connect_to_mysql()
        cursor=db.cursor()
        sql="INSERT INTO user_info(id, pwd, port) VALUES ('%s', '%s', %d)" % (account, password, port)
        try:
            cursor.execute(sql)
            db.commit()
            print('成功修改数据库内容')
        except:
            db.rollback()
            print("失败")
        db.close()
        messagebox.showinfo('注册成功','恭喜您 注册成功\n~\(≧▽≦)/~')
        self.root.destroy()#销毁注册窗口
        return 1

#主界面
class MainPanel:
    def run(self):
        self.root.mainloop()

    def __init__(self,user_id):

        self.user_id=user_id
        #界面
        self.root=Tk()
        self.root.title('app主界面')
        self.root.geometry('350x800+400+50')

        #个人信息区域
        self.head=Canvas(self.root,bg='#ADD8E6')
        self.head.place(x=5,y=0,heigh=135,width=340)

        # 自己的id标签
        self.id_label = Label(text='当前用户:'+str(self.user_id), bg='#ADD8E6')
        self.id_label.place(x=30, y=50)

        #好友区域
        self.frend = Canvas(self.root, bg='#ADD8E6')
        self.frend.place(x=5, y=210, heigh=590, width=340)

        #设置区域
        self.setting = Canvas(self.root, bg='#ADD8E6')
        self.setting.place(x=5, y=760, heigh=40, width=340)

        #显示好友，群聊按钮
        self.friend_btn = Button(self.root, text='好友',command=self.refresh_friend_list).place(x=10,y=173,height=30,width=165,)
        self.group_btn = Button(self.root, text='群聊',command=self.refresh_group_list).place(x=180,y=173,height=30,width=160)

        #好友栏
        self.contact_area=scrolledtext.ScrolledText()
        self.contact_area.place(x=10, y=215, heigh=540, width=330)

        # 在界面添加输入框和按钮
        self.add_entry = Entry(self.root)
        self.add_entry.place(x=40, y=135, height=30, width=225)
        self.add_button = Button(self.root, text='+', command=self.add_button_clicked).place(x=6, y=135, height=30, width=30)  # 添加按钮
        #创建群聊按钮
        self.create_group_button=Button(self.root,text='创建群聊',command=self.create_group_button_clicked).place(x=270, y=135, height=30, width=70)

        #刷新好友列表
        self.refresh_friend_list()

    # 添加按键点击
    def add_button_clicked(self):
        # 获取输入的用户名
        search_id = self.add_entry.get()
        try:
            if search_id:#不为空
                # 连接数据库
                db = connect_to_mysql()
                cursor = db.cursor()
                # 数据库搜索用户或群是否存在
                sql1 = "SELECT id FROM user_info WHERE id=%s" % search_id
                sql2="select DISTINCT group_id from group_info where group_id=%s" % search_id
                cursor.execute(sql1)
                result1 = cursor.fetchone()
                print(result1,'\n')
                cursor.execute(sql2)
                result2=cursor.fetchone()
                print(result2)
                if result1:  # 用户存在，群不存在
                    # 在当前用户的好友列表中插入该用户名
                    sql3 = "INSERT INTO friend_info (user_id, friend_id) VALUES (%s, %s) " % (self.user_id, search_id)
                    sql4="INSERT INTO friend_info (friend_id,user_id ) VALUES (%s, %s)" % (self.user_id, search_id)
                    cursor.execute(sql3)
                    cursor.execute(sql4)
                    db.commit()
                    messagebox.showinfo('添加成功', '添加好友成功')
                    self.add_entry.delete(0, END)
                    self.refresh_friend_list()
                elif result2:   #群存在，用户不存在
                    sql5="SELECT DISTINCT port from group_info where group_id=%s" % search_id
                    cursor.execute(sql5)
                    group_port=cursor.fetchone()[0]
                    #将当前用户加入到群中
                    sql6="insert into group_info values (%s,%s,%s)" % (search_id,self.user_id,group_port)
                    print(sql6)
                    cursor.execute(sql6)
                    db.commit()
                    messagebox.showinfo('加入成功', '加入群聊成功')
                    self.add_entry.delete(0, END)
                    self.refresh_group_list()
                else:
                    messagebox.showerror('error', '请输入正确的id')
                db.close()
            else:
                messagebox.showerror('error', '添加输入不能为空')
        except:
            messagebox.showerror('错误', '用户或群不存在')

    # 好友按钮
    def friend_button(self, friend_id):
        friend_button = Button(self.contact_area, text=friend_id, bg='#F5FFFA', fg='#6495ED', width=33, height=2,
                               command=lambda: self.friend_button_clicked(friend_id))
        self.contact_area.window_create(END, window=friend_button)
        # 创建右键菜单
        menu = tkinter.Menu(self.contact_area, tearoff=0)
        # 添加删除菜单项
        menu.add_command(label="删除好友", command=lambda: self.delete_friend_button_clicked(friend_id))
        # 绑定右键事件
        friend_button.bind("<Button-3>", lambda event: menu.post(event.x_root, event.y_root))
    #获取好友信息
    def friend_info(self):
        db = connect_to_mysql()
        cursor = db.cursor()
        sql1 = 'SELECT COUNT(*) FROM friend_info WHERE user_id = %s' % self.user_id
        sql2 = 'select friend_id from friend_info where user_id=%s' % self.user_id
        cursor.execute(sql1)
        data1 = cursor.fetchone()
        friend_num = int(','.join(str(x) for x in data1))
        cursor.execute(sql2)
        data2 = cursor.fetchall()
        friend_list=[r[0] for r in data2]
        print('好友列表'+str(friend_list))
        print('好友数量'+str(friend_num))
        return friend_num,friend_list
    # 刷新好友列表
    def refresh_friend_list(self):
        # 清空当前好友栏
        self.contact_area.delete('1.0', END)
        # 重新获取好友信息
        friend_num, friend_list = self.friend_info()#返回好友数量和好友id列表
        for i in range(friend_num):
            Thread(target=self.friend_button(friend_list[i]), args=(str(friend_list[i]))).start()# -对每个好友id,启动一个线程调用friend_button方法创建按钮
    # 好友按钮点击事件**************
    def friend_button_clicked(self, friend_id):
        # 检测好友是否还是你的好友
        db = connect_to_mysql()
        cursor = db.cursor()
        # 检查用户名是否存在
        sql1 = "SELECT friend_id FROM friend_info WHERE user_id=%s and friend_id=%s" % (self.user_id, friend_id)
        cursor.execute(sql1)
        result = cursor.fetchone()
        if result:
            # 生成聊天界面
            friend_chatpanel = private_ChatPanel(self.user_id, friend_id)
            friend_chatpanel.run()
        else:
            messagebox.showerror('error', '对方不是你好友')
    # 删除好友按键触发
    def delete_friend_button_clicked(self, friend_id):
        # 连接数据库
        db = connect_to_mysql()
        cursor = db.cursor()
        sql1 = 'delete from friend_info where user_id=%s and friend_id=%s' % (self.user_id, friend_id)  # 单方面删除好友
        sql2 = 'delete from friend_info where user_id=%s and friend_id=%s' % (friend_id, self.user_id)
        cursor.execute(sql1)
        db.commit()
        cursor.execute(sql2)
        db.commit()
        self.refresh_friend_list()

    #创建群聊按钮点击
    def create_group_button_clicked(self):
        pass
        # 获取输入的用户名
        group_id = self.add_entry.get()
        try:
            if group_id:
                # 连接数据库
                db = connect_to_mysql()
                cursor = db.cursor()
                # 数据库搜索群是否存在
                sql1 = "select DISTINCT group_id from group_info where group_id=%s" % group_id
                cursor.execute(sql1)
                result1 = cursor.fetchone()
                if not result1 :  # 群已经存在
                    port=int(random.randint(1,1000000)%65535)
                    # 在当前用户的好友列表中插入该用户名
                    sql2 = "INSERT INTO group_info (group_id, member_id,port) VALUES (%s, %s,%d) " % (group_id, self.user_id,port)
                    cursor.execute(sql2)
                    db.commit()
                    messagebox.showinfo('创建', '创建群成功')
                    self.add_entry.delete(0,END)
                    self.refresh_friend_list()
                else:#群聊已存在
                    messagebox.showerror('错误', '群已经存在')
                db.close()
            else:
                messagebox.showerror('error', '添加输入不能为空')
        except:
            messagebox.showerror('error', '无法创建群')
    # 群聊按钮
    def group_button(self, group_id):
        group_button = Button(self.contact_area, text=group_id, bg='#F5FFFA', fg='#6495ED', width=33, height=2,command=lambda: self.group_button_clicked(group_id))
        self.contact_area.window_create(END, window=group_button)
        # 创建右键菜单
        menu = tkinter.Menu(self.contact_area, tearoff=0)
        # 添加删除菜单项
        menu.add_command(label="删除群聊", command=lambda: self.delete_group_button_clicked(group_id))
        # 绑定右键事件
        group_button.bind("<Button-3>", lambda event: menu.post(event.x_root, event.y_root))
    #获取群聊信息
    def group_info(self):
        db = connect_to_mysql()
        cursor = db.cursor()
        sql1 = 'SELECT group_id FROM group_info WHERE member_id =%s' % self.user_id
        cursor.execute(sql1)
        group_id_list = cursor.fetchall()
        sql2 = 'SELECT COUNT(DISTINCT group_id) AS group_count FROM group_info WHERE member_id =%s' % self.user_id
        cursor.execute(sql2)
        group_num = cursor.fetchone()[0]
        print('群数量' + str(group_num))
        #返回群成员列表和群成员数量
        return group_id_list,group_num
    #群聊按钮点击事件
    def group_button_clicked(self, group_id):
        # 检测是否是群聊成员
        db = connect_to_mysql()
        cursor = db.cursor()
        # 检查用户名是否存在
        sql1 = "SELECT member_id FROM group_info where group_id=%s and member_id=%s" % (group_id[0],self.user_id)
        cursor.execute(sql1)
        result = cursor.fetchone()
        if result:
            # 生成聊天界面
            group_chatpanel = group_ChatPanel(self.user_id, group_id)
            group_chatpanel.run()
        else:
            messagebox.showerror('error', '对方不是你好友')
    #刷新群聊列表
    def refresh_group_list(self):
        # 清空当前栏目
        self.contact_area.delete('1.0', END)
        #获取群聊信息
        group_id_list,group_num=self.group_info()
        print(group_id_list)
        for i in range(group_num):
            Thread(target=self.group_button(group_id_list[i]), args=(str(group_id_list[i]))).start()
    #删除群聊点击事件
    def delete_group_button_clicked(self, group_id):
        # 连接数据库
        db = connect_to_mysql()
        cursor = db.cursor()
        sql1 = 'delete from group_info where member_id=%s and group_id=%s ' % (self.user_id,group_id[0]) # 退群
        cursor.execute(sql1)
        db.commit()
        db.close()
        self.refresh_group_list()

#客户端
class client:
    def __init__(self, user_id, contact_id, chatPanel):
        self.chatPanel=chatPanel
        self.user_id = user_id
        self.contact_id=contact_id
        print('conact_id为：'+str(self.contact_id))
        #连接数据库，获取用户端口
        self.db = connect_to_mysql()
        self.cursor = self.db.cursor()
        sql1 = 'select port from user_info where id=%s' % (self.user_id)
        self.cursor.execute(sql1)
        self.user_port = int(self.cursor.fetchone()[0])
        self.s = socket.socket()#绑定用户socket
        self.s.bind(('127.0.0.1',self.user_port))

    #私聊发信息
    def send_message_to_friend(self, msg):
        # 根据好友id从数据库获取端口号
        sql2 = 'select port from user_info where id=%s' % (self.contact_id)
        print(sql2)
        self.cursor.execute(sql2)
        self.friend_port = int(self.cursor.fetchone()[0])
        print(self.friend_port)
        # 建立socket连接
        self.send_socket = socket.socket()
        self.send_socket.connect(('127.0.0.1', self.friend_port))
        try:
            # 发送消息给好友
            message=str(self.user_id)+','+str(msg)#发送者id和消息内容
            self.send_socket.send(bytes(message,encoding='utf-8'))
            print('消息发送成功')
        except:
            messagebox.showinfo('错误','消息发送出错')
    #群聊发信息
    def send_message_to_group(self, msg):
        # 根据群聊从数据库获取端口号
        sql2 = 'select port from group_info where group_id=%s' % (self.contact_id[0])
        self.cursor.execute(sql2)
        self.group_port = int(self.cursor.fetchone()[0])
        #建立socket连接
        self.send_socket = socket.socket()
        self.send_socket.connect(('127.0.0.1', self.group_port))
        try:
            # 发送消息给服务器
            message=str(self.user_id)+','+str(msg)#发送者id和消息内容
            self.send_socket.send(bytes(message, encoding='utf-8'))
            print('消息发送成功')
        except:
            messagebox.showinfo('错误', '消息发送出错')

    # 接收私聊发来的信息
    def recv_private_message(self):
        self.s.listen(5)
        while True:
            conn, addr = self.s.accept()
            # 接收消息
            t = strftime("%Y-%m-%d %H:%M:%S", localtime())
            message = conn.recv(1024).decode()
            if not message:
                continue
            send_user_id = message.split(',')[0]  # 发送者id
            msg = message.split(',')[1]  # 消息内容
            self.chatPanel.chat_scroll_box.insert(END, str(t) + '\n' + str(send_user_id) + '\t:' + str(msg) + '\n')
    #接收群聊信息
    def recv_group_message(self):
        self.s.listen(5)
        while True:
            conn, addr = self.s.accept()
            # 接收消息
            t = strftime("%Y-%m-%d %H:%M:%S", localtime())
            message = conn.recv(1024).decode()
            if not message:
                continue
            send_user_id=message.split(',')[0]#发送者id
            msg=message.split(',')[1]#消息内容
            self.chatPanel.chat_scroll_box.insert(END, str(t) + '\n' + str(send_user_id) + '\t:' + str(msg) + '\n')
    #断开与服务器的连接
    def close_connect(self):
        self.s.close()
        self.db.close()#关闭数据库连接
        print('客户端与服务器断开连接！！！\n')

#一对一聊天界面
class private_ChatPanel:
    def run(self):
        threading.Thread(target=self.client.recv_private_message).start()  # 接收私聊信息线程开启
        print('接收信息线程启动!\n')
        self.root.mainloop()

    def __init__(self,user_id,friend_id):
        self.root = Tk()
        self.client=client(user_id,friend_id,self)
        self.user_id = user_id
        self.friend_id = friend_id

        # 标题
        self.root.title('登录用户: '+str(self.user_id)+'聊天对象:'+str(self.friend_id))
        self.root.geometry('700x600+400+50')
        self.headtitle = Canvas(self.root, bg='skyblue')
        self.headtitle.place(x=5, y=5, heigh=40, width=690)

        #好友名字标签
        titlenamelable=Label(self.headtitle,text=self.friend_id,bg='skyblue')
        titlenamelable.place(x=50,y=5, heigh=30, width=300)
        #聊天信息区域
        self.chat_area = Canvas(self.root, bg='orange')
        self.chat_area.place(x=5, y=45, heigh=400, width=690)
        #输入区域
        self.input_area = Canvas(self.root, bg='pink')
        self.input_area.place(x=5, y=445, heigh=150, width=690)

        #发送按钮
        send_button=Button(self.input_area, text='发送',command=self.send_button_clicked) #待确定
        send_button.place(x=600, y=110, heigh=30, width=80)
        #关闭按钮
        closebutton=Button(self.input_area, text='关闭', command=self.close_button_clicked)#绑定按键功能为摧毁当前界面
        closebutton.place(x=510, y=110, heigh=30, width=80)

        #聊天信息框
        self.chat_scroll_box=scrolledtext.ScrolledText(self.chat_area, font=("宋体", 16, "normal"))
        self.chat_scroll_box.place(x=5, y=5, heigh=390, width=680)

        # 信息输入框
        self.input_chat_box = scrolledtext.ScrolledText(self.input_area, font=("宋体", 16, "normal"))
        self.input_chat_box.place(x=5, y=5, heigh=100, width=680)

    #关闭按钮点击事件
    def close_button_clicked(self):
        self.root.destroy()
        self.client.close_connect()

    #发送按钮点击事件
    def send_button_clicked(self):
        # 获取输入信息
        t = strftime("%Y-%m-%d %H:%M:%S", localtime())
        msg = self.input_chat_box.get('0.0', END)
        self.input_chat_box.delete('0.0', END)
        # 若不为空将消息发送
        if msg:
            self.client.send_message_to_friend(msg)
        else:
            messagebox.showinfo('提示','消息不能为空')
        print('发送按钮被点击了')
        # 将输入信息贴到聊天记录中
        self.chat_scroll_box.insert(END, str(t) + '\n' + str('我:  ') + str(msg)+'\n')

#群聊界面
class group_ChatPanel:
    def run(self):
        threading.Thread(target=self.client.recv_group_message).start()  # 接收群聊信息线程开启
        print('接收信息线程启动!\n')
        self.root.mainloop()

    def __init__(self,user_id,group_id):
        self.root = Tk()
        self.client=client(user_id,group_id,self)
        self.user_id = user_id
        self.group_id = group_id

        # 标题
        self.root.title('登录用户: '+str(self.user_id)+' 群聊:'+str(self.group_id[0]))
        self.root.geometry('700x600+400+50')
        self.headtitle = Canvas(self.root, bg='skyblue')
        self.headtitle.place(x=5, y=5, heigh=40, width=690)

        #好友名字标签
        titlenamelable=Label(self.headtitle,text=self.group_id,bg='skyblue')
        titlenamelable.place(x=50,y=5, heigh=30, width=300)
        #聊天信息区域
        self.chat_area = Canvas(self.root, bg='orange')
        self.chat_area.place(x=5, y=45, heigh=400, width=690)
        #输入区域
        self.input_area = Canvas(self.root, bg='pink')
        self.input_area.place(x=5, y=445, heigh=150, width=690)

        #发送按钮
        send_button=Button(self.input_area, text='发送',command=self.send_button_clicked) #待确定
        send_button.place(x=600, y=110, heigh=30, width=80)
        #关闭按钮
        closebutton=Button(self.input_area, text='关闭', command=self.close_button_clicked)#绑定按键功能为摧毁当前界面
        closebutton.place(x=510, y=110, heigh=30, width=80)

        #聊天信息框
        self.chat_scroll_box=scrolledtext.ScrolledText(self.chat_area, font=("宋体", 16, "normal"))
        self.chat_scroll_box.place(x=5, y=5, heigh=390, width=680)

        # 信息输入框
        self.input_chat_box = scrolledtext.ScrolledText(self.input_area, font=("宋体", 16, "normal"))
        self.input_chat_box.place(x=5, y=5, heigh=100, width=680)

    #关闭按钮点击事件
    def close_button_clicked(self):
        self.root.destroy()
        self.client.close_connect()

    #发送按钮点击事件
    def send_button_clicked(self):
        # 获取输入信息
        t = strftime("%Y-%m-%d %H:%M:%S", localtime())
        msg = self.input_chat_box.get('0.0', END)
        self.input_chat_box.delete('0.0', END)
        # 将消息发送
        message=str(msg)
        self.client.send_message_to_group(message)
        print('发送按钮被点击了')
        # 将输入信息贴到聊天记录中
        self.chat_scroll_box.insert(END, str(t) + '\n' + str('我: ') + str(msg)+'\n')

if __name__ == '__main__':

    start=LoginPanel()    #user_id
    start.run()
    # mainpanel=MainPanel(33333333)     #user_id
    # mainpanel.run()

    #chatpanel=ChatPanel()  #user_id,friend_id(1454991831,485508446)
    #chatpanel.run()

    # register=RegisterPanel()
    # register.run()


