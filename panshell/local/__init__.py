# coding=utf-8
# author@alingse
# 2016.10.09

from panshell.base import FS


class localFS(FS):

    name = 'local'

    def __init__(self, **kwargs):
        name = kwargs.pop('name', self.name)
        super(localFS, self).__init__(name, **kwargs)

    def do_ls(self, line):
        """
        "localFS"
        `ls `
        `ls path`
        """
        print(self.name, 'ls')

    def do_exit(self, line):
        print('exit this local')
