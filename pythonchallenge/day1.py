#!/usr/bin/env python
# -*- coding:utf-8 -*-

import string
import requests

'number 0'

print 2 ** 38

'number 1'
# map -> ocr

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
print str2


table = string.maketrans(string.lowercase, string.lowercase[2:]+string.lowercase[:2])
print str1.translate(table)

'number 2'
# ocr -> equality

r = requests.get(url='http://www.pythonchallenge.com/pc/def/ocr.html')
# print r.text

r2 = ''

for r1 in r.text:
    if r1 in string.lowercase or r1 in string.uppercase:
        r2 += r1
print r2

'number 3'
#



