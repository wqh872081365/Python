#!/usr/bin/env python
# -*- coding:utf-8 -*-

import string
import requests
import re

'number 0'

# print 2 ** 38

'number 1'
# map -> ocr

"""
str1 = 'g fmnc wms bgblr rpylqjyrc gr zw fylb. rfyrq ufyr amknsrcpq ypc dmp. bmgle gr gl zw fylb gq glcddgagclr ylb rfyr\'q ufw rfgq rcvr gq qm jmle. sqgle qrpgle.kyicrpylq() gq pcamkkclbcb. lmu ynnjw ml rfc spj.'
str2 = ''
# print [chr(ord(x)+2) for x in str1]


for x in str1:
    if not (x == ' ' or x == '\'' or x == '.' or x == '(' or x == ')'):
        if x == 'y' or x == 'z':
            x = chr(ord(x)-24)
        else:
            x = chr(ord(x)+2)
    str2 += x
# print str2


table = string.maketrans(string.lowercase, string.lowercase[2:]+string.lowercase[:2])
# print str1.translate(table)
"""

'number 2'
# ocr -> equality

"""
r = requests.get(url='http://www.pythonchallenge.com/pc/def/ocr.html')
# print r.text

r2 = ''

for r1 in r.text:
    if r1 in string.lowercase or r1 in string.uppercase:
        r2 += r1
# print r2
"""

'number 3'
# linkedlist

"""
r3 = requests.get(url='http://www.pythonchallenge.com/pc/def/equality.html')
# print r3.text

res = re.compile(r'[^A-Z][A-Z]{3}([a-z])[A-Z]{3}[^A-Z]')
list3 = re.findall(res, r3.text)
result = ''
for x in list3:
    result += x.encode('utf-8')
print result
# print re.search(res, r3.text).groups()
"""

'number 4'
# 12345 82682 44671 66831 peak.html

"""
url4 = 'http://www.pythonchallenge.com/pc/def/linkedlist.php?nothing=44671'
r4 = requests.get(url=url4)
res = re.compile(r'[0-9]+')
res4 = re.search(res, r4.text).group().encode('utf-8')

for x in range(400):
    url4 = 'http://www.pythonchallenge.com/pc/def/linkedlist.php?nothing='+res4
    r4 = requests.get(url=url4)
    m = re.search(res, r4.text)
    if m is not None:
        res4 = m.group().encode('utf-8')
        print r4.text, url4, x
    elif res4 == '16044':
        res4 = '8022'
        print r4.text, url4, x
    elif res4 == '82683':
        res4 = '63579'
        print r4.text, url4, x
    else:
        print r4.text, url4, x
        break
"""

'number 5'
#



