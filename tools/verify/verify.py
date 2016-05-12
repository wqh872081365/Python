#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pytesseract
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random

from Tkinter import Frame, Label, Entry, Button
import tkMessageBox
import MySQLdb

# simple image to string
'''
image = Image.open('chinese.jpg')

vcode = pytesseract.image_to_string(image, lang='chi_sim')

print image

print vcode
'''

# string to image

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

    # run Button
    def run(self):
        number = self.numberInput.get()
        digit = self.digitInput.get()

        with open('E:/pycharm/practice1/image/verify.txt', 'w') as f:
            verify = verify_str(number, digit)
            f.write(verify)

        tkMessageBox.showinfo('verify', verify)

# 随机A-Z
def rndChar():
    return chr(random.randint(65, 90))

# 随机Color
def rndColor():
    return random.randint(64, 255), random.randint(64, 255), random.randint(64, 255)

# 随机Color2
def rndColor2():
    return random.randint(32, 127), random.randint(32, 127), random.randint(32, 127)

#　获取字符型验证码
def verify_str(number, digit):

    try:
        number = int(number)
    except ValueError:
        return 'number must belong to int'

    try:
        digit = int(digit)
    except ValueError:
        return 'digit must belong to int'

    if digit > 10:
        return 'digit is too long'

    width = 60*digit
    height = 60
    verify_data = ''

    # 保存到数据库MySQL
    db = MySQLdb.connect("localhost", "root", "password", "verify")
    cursor = db.cursor()

    sql = """CREATE TABLE IF NOT EXISTS TABLE_VERIFY(ID_VERIFY INT PRIMARY KEY AUTO_INCREMENT,VERIFY_STR CHAR(20),
    VERIFY_PATH CHAR(100),VERIFY_IMAGE MEDIUMBLOB) DEFAULT CHARSET=utf8"""
    cursor.execute(sql)
    db.commit()

    for a in range(number):
        image = Image.new('RGB', (width, height), (255, 255, 255))
        font = ImageFont.truetype('C:\Windows\Fonts\Arial.ttf', 36)
        draw = ImageDraw.Draw(image)

        for x in range(width):
            for y in range(height):
                draw.point((x, y), fill=rndColor())

        chrtem = ''

        for t in range(digit):
            tem = rndChar()
            draw.text((60*t+10, 10), tem, font=font, fill=rndColor2())
            chrtem += tem

        verify_data += chrtem + '\n'
        verify_path = 'E:/pycharm/practice1/image/code'+str(a+1)+'.jpg'

        # 保存图形文件
        image = image.filter(ImageFilter.BLUR)
        image.save(verify_path, 'jpeg')

        # 读取图形文件
        f = open(verify_path, 'rb')
        img = f.read()
        f.close()

        # 插入记录
        sql = """INSERT IGNORE INTO TABLE_VERIFY(VERIFY_STR, VERIFY_PATH, VERIFY_IMAGE)
        VALUES('%s','%s','%s')""" % (chrtem, verify_path, MySQLdb.escape_string(img))
        cursor.execute(sql)
        db.commit()

    cursor.close()
    db.close()

    return verify_data


def main():
    app = Application()
    app.master.title('verify_list')
    app.mainloop()

if __name__ == '__main__':
    main()


