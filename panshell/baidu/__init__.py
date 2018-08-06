# coding=utf-8
# author@alingse
# 2016.10.09

import getpass

from panshell.base import FS
from pan import Pan


class baiduFS(FS):
    """baidu yunpan (百度云盘) 文件系统"""

    name = 'baidu'

    def __init__(self, **kwargs):
        name = kwargs.pop('name', self.name)
        super(baiduFS, self).__init__(name, **kwargs)

        self.pan = Pan(name='<new>')

    def do_login(self, line):
        """
        login [username]
        """
        username = line.strip()
        if username == '':
            username = raw_input('username:')
        if username == '':
            print('not login')
            return

        password = getpass.getpass()
        self.pan.new_account(username, password)
        self.pan.login()
        print('login', self.pan.status)
        return

    def do_ls(self, line):
        """
        ls .
        ls path
        """
        print(self.name, 'do---')

    def do_exit(self, line):
        print('exit this baidu')
