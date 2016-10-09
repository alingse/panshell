#coding=utf-8
#author@alingse
#2016.10.09

from panshell.core import FS


class baidu(FS):
    name = 'baidu'
    def __init__(self,**kwargs):
        super(baidu,self).__init__(self,name=name,**kwargs)

    def do_ls(self,line):
        print(self.name,'ls')