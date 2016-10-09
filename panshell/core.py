#coding=utf-8

import cmd
import readline
import sys

class fs(object):
    
    """ 抽象的 filesystem """
    _prompt = '{}-sh$>'

    def __init__(self,name,**kwargs):
        """  """
        self.name = name
        prompt = kwargs.pop('prompt',None)
        if not prompt:
            prompt = _prompt.format(name)

        self.prompt = prompt


class Shell(cmd.Cmd):
    
    prompt = 'pansh$>'

    def __init__(self):        
        
        cmd.Cmd.__init__(self)

        self.fs = None
        self.stack = []

    def plugin(self,fscls,**kwargs):
        if super(fscls) != fs:
            raise Exception('must inherit `panshell.core.fs`')
        tmp = fscls(**kwargs)
        del tmp

    
    def __getattribute__(self,attr):
        print(attr)
        value = self.__getattr__(attr)
        return value


    def do_use(self,name):
        print(name)

    def do_exit(self,line):
        sys.exit(0)

    def run(self):
        self.cmdloop()


