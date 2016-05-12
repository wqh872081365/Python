#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Python version: 2.7.11
# Author: WangQihui
# date: 2016/05/10 - 2016/05/11
# version: 1.0

'''
小球碰撞
'''

from Tkinter import *
import time
import random


class Ball(object):
    # 球体属性设定
    def __init__(self, rad, color, pos_x, pos_y, v_x, v_y, a_x=0, a_y=0):
        self.r = rad
        self.color = color
        self.x = pos_x
        self.y = pos_y
        self.v_x = v_x
        self.v_y = v_y
        self.a_x = a_x
        self.a_y = a_y

    def ball_pos(self):
        # 自动运行的单个球体位置更新
        # 自动运行的单个球体位置与边界的碰撞判断与速度处理
        t = 0.01
        ball_tem = self
        ball_tem.x, ball_tem.y = self.x + self.v_x * t, self.y + self.v_y * t
        if ball_tem.y > 400 - self.r or ball_tem.y < self.r:
            ball_tem.v_y = -1 * ball_tem.v_y
        if ball_tem.x > 600 - self.r or ball_tem.x < self.r:
            ball_tem.v_x = -1 * ball_tem.v_x
        return ball_tem

    def balls_wait_pos(self, list):
        # 自动运行的球体之间的碰撞判断与速度处理
        for index_1 in range(len(list)):
            if (list[index_1].x - self.x) ** 2 + (list[index_1].y - self.y) ** 2 < (list[index_1].r + self.r) ** 2:
                list[index_1].v_x, list[index_1].v_y = -1 * list[index_1].v_x, -1 * list[index_1].v_y
        return list


def balls_pos(list):
    # 可控制的球体与自动运行球体之间的碰撞判断与速度处理
    for index_1 in range(len(list)-1):
        for index_2 in range(index_1+1, len(list)):
            if (list[index_1].x - list[index_2].x) ** 2 + (list[index_1].y - list[index_2].y) ** 2 < \
                            (list[index_1].r + list[index_2].r) ** 2:
                list[index_1].v_x, list[index_1].v_y, list[index_2].v_x, list[index_2].v_y = \
                    list[index_2].v_x, list[index_2].v_y, list[index_1].v_x, list[index_1].v_y
    return list


class Balls(Frame):
    # 用户界面的框架设计 使用Tkinter
    def __init__(self, ball_start, master=None):
        # 初始化函数 输入初始化球体的属性
        Frame.__init__(self, master)
        self.pack()
        Pack.config(self)
        self.ball = ball_start[0:len(ball_start)-1]  # 自动运行的球体多个
        self.ball_wait = ball_start[len(ball_start)-1]  # 可控制的球体1个
        self.t = 0.01  # 设定延时时间
        self.createWidgets()  # 框架初始化
        self.after(int(self.t*1000), self.moveBall)  # 框架循环

    def createWidgets(self):
        # 框架设计
        self.draw = Canvas(self, width='600', height='400', bg='white')  # 画布设计
        self.ball = [self.ball[index].ball_pos() for index in range(len(self.ball))]  # 自动运行球体的数据更新
        self.ball_wait = self.ball_wait.ball_pos()  # 可控制球体的数据更新
        self.ball_new = [self.draw.create_oval(self.ball[index].x-self.ball[index].r,
                                               self.ball[index].y+self.ball[index].r,
                                               self.ball[index].x+self.ball[index].r,
                                               self.ball[index].y-self.ball[index].r,
                                               fill=self.ball[index].color) for index in range(len(self.ball))]
        # 自动运行球体在画布上的绘制
        self.ball_wait_new = self.draw.create_oval(self.ball_wait.x-self.ball_wait.r,
                                                   self.ball_wait.y+self.ball_wait.r,
                                                   self.ball_wait.x+self.ball_wait.r,
                                                   self.ball_wait.y-self.ball_wait.r,
                                                   fill=self.ball_wait.color)
        # 手动控制球体在画布上的绘制
        self.draw.pack()  # 所有球体在画布上的添加
        self.upButton = Button(self, text='w', command=self.up)
        self.upButton.bind('<Key>', self.printEvent)
        self.upButton.focus_set()
        self.upButton.pack(side=LEFT)
        # 控制球体向上运行，每按一次，向上1个像素；同时与键盘‘w’绑定
        self.leftButton = Button(self, text='a', command=self.left)
        self.leftButton.bind('<Key>', self.printEvent)
        self.leftButton.focus_set()
        self.leftButton.pack(side=LEFT)
        # 控制球体向左运行，每按一次，向左1个像素；同时与键盘‘a’绑定
        self.rightButton = Button(self, text='d', command=self.right)
        self.rightButton.bind('<Key>', self.printEvent)
        self.rightButton.focus_set()
        self.rightButton.pack(side=LEFT)
        # 控制球体向右运行，每按一次，向右1个像素；同时与键盘‘d’绑定
        self.downButton = Button(self, text='s', command=self.down)
        self.downButton.bind('<Key>', self.printEvent)
        self.downButton.focus_set()
        self.downButton.pack(side=LEFT)
        # 控制球体向下运行，每按一次，向下1个像素；同时与键盘‘s’绑定
        self.quitButton = Button(self, text='quit', command=self.quit)
        self.quitButton.pack(side=RIGHT)
        # 退出键

    def moveBall(self):
        # 控制球体运行的循环函数
        # start = time.clock()
        # print start
        self.ball = [self.ball[index].ball_pos() for index in range(len(self.ball))]  # 自动运行球体的位置更新
        self.ball = balls_pos(self.ball)  # 自动运行球体之间的碰撞判断
        self.ball_wait.balls_wait_pos(self.ball)  # 手动控制球体与自动运行球体之间的碰撞判断
        for index in range(len(self.ball)):
            self.draw.move(self.ball_new[index], str(self.ball[index].v_x*self.t), str(self.ball[index].v_y*self.t))
        # 自动运行球体在画布上的位置更新
        # end = time.clock()
        # print end
        # print end-start
        self.after(int(self.t*1000), self.moveBall)
        # 循环函数

    def up(self):
        # 手动按钮控制球体坐标向上一个像素，并在画布上更新
        ball_wait_tem = self.ball_wait
        ball_wait_tem.y -= 1
        self.draw.move(self.ball_wait_new, str(0), str(-1))
        self.ball_wait = ball_wait_tem

    def left(self):
        # 手动按钮控制球体坐标向左一个像素，并在画布上更新
        ball_wait_tem = self.ball_wait
        ball_wait_tem.x -= 1
        self.draw.move(self.ball_wait_new, str(-1), str(0))
        self.ball_wait = ball_wait_tem

    def right(self):
        # 手动按钮控制球体坐标向右一个像素，并在画布上更新
        ball_wait_tem = self.ball_wait
        ball_wait_tem.x += 1
        self.draw.move(self.ball_wait_new, str(1), str(0))
        self.ball_wait = ball_wait_tem

    def down(self):
        # 手动按钮控制球体坐标向下一个像素，并在画布上更新
        ball_wait_tem = self.ball_wait
        ball_wait_tem.y += 1
        self.draw.move(self.ball_wait_new, str(0), str(1))
        self.ball_wait = ball_wait_tem

    def printEvent(self, event):
        # 手动键盘‘wasd’控制球体运行，更新坐标，并在画布上更新
        if event.char == 'w':
            ball_wait_tem = self.ball_wait
            ball_wait_tem.y -= 1
            self.draw.move(self.ball_wait_new, str(0), str(-1))
            self.ball_wait = ball_wait_tem
        elif event.char == 'a':
            ball_wait_tem = self.ball_wait
            ball_wait_tem.x -= 1
            self.draw.move(self.ball_wait_new, str(-1), str(0))
            self.ball_wait = ball_wait_tem
        elif event.char == 'd':
            ball_wait_tem = self.ball_wait
            ball_wait_tem.x += 1
            self.draw.move(self.ball_wait_new, str(1), str(0))
            self.ball_wait = ball_wait_tem
        elif event.char == 's':
            ball_wait_tem = self.ball_wait
            ball_wait_tem.y += 1
            self.draw.move(self.ball_wait_new, str(0), str(1))
            self.ball_wait = ball_wait_tem


def main():
    color_list = ['black', 'darkblue', 'darkgreen', 'darkcyan', 'darkred', 'darkmagenta',  'brown', 'blue', 'green',
                  'cyan', 'red', 'magenta', 'yellow']
    # 使用的球体颜色list

    pos_slice1 = random.sample(range(100, 550, 50), 5)
    pos_slice2 = random.sample(range(100, 350, 50), 5)
    # 使用的球体初始位置坐标范围和数量

    ball_start = [Ball(random.randint(15, 30), random.choice(color_list),
                       pos_slice1[l], pos_slice2[l],
                       random.choice(range(50, 151)+(range(-150, -49))),
                       random.choice(range(50, 151)+(range(-150, -49)))) for l in range(5)]
    # 使用的球体初始速度范围和数量

    game = Balls(ball_start)  # 建立新对象
    game.master.title('ball')  # 对象标题
    game.mainloop()  # 输入检测循环


if __name__ == '__main__':
    main()

