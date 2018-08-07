# coding=utf-8
# author@alingse
# 2016.12.14

import requests

from account import BaiduAccount


class Pan(object):

    def __init__(self, name='default'):
        self._name = name
        self.session = requests.Session()
        self.account = None
        self.context = None

    def new_account(self, username, password):
        self.account = BaiduAccount(username, password)
        self.account.attach_session(self.session)

    def login(self):
        self.account.login()

    def logout(self):
        self.account = None
        self.session = requests.Session()

    @property
    def name(self):
        if not self.account:
            return self._name
        name = '{}.{}'.format(self._name, self.account.username)
        if self.login_status:
            return name + '[login]'
        return name

    @property
    def login_status(self):
        if self.account:
            return self.account.login_status
        return False

    def list(self):
        if not self.login_status:
            print('need login!')
        print('do account ls')

    def exit(self):
        self.logout()
        print('pan {} exit.'.format(self.name))
