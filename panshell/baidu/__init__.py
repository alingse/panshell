#coding=utf-8
#author@alingse
#2016.10.09

from panshell.core import FS


class baiduFS(FS):
    """ baidu yunpan (百度云盘) 文件系统"""
    name = 'baidu'
    def __init__(self,**kwargs):
        name = kwargs.pop('name',self.name)        
        FS.__init__(self,name,**kwargs)


    def do_ls(self,line):
        print(self.name,'ls')

if __name__ == '__main__':
    fs = baiduFS()