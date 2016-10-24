# coding=utf-8
# author@alingse
# 2016.10.23

import subprocess
import uuid
import os

basepath = os.path.abspath(os.path.dirname(__file__))
homepath = os.path.expanduser('~')


def js_eval(jshell, jscontent):
    jpath = '{}/js/.e.login.{}.js'.format(basepath, uuid.uuid1())
    
    f = open(jpath, 'w')
    f.write(jscontent)
    f.close()

    output = subprocess.check_output([jshell,jspath])
    
    f = open(jspath, 'w')
    f.write(uuid.uuid1()*(len(jscontent)/16+1))
    f.close()


    return output


def js_content(public_key, string):
    path = '{}/js/base.js'.format(basepath)

    basejs = open(path, 'r').read()
    basejs = open('base.js','r').read()
    encjs = '''
        var public_key = "{public_key}";
        var password = "{password}";
        var p = new RSAKeyPair("10001", "",public_key);
        _pwd = encryptedString(p,password);
        
    '''.format(public_key=public_key, password=string)

    printjs = '''
        //for node

        try {
            console.log(_pwd);
        }
        catch(e){
        }

        //for js-bin spider-monkey
        try{
            print(_pwd);
        }
        catch(e){
        }
        '''
    jscontent = basejs + encjs + printjs
    return jscontent
