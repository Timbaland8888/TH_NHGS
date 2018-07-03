#! /usr/bin/env python
# -*- coding: UTF-8 -*-
from pywinauto import Application,application,findwindows
import time,os
class Authentication():
    # app = Application().start('notepad.exe')
    #本地添加远程连接的凭证命令：cmdkey /add: 172.16.62.15 /user:administrator /pass:123456
    def cmdkey_pc(self,host):
        cmd_pass = """cmdkey /add: %s /user:administrator /pass:123456""" %(host)
        try:
            os.popen(cmd_pass)
        except Exception as e:
            print (e)
            print ("添加凭证失败")

# app = application.Application().start("mstsc  /console /v: 192.168.24.237:3389")

# app.connect(u"远程桌面连接")
# time.sleep(1)
# w_handle = findwindows.find_windows(title=u'远程桌面连接', class_name='#32770')[0]
# aduc_window = app.window_(handle=w_handle)
# aduc_window.print_control_identifiers()
# b = aduc_window.child_window(title=u"连接(&N)", class_name="Button")
# b.print_control_identifiers()
# tip = u'不再询问我是否连接到此计算机(&O)'
# OK = u'取消(&C)'
# OK = u'连接(&N)"'
# aduc_window[tip].Check()
# aduc_window[OK].Click()

# app = Application().start('notepad.exe')
#本地添加远程连接的凭证命令：cmdkey /add: 172.16.62.15 /user:administrator /pass:123456
# cmd_pass = """cmdkey /add: 172.16.62.15 /user:win7 /pass:123456"""
# try:
#     os.popen(cmd_pass)
#     print('添加凭据成功')
# except Exception,e:
#     print e+"添加凭证失败"
    def conect_pc(self,host):
        try:
            play = "mstsc  /console /v: %s:3389" %(host)
            app = application.Application(backend='uia').start(play)

            #一定要1秒中的停留窗口的时间
            time.sleep(1)
            w_handle = findwindows.find_windows(title=u'远程桌面连接', class_name='#32770')[0]
            aduc_window = app.window_(handle=w_handle)
            # aduc_window.print_control_identifiers()

            # b = aduc_window.child_window(title=u'是(&Y)', class_name="Button")
            # b.print_control_identifiers()
            tip = u'不再询问我是否连接到此计算机(&D)'
            # OK = u'取消(&C)'
            OK = u'是(&Y)'
            # aduc_window[tip].Check()
            #模拟点击操作
            aduc_window[OK].Click()

        except Exception as e:
            print (e)

