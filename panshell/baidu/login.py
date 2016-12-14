# coding=utf-8
# author@alingse
# 2016.06.22

import logging
import sys
import time

from .const import PUBLIC_KEY
from .const import RSA_E
from .const import RSA_D

from .rsa import RSAKeyPair


headers = {
    "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
    "Accept-Encoding": "gzip, deflate, sdch",
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1",
    "Connection": "keep-alive",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "Referer": "http://wappass.baidu.com/passport/?login&tpl=wimn&ssid%3D0%26amp%3Bfrom%3D844b%26amp%3Buid%3D%26amp%3Bpu%3Dsz%25401320_2001%252Cta%2540iphone_1_9.1_3_601%26amp%3Bbd_page_type%3D1&tn=&regtype=1&u=https%3A%2F%2Fm.baidu.com",
    "X-Requested-With": "XMLHttpRequest",
    }

baidu_rsa = RSAKeyPair(RSA_E, RSA_D, PUBLIC_KEY)

now = lambda: str(int(time.time() * 1000))


def visit_url(session, url):
    try:
        r = session.get(url, headers=headers, timeout=2)
        return r.content
    except Exception as e:
        logging.warn(e)


def get_servertime(session):
    url = 'http://wappass.baidu.com/wp/api/security/antireplaytoken'
    params = {
        'tpl': 'wimn',
        'v': now()
        }

    try:
        r = session.get(url, params=params, headers=headers, timeout=1)
        return r.json()
    except Exception as e:
        logging.error(e)


def post_login(session, servertime, username, encrypt_pwd):
    url = 'https://wappass.baidu.com/wp/api/login?tt=' + now()

    cookies = session.cookies.get_dict()
    uid = cookies.get('BAIDU_WISE_UID', now() + '_530')

    data = {
        "tpl": "wimn",
        "uid": uid,
        "clientfrom": "",
        "servertime": servertime,
        "verifycode": "",
        "login_share_strategy": "",
        "connect": "0",
        "skin": "default_v2",
        "mobilenum": "undefined",
        "from": "844c",
        "ssid": "",
        "bindToSmsLogin": "",
        "pu": "sz%401320_2001%2Cta%40iphone_1_4.0_3_532",
        "regist_mode": "",
        "tn": "",
        "subpro": "",
        "regtype": "",
        "type": "",
        "username": username,
        "logLoginType": "wap_loginTouch",
        "password": encrypt_pwd,
        "countrycode": "",
        "adapter": "0",
        "bd_page_type": "1",
        "loginmerge": "1",
        "client": "",
        "action": "login",
        "vcodestr": "",
        "isphone": "0"
        }

    try:
        r = session.post(url, data=data, headers=headers, timeout=3)
        return r.json()
    except Exception as e:
        logging.warn(e)


def login(session, username, password):
    # prepare
    home_url = 'https://wap.baidu.com'
    passport_url = 'http://wappass.baidu.com/passport/?login&tpl=wimn&ssid%3D0%26amp%3Bfrom%3D%26amp%3Buid%3D%26amp%3Bpu%3Dsz%25401320_1001%252Cta%2540iphone_2_5.0_3_537%26amp%3Bbd_page_type%3D1&tn=&regtype=1&u=http://cp01-mi-wise32.cp01.baidu.com:8080/'

    visit_url(session, home_url)
    visit_url(session, passport_url)

    # get servertime
    result = get_servertime(session)
    if result is None or 'time' not in result:
        return False

    servertime = result['time']

    # encrypt
    encrypt_pwd = baidu_rsa.encrypt(password + servertime)

    # login
    result = post_login(session, servertime, username, encrypt_pwd)
    if result is None:
        return False

    if result['errInfo']['no'] != '400408':
        return False

    # ptoken
    session.cookies.set('BDUSS', result['data']['bduss'])

    # visit goto
    visit_url(session, result['data']['gotoUrl'])
    visit_url(session, result['data']['u'])
    return True


if __name__ == '__main__':
    import requests
    username = sys.argv[1]
    password = sys.argv[2]
    session = requests.Session()

    status = login(session, username, password)
    print(status)
