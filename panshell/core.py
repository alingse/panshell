#coding=utf-8

import cmd

class shell(cmd.Cmd):
    prompt = 'pansh$>'
    def run(self):
        self.cmdloop()




def pansh():
    sh = shell()
    sh.run()
