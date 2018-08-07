# coding=utf-8


class FS(object):
    """filesystem Base Class"""

    def __init__(self, name, **kwargs):
        self.name = name

    @property
    def prompt(self):
        return '{}-sh$>'.format(self.name)

    def do_exit(self, line):
        pass
