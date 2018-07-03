#!/usr/bin/python
# -*- coding: UTF-8 -*-
# * Created by .
# * Date: 2017/1/10 0004
# * Time: 下午 2:32
# * Project: PYTHON STUDY
# * Power: DATABASE
import pymysql

class Con_mysql():
    # result = []
    # 打开数据库连接（ip/数据库用户名/登录密码/数据库名）
    def __init__(self,Host,Root,Pwd,Databas):
        self.Host = Host
        self.Root =Root
        self.Pwd =Pwd
        self.Databas = Databas
    def query(self,sql_query):
        db = pymysql.connect(self.Host, self.Root,self.Pwd, self.Databas )
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = db.cursor()
        # SQL 插入语句
        sql = sql_query
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
            result= cursor.fetchall()
        except:
            # 如果发生错误则回滚
            db.rollback()

        # 关闭数据库连接
        db.close()
        return result

