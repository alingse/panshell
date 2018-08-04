# coding=utf-8
# author@alingse
# 2016.12.14

import json
import logging
import requests

from login import login
from login import visit_url

class Pan(object):
    disk_home = 'https://pan.baidu.com/'

    headers = {
        "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4", 
        "Accept-Encoding": "gzip, deflate, sdch, br", 
        "Host": "pan.baidu.com", 
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", 
        "Upgrade-Insecure-Requests": "1", 
        "Connection": "keep-alive", 
        # "Cookie": "PANWEB=1; secu=1; BDUSS=FaM1VOU2xySWJpczltU2JvTno1UkI4RkNDQm93NEVBRHY5Rk5jLW5qd211WmxZSVFBQUFBJCQAAAAAAAAAAAEAAADUuagmtefG-Naux7AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACYsclgmLHJYWk; STOKEN=309a91ba41deebc95f195b5e921a98bd2b469dc637d697df378bfea9672ac55a; SCRC=a4e9aa89da6dc929f8d6aabfadcbb55b; BAIDUID=95EF17F85F9681DCD5C928F861C22F11:FG=1; BIDUPSID=5BAFB05104F3BD8089E1AF3218F01CFB; PSTM=1483897153; PSINO=7; H_PS_PSSID=1452_21118_17001_20698; pgv_pvi=1579108352; pgv_si=s5990712320; Hm_lvt_7a3960b6f067eb0085b7f96ff5e660b0=1483453930,1483877421,1483888577,1483982534; Hm_lpvt_7a3960b6f067eb0085b7f96ff5e660b0=1483982534; cflag=15%3A3; PANPSC=12595739823646408641%3A5e7emfqPscI23oUCIFIrBOn90oj%2BY%2FIsgF65T%2F3uyeY%2B2W5p%2FZpnszSh4urKG3yYSrvFsiwiy%2BGtcMJUDArx5A7FIdK4KiBN3Qw%2BedwMU7Xptl5jktm3V0NQsOYbdMWf3jGzPWbmHccDzLGxCF9yjchTKu%2BdwTb%2Fnr9yQoCeHI88g1PcRcrciFklnS5G%2BZJP", 
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

    def __init__(self):
        self.session = requests.Session()
        self.is_login = False
        self.context = None

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

    def login(self, username, password):
        self.username = username        
        status = login(self.session, username, password)
        print(status)
        if status:
            self.is_login = True
            self.parse_home()
        return status


if __name__ == '__main__':
    import sys
    pan = Pan()
    pan.login(sys.argv[1], sys.argv[2])
    print pan.context
