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

    def do_use(self,name):
        print(name)

    def do_exit(self,line):
        sys.exit(0)

    def run(self):
        self.cmdloop()


