# coding=utf-8
from __future__ import print_function

import cmd
import inspect
import sys

from panshell.base import FS


class Shell(cmd.Cmd):

    def __init__(self):
        cmd.Cmd.__init__(self)

        self.stack = []
        self.fsmap = {}
        self.fs = None

        self._funcs = []
        self._keywords = ['use', 'exit']

    @property
    def prompt(self):
        if self.fs:
            return self.fs.prompt
        return 'pansh$>'

    def plugin(self, fscls, **setting):
        if not issubclass(fscls, FS):
            raise Exception('must inherit `panshell.core.FS`')

        name = fscls.name
        if name in self.fsmap:
            raise Exception('FS <{}> has already plugin in '.format(name))

        fs = fscls(**setting)
        self.fsmap[name] = (fscls, setting, fs)

    def get_names(self):
        """
        rewrite cmd.Cmd ｀dir(self.__class__)｀
        """
        return dir(self)

    def __getattr__(self, name):
        if name.startswith('do_'):
            action = name[3:]
            if action not in self._keywords:
                return getattr(self.fs, name)

        if name in self.__dict__:
            return self.__dict__[name]

        return cmd.Cmd.__getattr__(name)

    def _plugin_in(self, fs):
        for name in dir(fs):
            action = name[3:]
            if name.startswith('do_') and action not in self._keywords:
                attr = getattr(fs, name)
                if inspect.ismethod(attr):
                    self._funcs.append(action)
                    setattr(self, name, attr)

    def _plugin_out(self):
        for action in self._funcs:
            name = 'do_' + action
            delattr(self, name)

        self._funcs = []

    def set_fs(self, fs):
        if self.fs is not None:
            self._plugin_out()
        self.fs = fs
        self._plugin_in(fs)

    def do_use(self, name):
        """use <fs> 选择使用某个fs
           use baidu
           use local
        """
        if name not in self.fsmap:
            raise Exception('not plugin in this FS with name %s', name)

        fscls, setting, _ = self.fsmap[name]
        fs = fscls(**setting)

        self.stack.append(self.fs)
        self.set_fs(fs)

    def do_exit(self, line):
        """
        退出 shell 或 当前 fs
        """
        if self.fs is None:
            print('exit-shell', file=sys.stdout)
            sys.exit(0)

        self.fs.do_exit(line)
        self.set_fs(self.stack.pop())

    def run(self):
        self.cmdloop()
