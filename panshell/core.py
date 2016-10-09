#coding=utf-8

import cmd
import readline
import sys

class FS(object):
    
    """ 抽象的 filesystem """
    _prompt = '{}-sh$>'

    def __init__(self,name,**kwargs):
        """  """
        self.name = name
        prompt = kwargs.pop('prompt',None)
        if not prompt:
            prompt = self._prompt.format(name)

        self.prompt = prompt


class Shell(cmd.Cmd):
    
    prompt = 'pansh$>'

    def __init__(self):        
        
        cmd.Cmd.__init__(self)

        self.fs = None
        self.stack = []
        self.fsmap = {}

        self.keywords = ['use']

    def plugin(self,fscls,**kwargs):
        if fscls.__bases__[0] != FS:
            raise Exception('must inherit `panshell.core.fs`')
        name = fscls.name
        if name in self.fsmap:
            raise Exception('fs <{}> has already plugin in '.format(name))
        #try it
        tmp = fscls(**kwargs)
        del tmp
        self.fsmap[name] = fscls

    def __getattr__(self,attr):
        if attr not in self.keywords:
            def f (x,y):
                print(x,y)
            if attr.startswith('do_'):
                return lambda x:f(self,x)
                
        return cmd.Cmd.__getattr__(self,attr)


    def do_use(self,name):
        print(name)


    def run(self):
        self.cmdloop()


