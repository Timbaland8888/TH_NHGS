#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')
from tkinter import *
from tkinter.messagebox import *
from PIL import Image,ImageTk
from con_mysql import Con_mysql
from mstsc_rdp import Authentication

class LoginPage(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.username = StringVar()
        self.password = StringVar()
        self.pack()
        self.createForm()

    def createForm(self):
        Label(self,bg='#B9D3EE',fg='red').grid(row=0, stick=W, pady=10)
        Label(self,bg='#B9D3EE', text='学号: ').grid(row=1, stick=W, pady=10)
        Entry(self, textvariable=self.username).grid(row=1, column=1, stick=E)
        Label(self,bg='#B9D3EE', text='密码: ').grid(row=2, stick=W, pady=10)
        Entry(self, textvariable=self.password, show='*').grid(row=2, column=1, stick=E)
        Button(self,bg='#B03060', text='登陆', command=self.loginCheck).grid(row=3, stick=W, pady=10)
        Button(self,bg='#B03060',  text='退出', command=self.quit).grid(row=3, column=1, stick=E)

    def loginCheck(self):
        name = self.username.get()
        secret = self.password.get()

        if name in students_id and secret in students_id and name == secret :
            host = new_id[name]
            print (host)
            print  (type(host))
            print ("login success")
            do_to = Authentication()
            do_to.cmdkey_pc(host)
            # self.destroy()
            # secret.MainPage()
            do_to.conect_pc(host)
            self.quit()
        else:
            showinfo(title='错误', message='学号或密码错误！')
            # print('账号或密码错误！')

#获取学生信息
sql = """select * from student_info """
try:
    con = Con_mysql('localhost','root','123456','nh_gs')
    result = con.query(sql)
    #学号集合
    students_id =[]
    host_ip =[]
    #总人数
    students  = len(result)
    for id  in range(students):
        students_id.append(str(result[id][0]))
        host_ip.append(str(result[id][6]))
    # print type(students_id[1])
    new_id = dict(zip(students_id, host_ip))
except:
    print ('请检查数据库服务器网络')
# print students_id
# print host_ip

root = Tk()
root.title('汇捷桌面')
root.iconbitmap('2.ico')
# image = Image.open('1.jpg')
# im = ImageTk.PhotoImage(image)
# w = im.width()
# h = im.height()
# root.geometry('%dx%d+0+0' % (w,h))
# background_label = Label(root, image=im)
# background_label.place(x=0, y=0, relwidth=1, relheight=1)
width = 320
height = 240
Label(root,bg='#B9D3EE',text="南华工商职业技术学院 版本：V1.0",fg='#27408B').pack(side = "bottom")
screenwidth = root.winfo_screenwidth()
screenheight = root.winfo_screenheight()
alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
root.geometry(alignstr)  # 居中对齐
root['background']='#B9D3EE'
page1 = LoginPage()
page1['background']='#B9D3EE'
root.mainloop()
