#!/usr/bin/env python3
# -*- coding:utf-8 _*_

__author__ = 'wangqihui'

'知乎登录功能'

import re
import urllib
import urllib.parse
import urllib.request
import http.cookiejar

header = {
    'Connection': 'keep-alive',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36',
    'Accept-Language': 'zh-CN,zh;q=0.8'
}

def getOpener(head):
    # deal with the cookies
    cj = http.cookiejar.CookieJar()
    pro = urllib.request.HTTPCookieProcessor(cj)
    opener = urllib.request.build_opener(pro)
    header = []
    for key, value in head.items():
        elem = (key, value)
        header.append(elem)
    opener.addheaders = header
    return opener

url = 'http://www.zhihu.com/'
opener = getOpener(header)
op = opener.open(url)
data = op.read()
link_re = re.compile(r'name="_xsrf" value="(.*?)"')
_xsrf = link_re.findall(data.decode())[0]

url += 'login/email'
id = 'email'
password = 'password'
postDict = {
    '_xsrf': _xsrf,
    'email': id,
    'password': password,
    'remember_me': 'true'
}
postData = urllib.parse.urlencode(postDict).encode()  # 发送 TextView
op = opener.open(url, postData)
data = op.read().decode()
print(data.encode())  # 接受 TextView
