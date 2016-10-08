#coding=utf-8

import cmd
import  readline

class fsAction(object):
    """docstring for fsAction"""

    def do_ls(self, path='.'):
        pass

    def do_cd(self,path=None):
        pass

    def do_login(self,line):
        pass

    def do_exit(self,line):
        pass



class Shell(cmd.Cmd):
    
    prompt = 'pansh$>'

    def do_use(self,name):
        print(name)

    def run(self):
        self.cmdloop()


