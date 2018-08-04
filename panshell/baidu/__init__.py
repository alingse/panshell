# coding=utf-8
# author@alingse
# 2016.10.09

import getpass
import requests

from panshell.base import FS

from login import login


class baiduFS(FS):
    """baidu yunpan (百度云盘) 文件系统"""

    name = 'baidu'

    def __init__(self, **kwargs):
        name = kwargs.pop('name', self.name)
        super(baiduFS, self).__init__(name, **kwargs)

        self.session = requests.Session()
        self.is_login = None

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
        status = login(self.session, username, password)
        self.is_login = status
        print('login', status)
        return

    def do_ls(self, line):
        """
        ls .
        ls path
        """
        print(self.name, 'do---')

    def do_exit(self, line):
        print('exit this baidu')
