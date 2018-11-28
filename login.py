#!/usr/bin/env python3

import os
os.environ["DJANGO_SETTINGS_MODULE"] = 'cmdb.settings'
import django
import re
django.setup()

from django.db.models import Q
from users.models import CustomUser
from accounts.auth_api import has_auth
from assets.models import Server,Project
from authorize.models import AuthNode,AuthGroupNode

# 显示错误装饰器
def showErr(func):
    def wrapper(self,*args,**kwargs):
        res = func(self,*args,**kwargs)
        if res != None:
            if res[0] > 10040:
                print("错误%d: %s" % (res[0],res[1]))
        return func(self,*args,**kwargs)
    return wrapper

class base(object):

    def __init__(self,username):
        self.username = username

    @showErr
    def errorCode(self,code,msg=None):
        codeDict = {
            10040:'成功',
            10041:'用户不可用',
            10042:'主机编号错误',
            10043:'主机连接错误',
            10044:'IP地址不存在',
            10045:'用户名不存在',
        }
        if not msg: msg = codeDict[code]
        codeDetail = [code,msg]
        return codeDetail

class CMDBSSH(base):
    def __init__(self,username):
        super(CMDBSSH,self).__init__(username)
        self.username = username

        self.user_is_active = self.__userIsActive() # 用户是否合法
        self.logo = self.__getLogo()


    def __userIsActive(self):
        '''
        判断用户是否可用
        :return:
        '''
        try:
            userObj = CustomUser.objects.get(username=self.username)
            if userObj.is_active and userObj.is_staff:
                return self.errorCode(10040)
            else:
                return self.errorCode(10041)
        except:
            return self.errorCode(10045)

    def showWelcome(self):
        '''
        显示欢迎信息
        :return:
        '''
        print(self.logo)    # 打印logo
        if self.user_is_active[0] == 10040: # 用户合法打印欢迎信息
            print("Welcome:  %s" % self.username)
            print("You can visit the following host:\n")
            self.__displayHost()
        else:
            print("用户信息错误!")
            raise ("user not allowed")

    def __displayHost(self):
        '''
        显示主机列表
        :return:
        '''
        ip_num = 1
        for pName,sList in self.__proHostDetail():
            sNum = len(sList)
            print("[%s] (主机数量:%s)" % (pName,sNum))
            for si in range(sNum):
                end = "\n" if (si+1)%4==0 else "\t\t"
                ipAddr = sList[si]
                print("[%3d] %12s" % (ip_num,ipAddr),end=end)
                ip_num += 1
                if si == sNum-1:print('\n')

    def __sortHostList(self):
        '''
        主机列表排序
        :return:
        '''
        host_list = []
        for i in self.__proHostDetail():
            for h in i[1]:
                host_list.append(h)
        return host_list

    def __proHostDetail(self):
        '''
        获取分组详细信息
        :return:
        '''
        project_server_dict = {}
        userObj = CustomUser.objects.get(username=self.username)
        if userObj.is_superuser:
            server_list = Server.objects.filter(is_active=True)
        else:
            server_list = Server.objects.filter(Q(authnode_node__user_name=userObj.uuid)|Q(authdepnode_node__department_name=userObj.department))
        for s in server_list:
            if len(s.project.all()) == 0:
                if project_server_dict.get('未分组'):
                    project_server_dict['未分组'].append(s.ip)
                else:
                    project_server_dict.setdefault('未分组',[s.ip])
                continue
            for p in s.project.all():
                if project_server_dict.get(p.name):
                    project_server_dict[p.name].append(s.ip)
                else:
                    project_server_dict.setdefault(p.name,[s.ip])
        return (sorted(project_server_dict.items(),key=lambda item:item[0]))

    def __getLogo(self):
        logo = """
 #######                   ####
 #######                  ##  ##
    #                     ##   #
    #     #####   #####   ##       #   #    ####
    #         #   #   #    #####   #   #   #    #
    #      ####   #   #        #   #   #   #    #
    #     #   #   #   #   #    #   #   #   #    #
    #     #   #   #   #   ##   #   #   #   ##  ##
    #     #####   #   #    ####    #####    ####

    """
        return logo



    def ssh(self,ip):
        try:
            print('正在登陆 %s...' % ip )
            os.system('ssh root@%s' % ip)
            os.system('clear')
            self.showWelcome()
        except:
            return self.errorCode(10043)

    def command(self):

        cmd = input("输入服务器id连接到服务器,输入help或者h查看附加功能帮助信息:")
        ip_comp = re.compile(r'^(\d{1,3}\.){3}\d{1,3}$')    # IP匹配
        is_digital = re.compile(r'^\d+$')               # 数字匹配
        search_comp = re.compile(r'^[s|S] (?P<ip>.+)$')    # 模糊匹配
        regex_serach = re.compile(r'^rs (?P<reg>.+)$')  # 正则模糊匹配

        host_list = self.__sortHostList()

        # 判断编号
        if is_digital.match(cmd):
            ServerNum = int(cmd)
            if 0<ServerNum<=len(host_list):
                sIp = host_list[ServerNum-1]
                self.ssh(sIp)
            else:
                return self.errorCode(10042)
        # 判断IP地址
        elif ip_comp.match(cmd):
            if cmd in host_list:
                self.ssh(cmd)
            else:
                return self.errorCode(10044)

        # 判断搜索
        elif search_comp.match(cmd):
            key_word = search_comp.match(cmd).groupdict()['ip']
            search_result = []
            for i in host_list:
                if key_word in i:
                    search_result.append(i)
            if len(search_result) == 1:
                self.ssh(search_result[0])
            elif len(search_result) > 1:
                print('共匹配 %d 台主机' % len(search_result))
                for i in range(len(search_result)):
                    end = '\t\t' if (i+1)%4 else "\n"
                    print('[%3d] %12s' % (host_list.index(search_result[i])+1,search_result[i]),end=end)
                print('')
            else:
                print("没有匹配到任何主机")
        elif regex_serach.match(cmd):
            regex = regex_serach.match(cmd).groupdict()['reg']
            search_result = []
            for i in host_list:
                if re.findall(regex,i):
                    search_result.append(i)
            if len(search_result) == 1:
                self.ssh(search_result[0])
            elif len(search_result) > 1:
                print('共匹配 %d 台主机' % len(search_result))
                for i in range(len(search_result)):
                    end = '\t\t' if (i+1)%4 else "\n"
                    print('[%3d] %12s' % (host_list.index(search_result[i])+1,search_result[i]),end=end)
                print('')
            else:
                print("没有匹配到任何主机")

        else:
            self.__showHelp()

    def __showHelp(self):
        help_msg = '''
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+  h | help   :  查看帮助信息                                                   +
+  f | flush  :  清除屏幕                                                      +
+  s          :  根据ip字段搜索服务器，如输入"s 118"搜索ip字段包含118的服务器        +
+  rs         :  根据ip字段正则匹配服务器，如输入"s 118$"搜索ip字段以118结束的服务器  +
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''
        print(help_msg)

    def run(self):
        self.showWelcome()
        while 1:
            self.command()








if __name__ == '__main__':
    username = 'yantao'
    cmdb = CMDBSSH(username=username)
    cmdb.run()
    # print(d.getProjects())
    # print(d.getHostList())
    # print(d.getLogo())