#!/usr/bin/evn python
# -*- encoding:utf-8 -*-
# function: connect exsi server api  for restart vm
# date:2018-12-14
# Arthor:Timbaland
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

_Arthur_ = 'Timbaland'
import pysphere, pymysql
from pysphere import VIServer
import logging
import ssl
import datetime, os, time
import ConfigParser, codecs

# 全局取消证书验证,忽略连接VSPHERE时提示证书验证
ssl._create_default_https_context = ssl._create_unverified_context

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class VcentTools(object):
    def __init__(self, host_ip, user, password):
        self.host_ip = host_ip
        self.user = user
        self.password = password

    # 可以连接esxi主机，也可以连接vcenter

    def _connect(self):

        server_obj = VIServer()

    def esxi_version(self):
        server_obj = VIServer()
        try:
            server_obj.connect(self.host_ip, self.user, self.password)
            servertype, version = server_obj.get_server_type(), server_obj.get_api_version()
            server_obj.disconnect()
            return servertype, version
        except Exception as  e:
            print e

    def vm_status(self, vm_name):

        server_obj = VIServer()
        try:
            server_obj.connect(self.host_ip, self.user, self.password)
            # servertype, version = server_obj.get_server_type(),server_obj.get_api_version()


        except Exception as  e:
            print e

        # 通过名称获取vm的实例
        vm = server_obj.get_vm_by_name(vm_name)
        if vm.is_powered_off() == False:
            server_obj.disconnect()
            return 1

        if vm.is_powered_off() == True:
            server_obj.disconnect()
            return 0
        return u"未知状态"

    def vmaction(self, vm_name, vm_hz):

        server_obj = VIServer()
        try:
            server_obj.connect(self.host_ip, self.user, self.password)
        except Exception as  e:
            print e

        # 通过名称获取vm的实例
        try:
            vm = server_obj.get_vm_by_name(vm_name)
        except Exception as e:
            return 0
        if vm.is_powered_off() == False:
            try:
                vm.reset()
                # print (type(int(vm_hz)))
                for i in range(1, int(vm_hz)):
                    print u'虚拟机%s 正在重置中。。。。，请等待注册\n' % (vm_name)
                    time.sleep(1)
                print u'重置完成'
                server_obj.disconnect()

                return 1
            except Exception as e:
                print e

        if vm.is_powered_off() == True:
            vm.power_on()
            print u'虚拟机%s 正在开机中。。。。' % (vm_name)
            server_obj.disconnect()
            return 2


class Class_VM(object):
    def __init__(self, host, user, pwd, port, db, charset):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.port = port
        self.db = db
        self.charset = charset

    # 获取教室里面的虚拟机信息
    def get_vmname(self, query_sql):
        try:
            # 连接mysql数据库参数字段
            con = None
            db = pymysql.connect(host=self.host, user=self.user, passwd=self.pwd, db=self.db, port=self.port,
                                 charset=self.charset)
            cursor = db.cursor()
            vmlist = []
            cursor.execute(query_sql)
            result = cursor.fetchall()
            # 获取教室云桌面数量
            vm_count = len(result)
            print unicode('教室云桌面虚拟机数量共{0}台'.format(vm_count), 'utf-8')

            # print len(cursor.fetchall())
            # cursor.execute(query_vm)
            for vm_id in range(0, vm_count, 1):
                # print result[vm_id][0]
                # print result[vm_id][1]
                vmlist.append(result[vm_id][0])
                # print result[vm_id][0]

            # print type(cursor.fetchall()[0])

            db.commit()

        except ValueError:
            db.roolback
            print 'error'
        # 关闭游标和mysql数据库连接
        cursor.close()
        db.close()
        return vmlist


if __name__ == '__main__':
    cf = ConfigParser.ConfigParser()
    # cf.read('config.ini',encoding="utf-8")
    cf.readfp(codecs.open('config.ini', "r", "utf-8-sig"))
    # print cf.get('vm_retime','set_retime')
    # print type(cf.get('vc','vc_ip'))
    # 连接vsphere
    # print cf.get('vc','vc_ip'),cf.get('vc','vc_acount'),cf.get('vc','vc_pwd')
    obj1 = VcentTools(cf.get('vc1', 'vc_ip'), cf.get('vc1', 'vc_acount'), cf.get('vc1', 'vc_pwd'))
    obj2 = VcentTools(cf.get('vc2', 'vc_ip'), cf.get('vc2', 'vc_acount'), cf.get('vc2', 'vc_pwd'))
    obj3 = VcentTools(cf.get('vc3', 'vc_ip'), cf.get('vc3', 'vc_acount'), cf.get('vc3', 'vc_pwd'))
    obj4 = VcentTools(cf.get('vc4', 'vc_ip'), cf.get('vc4', 'vc_acount'), cf.get('vc4', 'vc_pwd'))
    # obj = VcentTools('10.22.14.130', 'administrator@vsphere.local', '1qaz@WSX')
    # print obj.host_ip,obj.password,obj.user,obj.esxi_version()
    # 查询教室虚拟机
    query_vm = '''  SELECT  b.vm_name 
                    from hj_dg a 
                    INNER JOIN hj_vm b on a.id = b.dg_id 
                    WHERE b.vm_type = 1 and b.vm_name not like "webapp%" 
                    union 
                    SELECT vm_name 
                    from hj_vm
                    WHERE vm_name LIKE "WN%" OR vm_name LIKE "VT%" and del_flag=0 '''
    # 查询虚拟机信息
    p = Class_VM(cf.get('hj_db', 'db_host'), cf.get('hj_db', 'db_user'), cf.get('hj_db', 'db_pwd'),
                 cf.getint('hj_db', 'db_port'), cf.get('hj_db', 'db'), 'utf8')
    # print p.get_vmname(query_vm)[0]
    # 获取当前时间
    now_date = datetime.datetime.now().strftime('%H:%M')
    # time.sleep(10)
    # base_dir = os.path.dirname(__file__)
    # path = os.path.join(base_dir, 'config.ini')
    # # print path
    # print type(now_date)
    # 自定义重启时间
    # # set_retime = ['01:30', '01:31']
    # settime = []
    # with open(path,'r') as  f:
    #      settime = f.readlines()
    # t = settime[1].split('=')[1].split(',')
    # m = []
    # for i in t:
    #      m.append(i.strip())
    #
    # # print m

    while True:

        if datetime.datetime.now().strftime('%H:%M') == cf.get('vm_retime', 'set_retime'):
            for vmname in p.get_vmname(query_vm):
                if obj1.vmaction(vmname, cf.get('vm_hz', 'vm_hz')) == 0:
                    print 'is not exsit %s' % (cf.get('vc1', 'vc_ip'))
                if obj2.vmaction(vmname, cf.get('vm_hz', 'vm_hz')) == 0:
                    print 'is not exsit %s' % (cf.get('vc2', 'vc_ip'))
                if obj3.vmaction(vmname, cf.get('vm_hz', 'vm_hz')) == 0:
                    print 'is not exsit %s' % (cf.get('vc3', 'vc_ip'))
                if obj4.vmaction(vmname, cf.get('vm_hz', 'vm_hz')) == 0:
                    print 'is not exsit %s' % (cf.get('vc4', 'vc_ip'))

                logger.info(u'正在重置%s' % (vmname))
                # time.sleep(10)
        nowdate = datetime.datetime.now().strftime
        logger.info(u'现在时间%s,还未到才重置时间%s 请等待重置' % (now_date, cf.get('vm_retime', 'set_retime')))
        # 检查是否有关机的虚拟机
        # for  vmname in p.get_vmname(query_vm):
        #     # t = datetime.datetime.now().strftime('%H:%M')
        #
        #     if datetime.datetime.now().strftime('%H:%M') == cf.get('vm_retime','set_retime'):
        #         for vmname in p.get_vmname(query_vm):
        #             obj.vmaction(vmname,cf.get('vm_hz','vm_hz'))
        #             logger.info(u'正在重置%s' % (vmname))
        #             # time.sleep(10)
        #     if obj.vm_status(vmname) == 0:
        #         obj.vmaction(vmname,cf.get('vm_hz','vm_hz'))
        #         logger.info(u'%s已经关机。。。。' %(vmname))
        #     else:
        #         logger.info(u'虚拟机%s正在运行,未到重置时间：%s'%(vmname,unicode(cf.get('vm_retime','set_retime'))))

        time.sleep(1)
