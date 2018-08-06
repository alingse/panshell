# coding=utf-8
# author@alingse
# 2018.08.04

import json
import os.path
import re
import time


class BaiduAccount(object):

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36',
    }

    token_url = 'https://passport.baidu.com/v2/api/?getapi&class=login&tpl=mn&tangram=true'
    post_url = 'https://passport.baidu.com/v2/api/?login'
    image_url_format = 'https://passport.baidu.com/cgi-bin/genimage?{code}'

    def __init__(self, username, password):
        self.username = username
        self.password = password

        self.session = None
        self.baiduid = None
        self.bduss = None

    def attach_session(self, session):
        self.session = session
        return self

    @property
    def check_url(self):
        return 'https://passport.baidu.com/v2/api/?logincheck&callback=bdPass.api.login._needCodestring' \
                'CheckCallback&tpl=mn&charset=utf-8&index=0' \
                '&username={username}&time={time}'.format(username=self.username, time=int(time.time()))

    def get_baidu_uid(self):
        """Get BAIDUID."""
        self.session.get('http://www.baidu.com', headers=self.headers)
        self.baiduid = self.session.cookies.get('BAIDUID')

    def check_verify_code(self):
        """Check if login need to input verify code."""
        r = self.session.get(self.check_url)
        s = r.text
        data = json.loads(s[s.index('{'):-1])
        if data.get('codestring'):
            return data.get('codestring', "")
        return ""

    def handle_verify_code(self, code):
        """Save verify code to filesystem and prompt user to input."""
        r = self.session.get(self.image_url_format.format(code=code))

        # FIXME use terminal better
        img_path = os.path.expanduser('~/') + 'pansh.{}.vcode.png'.format(hash(self.username))
        with open(img_path, mode='wb') as fp:
            fp.write(r.content)
        print("Saved verification code to {}".format(os.path.dirname(img_path)))
        vcode = raw_input("Please input the captcha:\n")
        return vcode

    def get_token(self):
        """Get bdstoken."""
        r = self.session.get(self.token_url)
        s = r.text
        token = re.search("login_token='(\w+)';", s).group(1)
        return token

    def post_login(self, code, vcode, token):
        """Post login form."""
        post_data = {'ppui_logintime': '9379', 'charset': 'utf-8', 'codestring': code, 'token': token,
                     'isPhone': 'false', 'index': '0', 'u': '', 'safeflg': 0,
                     'staticpage': 'http://www.baidu.com/cache/user/html/jump.html', 'loginType': '1', 'tpl': 'mn',
                     'callback': 'parent.bdPass.api.login._postCallback', 'username': self.username,
                     'password': self.password, 'verifycode': vcode, 'mem_pass': 'on'}

        response = self.session.post(self.post_url, data=post_data)
        return response

    def login(self):
        self.get_baidu_uid()
        code = self.check_verify_code()
        if code:
            vcode = self.handle_verify_code(code)
        else:
            vcode = ""
        token = self.get_token()
        response = self.post_login(code, vcode, token)
        # error
        if 'error=257' in response.text:
            code = re.findall('codestring=(.*?)&', response.text)[0]
            vcode = self.handle_verify_code(code)
            response = self.post_login(code, vcode, token)
        self.bduss = response.cookies.get("BDUSS")

    @property
    def login_status(self):
        return self.bduss and self.baiduid

'''
   disk_home = 'https://pan.baidu.com/'

    headers = {
        "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4",
        "Accept-Encoding": "gzip, deflate, sdch, br",
        "Host": "pan.baidu.com",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Upgrade-Insecure-Requests": "1",
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36"
    }


    headers = {
        "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4",
        "Accept-Encoding": "gzip, deflate, sdch, br",
        "Host": "pan.baidu.com",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Upgrade-Insecure-Requests": "1",
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36"
        }


    def get(self, url, headers=None, **kwargs):
        if headers is None:
            headers = self.headers

        try:
            print(self.session.cookies.get_dict())
            r = self.session.get(url, headers=headers, **kwargs)
            return r.content
        except Exception as e:
            logging.warn(e)

    def parse_home(self):
        content = self.get(self.disk_home)
        if content is None:
            return False
        sk = content.find('var context=')
        if sk == -1:
            print(sk, content)
            return False
        sk += len('var context=')
        ek = content.find(';', sk)
        config = content[sk:ek]
        self.context = json.loads(config)
        self.nick = context['username']
        return True


'''
