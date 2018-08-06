# coding=utf-8
# author@alingse
# 2016.12.14

import requests

from account import BaiduAccount


class Pan(object):

    def __init__(self, name='default'):
        self.name = name
        self.session = requests.Session()
        self.account = None
        self.status = None
        self.context = None

    def new_account(self, username, password):
        self.account = BaiduAccount(username, password)
        self.account.attach_session(self.session)

    def login(self):
        self.account.login()
        self.status = 'login'

    def logout(self):
        self.account = None
        self.session = requests.Session()
