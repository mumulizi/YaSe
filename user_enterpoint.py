#!/usr/bin/env python
#_*_coding:utf-8_*_
#__author__="lihongxing"

import getpass,os
from django.contrib.auth import authenticate
import subprocess
import hashlib,time

class UserPortal(object):
    '''命令行端交互入口'''
    def __init__(self):
        self.user = None


    def user_auth(self):
        '''完成用户命令行交互'''
        retry_count = 0
        while retry_count < 3:
            username = raw_input("请输入用户名:").strip()
            if len(username) == 0:
                continue
            password = getpass.getpass('请输入密码:').strip()
            if len(password) == 0:
                print("密码不能为空")
            user = authenticate(username=username, password=password) # 用户名密码验证
            if user:
                self.user = user
                # print("welcome login")
                return
            else:
                print("用户名或密码错误")

            retry_count += 1

        else:
            exit('Too many attempts.')


    def interactive(self):
        '''交互函数'''

        self.user_auth()
        if self.user: # 表示认证成功
            flag = False
            while not flag:
                bind_hosts = self.user.bind_hosts.select_related().count() # 关联的主机
                host_groups = self.user.host_groups.all() # 所有属组
                # print(bind_hosts,host_groups)
                for index, host_group in enumerate(host_groups):
                    print("%s. %s[%s]" % (index, host_group.name, host_group.bind_hosts.all().count()))

                print("%s. 未分组主机[%s]" % (index+1,bind_hosts))

                user_input = raw_input("请选择组>>> ").strip()
                if len(user_input) == 0:
                    continue
                if user_input.isdigit(): # 判断是不是数字
                    user_input = int(user_input)
                    selected_hostgroup = None
                    if user_input >= 0 and user_input < host_groups.count():
                        selected_hostgroup = host_groups[user_input]

                    elif user_input == host_groups.count(): # 表示选中了未分组的属组
                        selected_hostgroup = self.user
                        # 之所以可以这样，是因为self.user里也有一个bind_hosts,跟HostGroup.bind_hosts指向的表一样
                    else:
                        print("无效的主机")
                        continue

                    select_hosts = selected_hostgroup.bind_hosts.all()
                    while True:
                        for index, bind_host in enumerate(select_hosts):
                            print("%s %s(%s user:%s" % (index,
                                                        bind_host.host.hostname,
                                                        bind_host.host.ip_addr,
                                                        bind_host.host_user.username
                                                        ))

                        user_host_input = raw_input("请选择主机>>>").strip()
                        if len(user_host_input) == 0:
                            continue
                        if user_host_input.isdigit():
                            user_host_input = int(user_host_input)
                            if user_host_input >= 0 and user_host_input < select_hosts.count():
                                selected_bindhost = select_hosts[user_host_input]
                                print("登陆该主机:",selected_bindhost.host.hostname)
                                md5_str = hashlib.md5(str(time.time()).encode()).hexdigest()

                                login_cmd = 'sshpass  -p {password} /usr/local/ssh7/bin/ssh {user}@{ip_addr}  -o "StrictHostKeyChecking no" -Z {md5_str}'.format(
                                    password=selected_bindhost.host_user.password,
                                    user=selected_bindhost.host_user.username,
                                    ip_addr=selected_bindhost.host.ip_addr,
                                    md5_str=md5_str)

                                print(login_cmd)

                                session_tracker_script = settings.SESSION_TRACKER_SCRIPT
                                tracker_obj = subprocess.Popen("%s %s" %(session_tracker_script,md5_str),shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,cwd=settings.BASE_DIR)

                                # 创建日志数据
                                models.SessionLog.objects.create(user=self.user,bind_host=selected_bindhost,session_tag=md5_str)


                                ssh_instance = subprocess.call(login_cmd, shell=True)
                                print("session tracekr",tracker_obj.stdout.read(),tracker_obj.stderr.read())

                        if user_host_input == 'q':
                            break

if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "YaSe.settings")
    import django
    django.setup()
    from django.conf import settings
    from audit import models
    portal = UserPortal()
    portal.interactive()
