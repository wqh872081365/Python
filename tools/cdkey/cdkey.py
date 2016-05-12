#!/usr/bin/env python
# -*- coding:utf-8 -*-

import string
import random
from Tkinter import *
import tkMessageBox
import MySQLdb
import redis

# 简易GUI
class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.titleLabel = Label(self, text='please input number and digit !')
        self.titleLabel.pack()
        self.numberLabel = Label(self, text='number: ')
        self.numberLabel.pack()
        self.numberInput = Entry(self)
        self.numberInput.pack()
        self.digitLabel = Label(self, text='digit: ')
        self.digitLabel.pack()
        self.digitInput = Entry(self)
        self.digitInput.pack()
        self.runButton = Button(self, text='run', command=self.run)
        self.runButton.pack()
        self.quitButton = Button(self, text='quit', command=self.quit)
        self.quitButton.pack()

    # run Button 响应
    def run(self):
        number = self.numberInput.get()
        digit = self.digitInput.get()

        with open('cdkey.txt', 'w') as f:
            key = cdkey(number, digit)
            f.write(key)

        tkMessageBox.showinfo('key', key)

# 获取CDKey
def cdkey(number, digit):

    try:
        number = int(number)
    except ValueError:
        return 'number must belong to int'

    try:
        digit = int(digit)
    except ValueError:
        return 'digit must belong to int'

    if digit < 8:
        return 'digit is too short'

    data = ''
    data_list = []

    # 保存到MySQL数据库
    db = MySQLdb.connect("localhost", "root", "password", "cdkey")
    cursor = db.cursor()

    # 保存到redis数据库
    r = redis.Redis(host='localhost', port=6379, db=11, password='password')

    for count in range(number):
        a = key_creator(digit)
        data += a + '\n'
        data_list.append(a)

        sql = """INSERT INTO TABLE_KEY(ID_KEY, KEY_COL) VALUES('%d','%s')""" % (count+1, a)
        cursor.execute(sql)

        r.set(count+1, a)

    cursor.close()
    db.commit()
    db.close()

    r.save()

    return data

# 获取一条记录
def key_creator(digit):
    key = ''
    for word in range(digit):
        key += random.choice(string.ascii_uppercase + string.digits)
    return key


def main():
    app = Application()
    app.master.title('cdkey')
    app.mainloop()

if __name__ == '__main__':
    main()







