# coding=utf-8
# author@alingse
# 2016.10.09

import getpass

from panshell.base import FS
from pan import Pan


class baiduFS(FS):
    """baidu yunpan (百度云盘) 文件系统"""

    name = 'baidu'

    def __init__(self, name='baidu', **kwargs):
        super(baiduFS, self).__init__(name, **kwargs)

        self._pan_map = {}
        self._pan_id = 0
        self._current_pan_id = self._pan_id
        # set default new pan
        self._new_pan()

    @property
    def prompt(self):
        return '{}-(pan-{})-sh$>'.format(self.name, self.current_pan.name)

    def _new_pan(self):
        self._current_pan_id = self._pan_id + 1
        self._pan_map[self._current_pan_id] = Pan(self._current_pan_id)
        self._pan_id += 1

    @property
    def current_pan(self):
        if not self._current_pan_id:
            return None
        return self._pan_map[self._current_pan_id]

    def select(self, pan_id):
        if pan_id not in self._pan_map:
            return False
        self._current_pan_id = pan_id

    def do_pan(self, line):
        if not line.strip():
            return self._new_pan()
        else:
            return self.select(int(line.strip()))

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
        self.current_pan.new_account(username, password)
        self.current_pan.login()
        print('login', self.current_pan.login_status)
        return

    def do_ls(self, line):
        """
        ls .
        ls path
        """
        self.current_pan.list()

    def do_exit(self, line):
        for k in self._pan_map:
            p = self._pan_map[k]
            p.exit()

        self._current_pan_id = self._pan_id = 0
        self._pan_map = {}
