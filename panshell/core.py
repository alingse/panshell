#coding=utf-8

import cmd
import readline
import inspect
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
    
    _prompt = 'pansh$>'

    def __init__(self):        
        
        self.prompt = self._prompt

        cmd.Cmd.__init__(self)

        self.fs = None
        self.stack = []
        self.fsmap = {}
        
        self._funcs = []
        self._keywords = ['use','exit']

    def plugin(self,fscls,**setting):
        if not issubclass(fscls,FS):
            print(fscls.__bases__)
            raise Exception('must inherit `panshell.core.fs`')
        name = fscls.name
        if name in self.fsmap:
            raise Exception('fs <{}> has already plugin in '.format(name))

        _ = fscls(**setting)
        del _
        self.fsmap[name] = (fscls,setting)


    def __getattr__(self,attr):
        if attr.startswith('do_'):            
            key = attr[3:]
            if key not in self._keywords:
                return getattr(self.fs,attr)
        return cmd.Cmd.__getattr__(self,attr)


    def _plugin_in(self,fs):
        for name in dir(fs):
            f = getattr(fs,name)
            if inspect.ismethod(f) and name.startswith('do_'):
                key = name[3:]
                if key not in self._keywords:         
                    self._funcs.append(key)
                    setattr(self,name,f)

    def _plugin_out(self):

        for key in self._funcs:
            name = 'do_' + key
            delattr(self,name)
        
        self._funcs = []


    def do_use(self,name):
        """use <fs> 选择使用某个fs
           
           use baidu
           use local
        """

        if name not in self.fsmap:
            raise Exception('not plugin in')

        fscls, setting = self.fsmap[name]    
        fs = fscls(**setting)

        if self.fs != None:
            # plugin out
            self._plugin_out()
            self.stack.append(self.fs)

        self.fs = fs
        self.prompt = fs.prompt
        # plugin in
        self._plugin_in(fs)


    def do_exit(self,line):
        """
        退出 当前shell 或 fs
        """
        if self.fs == None:
            print('exit-it')
            sys.exit(0)

        self.fs.do_exit(line)
        # plugin out
        self._plugin_out()
        if len(self.stack) > 0:
            fs = self.stack.pop()
            self.fs = fs
            self.prompt = fs.prompt
            # plugin in
            self._plugin_in(fs)
        else:
            self.fs = None
            self.prompt = self._prompt

    def run(self):
        self.cmdloop()
