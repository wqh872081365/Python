#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Python version: 2.7.11
# pygame version：1.9.2a0
# system：windows7 64 bit
# Author: WangQihui  E-mail : wangqihui0324@gmail.com
# date: 2016/05/14 -05/18
# version: 1.0


import pygame
from pygame.locals import *
from sys import exit
import time
import random
from fir_ai import searcher


class ChessPlay(object):
    def __init__(self):
        pygame.init()  # pygame初始化
        self.size_x = 15  # 棋盘X轴
        self.size_y = 15  # 棋盘Y轴
        self.chess_next = 'black'  # 下一个落子的颜色
        self.first_step = 'P'  # P（玩家），C（AI）先手
        # self.first_step = 'C'
        self.chess_depth = 1  # 难度，默认为1，简单；2，中等；3，困难
        self.chess_start = 0  # 游戏开始设置
        self.ai_tem = 1  # AI走一步
        self.chess_white_list = []  # 白棋列表
        self.chess_black_list = []  # 黑棋列表
        self.chess_list_all = [(x, y) for x in range(1, self.size_x + 1) for y in range(1, self.size_y + 1)]  # 全表
        self.chess_both_list = []  # 白棋和黑棋列表
        self.chess_list_opp = list(set(self.chess_list_all)-set(self.chess_both_list))  # 空的列表
        self.board = [[0 for n in xrange(self.size_y)] for m in xrange(self.size_x)]  # 棋盘阵列图，注意0 - size-1
        self.last_pos = (0, 0)  # 最近1个落子的位置
        self.chess_result = ''  # 棋局结果
        self.start_time = time.time()
        self.sum_time = 0
        self.SCREEN_SIZE = [640, 489]  # SCREEN_SIZE初始化
        self.screen = pygame.display.set_mode(self.SCREEN_SIZE, 0, 32)  # screen初始化
        self.background = pygame.image.load("C:/Users/wangq/Documents/wqh872081365/Python/game/FIR/images/chessboard.png").convert()
        # 获得background
        self.background_side = pygame.image.load("C:/Users/wangq/Documents/wqh872081365/Python/game/FIR/images/board.png").convert()
        # 获得background_side
        self.chess_black = pygame.image.load("C:/Users/wangq/Documents/wqh872081365/Python/game/FIR/images/black.png").convert_alpha()
        # 获得chess_black
        self.chess_white = pygame.image.load("C:/Users/wangq/Documents/wqh872081365/Python/game/FIR/images/white.png").convert_alpha()  # 获得chess_white
        self.font = pygame.font.Font("C:/Users/wangq/Documents/wqh872081365/Python/game/FIR/source/fonts/ncsj.ttf", 25)  # 字体设置
        self.text1_surface = self.font.render(u"玩家先", True, (0, 0, 0), (0, 255, 0))
        # pygame.image.save(self.text1_surface, "source/image/text1.png")
        self.text2_surface = self.font.render(u'AI先', True, (0, 0, 0), (255, 255, 255))
        # pygame.image.save(self.text2_surface, "source/image/text2.png")
        self.text3_surface = self.font.render(u'Start', True, (0, 0, 0), (255, 255, 255))
        # pygame.image.save(self.text3_surface, "source/image/text3.png")
        self.text4_surface = self.font.render(u'End', True, (0, 0, 0), (255, 255, 255))
        # pygame.image.save(self.text4_surface, "source/image/text4.png")
        self.text5_surface = self.font.render(u'悔棋', True, (0, 0, 0), (255, 255, 255))
        # pygame.image.save(self.text5_surface, "source/image/text5.png")
        self.text6_surface = self.font.render(u'难度：', True, (0, 0, 0), (255, 255, 255))
        # pygame.image.save(self.text6_surface, "source/image/text6.png")
        self.text7_surface = self.font.render(u'低', True, (0, 0, 0), (0, 255, 0))
        # pygame.image.save(self.text7_surface, "source/image/text7.png")
        self.text8_surface = self.font.render(u'中', True, (0, 0, 0), (255, 255, 255))
        # pygame.image.save(self.text8_surface, "source/image/text8.png")
        self.text9_surface = self.font.render(u'高', True, (0, 0, 0), (255, 255, 255))
        # pygame.image.save(self.text9_surface, "source/image/text9.png")
        self.text10_surface = self.font.render(u'计时：', True, (0, 0, 0), (255, 255, 255))
        # pygame.image.save(self.text10_surface, "source/image/text10.png")
        self.text11_surface = self.font.render(u'Result：', True, (0, 0, 0), (255, 255, 255))
        # pygame.image.save(self.text11_surface, "source/image/text11.png")
        self.text12_surface = self.font.render(u'', True, (0, 0, 0))
        # pygame.image.save(self.text12_surface, "source/image/text12.png")
        self.text13_surface = self.font.render(u'0', True, (0, 0, 0), (255, 255, 255))
        # pygame.image.save(self.text13_surface, "source/image/text13.png")
        pygame.display.set_caption("五子棋")  # screen标题
        self.updateChessBoard()  # 棋盘实时更新

    def updateChessBoard(self):
        # 棋盘更新

        while True:
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.background_side, (490, 0))
            self.screen.blit(self.text1_surface, (500, 100))
            self.screen.blit(self.text2_surface, (500, 150))
            self.screen.blit(self.text3_surface, (500, 400))
            self.screen.blit(self.text4_surface, (570, 400))
            self.screen.blit(self.text5_surface, (500, 450))
            self.screen.blit(self.text6_surface, (500, 200))
            self.screen.blit(self.text7_surface, (500, 250))
            self.screen.blit(self.text8_surface, (540, 250))
            self.screen.blit(self.text9_surface, (580, 250))
            self.screen.blit(self.text10_surface, (500, 5))
            self.screen.blit(self.text11_surface, (500, 300))
            self.screen.blit(self.text12_surface, (500, 350))
            self.screen.blit(self.text13_surface, (500, 50))

            self.chess_place()
            if self.chess_start == 1:
                self.sum_time = int(time.time() - self.start_time)
                self.text13_surface = self.font.render(str(self.sum_time), True, (0, 0, 0), (255, 255, 255))

            if self.chess_start == 1:
                self.get_mouse()

            pygame.display.update()

            for event in pygame.event.get():  # 事件处理
                if event.type == QUIT:  # 点击关闭按钮
                    pygame.quit()
                    exit()

                if self.chess_start == 1:
                    if event.type == MOUSEBUTTONUP:
                        if self.first_step == 'P':
                            if self.get_mouseButton(event):
                                if self.chess_result != '':
                                    self.start_new()
                                else:
                                    self.get_ai_place()
                                    if self.chess_result != '':
                                        self.start_new()

                    if self.first_step == 'C':
                        if self.ai_tem == 1:
                            self.get_ai_place()
                            self.ai_tem += 1
                            if self.chess_result != '':
                                self.start_new()
                        if event.type == MOUSEBUTTONUP:
                            if self.get_mouseButton(event):
                                self.ai_tem = 1
                                if self.chess_result != '':
                                    self.start_new()

                    if event.type == MOUSEBUTTONDOWN:
                        # end按钮实现
                        if 570 < event.pos[0] < 603 and 400 < event.pos[1] < 428:
                            self.text4_surface = self.font.render(u'End', True, (0, 0, 0), (0, 255, 0))
                            self.screen.blit(self.text4_surface, (570, 400))
                            pygame.display.update()
                            # pygame.image.save(self.text4_surface, "source/image/text4_1.png")
                    if event.type == MOUSEBUTTONUP:
                        if 570 < event.pos[0] < 603 and 400 < event.pos[1] < 428:
                            self.text4_surface = self.font.render(u'End', True, (0, 0, 0), (255, 255, 255))
                            self.start_new()

                    if event.type == MOUSEBUTTONDOWN:
                        # 悔棋按钮
                        if 500 < event.pos[0] < 550 and 450 < event.pos[1] < 478:
                            self.text5_surface = self.font.render(u'悔棋', True, (0, 0, 0), (0, 255, 0))
                            self.screen.blit(self.text5_surface, (500, 450))
                            pygame.display.update()
                            # pygame.image.save(self.text5_surface, "source/image/text5_1.png")
                    if event.type == MOUSEBUTTONUP:
                        if 500 < event.pos[0] < 550 and 450 < event.pos[1] < 478:
                            self.text5_surface = self.font.render(u'悔棋', True, (0, 0, 0), (255, 255, 255))
                            self.chess_regret()

                elif self.chess_start == 0:
                    # start按钮实现
                    if event.type == MOUSEBUTTONDOWN:
                        if 500 < event.pos[0] < 550 and 400 < event.pos[1] < 428:
                            self.text3_surface = self.font.render(u'Start', True, (0, 0, 0), (0, 255, 0))
                            self.screen.blit(self.text3_surface, (500, 400))
                            pygame.display.update()
                            # pygame.image.save(self.text3_surface, "source/image/text3_1.png")
                    if event.type == MOUSEBUTTONUP:
                        if 500 < event.pos[0] < 550 and 400 < event.pos[1] < 428:
                            self.text3_surface = self.font.render(u'Start', True, (0, 0, 0), (255, 255, 255))
                            self.chess_start = 1
                            self.chess_white_list = []
                            self.chess_black_list = []
                            self.chess_result = ''
                            self.text12_surface = self.font.render(u'', True, (0, 0, 0))
                            self.start_time = time.time()

                    # 先手选择
                    if event.type == MOUSEBUTTONDOWN:
                        if 500 < event.pos[0] < 575 and 100 < event.pos[1] < 128:
                            self.text1_surface = self.font.render(u'玩家先', True, (0, 0, 0), (0, 255, 0))
                            # pygame.image.save(self.text1_surface, "source/image/text1_1.png")
                            self.text2_surface = self.font.render(u'AI先', True, (0, 0, 0), (255, 255, 255))
                            self.first_step = 'P'
                    if event.type == MOUSEBUTTONDOWN:
                        if 500 < event.pos[0] < 545 and 150 < event.pos[1] < 178:
                            self.text2_surface = self.font.render(u'AI先', True, (0, 0, 0), (0, 255, 0))
                            # pygame.image.save(self.text2_surface, "source/image/text2_1.png")
                            self.text1_surface = self.font.render(u'玩家先', True, (0, 0, 0), (255, 255, 255))
                            self.first_step = 'C'

                    # 难度选择
                    if event.type == MOUSEBUTTONDOWN:
                        if 500 < event.pos[0] < 525 and 250 < event.pos[1] < 278:
                            self.text7_surface = self.font.render(u'低', True, (0, 0, 0), (0, 255, 0))
                            # pygame.image.save(self.text7_surface, "source/image/text7_1.png")
                            self.text8_surface = self.font.render(u'中', True, (0, 0, 0), (255, 255, 255))
                            self.text9_surface = self.font.render(u'高', True, (0, 0, 0), (255, 255, 255))
                            self.chess_depth = 1
                    if event.type == MOUSEBUTTONDOWN:
                        if 540 < event.pos[0] < 565 and 250 < event.pos[1] < 278:
                            self.text8_surface = self.font.render(u'中', True, (0, 0, 0), (0, 255, 0))
                            # pygame.image.save(self.text8_surface, "source/image/text8_1.png")
                            self.text7_surface = self.font.render(u'低', True, (0, 0, 0), (255, 255, 255))
                            self.text9_surface = self.font.render(u'高', True, (0, 0, 0), (255, 255, 255))
                            self.chess_depth = 2
                    if event.type == MOUSEBUTTONDOWN:
                        if 580 < event.pos[0] < 605 and 250 < event.pos[1] < 278:
                            self.text9_surface = self.font.render(u'高', True, (0, 0, 0), (0, 255, 0))
                            # pygame.image.save(self.text9_surface, "source/image/text9_1.png")
                            self.text7_surface = self.font.render(u'低', True, (0, 0, 0), (255, 255, 255))
                            self.text8_surface = self.font.render(u'中', True, (0, 0, 0), (255, 255, 255))
                            self.chess_depth = 3

            # print self.chess_list
            # for m in range(1, 16, 2):
            #     for n in range(1, 16, 2):
            #         self.check_place(m, n, 'black')
            #         self.check_place(m, n+1, 'white')
            # print self.chess_black_list
            # print self.chess_white_list
            # print self.chess_both_list

    def game_start(self):
        pass

    def check_place(self, x, y, color):
        # 棋子摆放
        if color == 'white':
            self.screen.blit(self.chess_white, (-11 - 16 + x * 32, -10 - 16 + y * 32))
        elif color == 'black':
            self.screen.blit(self.chess_black, (-11 - 16 + x * 32, -10 - 16 + y * 32))

    def get_mouse(self):
        # 得到鼠标的位置
        x, y = pygame.mouse.get_pos()  # 获取当前鼠标坐标
        # pygame.mouse.set_visible(False)
        if 0 < x < 489 and 0 < y < 488:
            x -= self.chess_white.get_width()/2
            y -= self.chess_white.get_height()/2
            # 计算图标左上角的位置
            if self.first_step == 'C':
                self.screen.blit(self.chess_white, (x, y))  # 将图标画上
            elif self.first_step == 'P':
                self.screen.blit(self.chess_black, (x, y))

    def get_mouseButton(self, event):
        # 得到玩家落子位置并落子
        (x, y) = event.pos
        x_mod, y_mod = x % 32, y % 32
        if 30 > x_mod > 10 and 31 > y_mod > 11:
            x = x/32 + 1
            y = y/32 + 1
            if 0 < x < 16 and 0 < y < 16:
                if (x, y) not in self.chess_both_list:
                    self.chess_update_place(x, y)
                    return 1
        return 0

    def get_ai_pos(self):
        # AI数据获取
        if self.first_step == 'P':
            who_put = 2
        else:
            who_put = 1
        # black =1 ; white =2

        s = searcher()
        s.board = self.board
        score, row, col = s.search(who_put, self.chess_depth)
        return row+1, col+1

    def get_ai_place(self):
        # 得到AI位置并落子
        # self.chess_list_opp = list(set(self.chess_list_all)-set(self.chess_both_list))
        # x, y = random.choice(self.chess_list_opp)
        x, y = self.get_ai_pos()
        if (x, y) not in self.chess_both_list:
            self.chess_update_place(x, y)
            return 1
        return 0

    def chess_update_place(self, x, y):
        # 更新list数据和next数据，并更新棋子
        if self.chess_next == 'black':
            self.chess_black_list.append((x, y))
            self.chess_both_list.append((x, y))
            self.chess_list_opp = list(set(self.chess_list_all)-set(self.chess_both_list))
            self.board[x-1][y-1] = 1
            self.last_pos = (x, y)
            for x, y in self.chess_white_list:
                self.check_place(x, y, 'white')
            for x, y in self.chess_black_list:
                self.check_place(x, y, 'black')
            self.chess_next = 'white'
            pygame.display.update()
            self.check_winner()

        elif self.chess_next == 'white':
            self.chess_white_list.append((x, y))
            self.chess_both_list.append((x, y))
            self.chess_list_opp = list(set(self.chess_list_all)-set(self.chess_both_list))
            self.board[x-1][y-1] = 2
            self.last_pos = (x, y)
            for x, y in self.chess_white_list:
                self.check_place(x, y, 'white')
            for x, y in self.chess_black_list:
                self.check_place(x, y, 'black')
            self.chess_next = 'black'
            pygame.display.update()
            self.check_winner()

    def chess_place(self):
        # 只摆放好棋子，不更新数据
        for x, y in self.chess_white_list:
            self.check_place(x, y, 'white')
        for x, y in self.chess_black_list:
            self.check_place(x, y, 'black')

    def check_winner(self):
        # 判断胜负
        if len(self.chess_list_opp) == 0:
            self.chess_result = 'game over !'
            self.text12_surface = self.font.render(u'game over !', True, (0, 0, 0), (0, 255, 0))
            # pygame.image.save(self.text12_surface, "source/image/text12_1.png")
            return 1
        else:
            x, y = self.last_pos
            table = []
            value = ''
            if (x, y) in self.chess_white_list:
                table = self.chess_white_list
                value = 'white'
            elif (x, y) in self.chess_black_list:
                table = self.chess_black_list
                value = 'black'
            list_direction = [0, 0, 0, 0]

            for i in range(1, 5):
                if x+i > self.size_x:
                    break
                elif (x+i, y) in table:
                    list_direction[0] += 1
                else:
                    break

            for i in range(1, 5):
                if x+i > self.size_x or y-i < 0:
                    break
                elif (x+i, y-i) in table:
                    list_direction[1] += 1
                else:
                    break

            for i in range(1, 5):
                if y-i < 0:
                    break
                elif (x, y-i) in table:
                    list_direction[2] += 1
                else:
                    break

            for i in range(1, 5):
                if y-i < 0 or x-i < 0:
                    break
                elif (x-i, y-i) in table:
                    list_direction[3] += 1
                else:
                    break

            for i in range(1, 5):
                if x-i < 0:
                    break
                elif (x-i, y) in table:
                    list_direction[0] += 1
                else:
                    break

            for i in range(1, 5):
                if x-i < 0 or y+i > self.size_y:
                    break
                elif (x-i, y+i) in table:
                    list_direction[1] += 1
                else:
                    break

            for i in range(1, 5):
                if y+i > self.size_y:
                    break
                elif (x, y+i) in table:
                    list_direction[2] += 1
                else:
                    break

            for i in range(1, 5):
                if x+i > self.size_x or y+i > self.size_y:
                    break
                elif (x+i, y+i) in table:
                    list_direction[3] += 1
                else:
                    break
            # print list_direction

            if list_direction[0] >= 4 or list_direction[1] >= 4 or list_direction[2] >= 4 or list_direction[3] >= 4:
                if (self.first_step == 'P' and value == 'black') or (self.first_step == 'C' and value == 'white'):
                    self.chess_result = 'You win !'
                    self.text12_surface = self.font.render(u'You win !', True, (0, 0, 0), (0, 255, 0))
                    # pygame.image.save(self.text12_surface, "source/image/text12_2.png")
                else:
                    self.chess_result = 'You lost !'
                    self.text12_surface = self.font.render(u'You lost !', True, (0, 0, 0), (0, 255, 0))
                    # pygame.image.save(self.text12_surface, "source/image/text12_3.png")
                # print self.chess_result
                return 1

    def start_new(self):
        # 恢复开始的设置和参数，除了self.chess_white_list和self.chess_black_list，用于保持棋盘形状
        self.chess_next = 'black'
        self.ai_tem = 1
        # self.chess_white_list = []
        # self.chess_black_list = []
        self.chess_both_list = []
        self.last_pos = (0, 0)  # 最近落子的位置
        self.chess_list_opp = list(set(self.chess_list_all)-set(self.chess_both_list))
        self.board = [[0 for n in xrange(self.size_y)] for m in xrange(self.size_x)]
        self.chess_start = 0

    def chess_regret(self):
        # 悔棋函数
        if self.first_step == 'P':
            if len(self.chess_black_list) > 1:
                self.chess_white_list = self.chess_white_list[:len(self.chess_white_list)-1]  # 白棋列表
                self.chess_black_list = self.chess_black_list[:len(self.chess_black_list)-1]  # 黑棋列表
                self.chess_both_list = self.chess_white_list + self.chess_black_list  # 白棋和黑棋列表
                self.chess_list_opp = list(set(self.chess_list_all)-set(self.chess_both_list))  # 反列表
                self.board = [[0 for n in xrange(self.size_y)] for m in xrange(self.size_x)]  # 棋盘阵列图
                for x, y in self.chess_white_list:
                    self.board[x-1][y-1] = 2
                for x, y in self.chess_black_list:
                    self.board[x-1][y-1] = 1
                self.last_pos = self.chess_white_list[len(self.chess_white_list)-1]  # 最近1个落子的位置
            elif len(self.chess_black_list) == 1:
                self.chess_white_list = self.chess_white_list[:len(self.chess_white_list)-1]  # 白棋列表
                self.chess_black_list = self.chess_black_list[:len(self.chess_black_list)-1]  # 黑棋列表
                self.chess_both_list = self.chess_white_list + self.chess_black_list  # 白棋和黑棋列表
                self.chess_list_opp = list(set(self.chess_list_all)-set(self.chess_both_list))  # 反列表
                self.board = [[0 for n in xrange(self.size_y)] for m in xrange(self.size_x)]  # 棋盘阵列图
                self.last_pos = (0, 0)  # 最近1个落子的位置

        else:
            if len(self.chess_white_list) > 1:
                self.ai_tem = 2
                self.chess_white_list = self.chess_white_list[:len(self.chess_white_list)-1]  # 白棋列表
                self.chess_black_list = self.chess_black_list[:len(self.chess_black_list)-1]  # 黑棋列表
                self.chess_both_list = self.chess_white_list + self.chess_black_list  # 白棋和黑棋列表
                self.chess_list_opp = list(set(self.chess_list_all)-set(self.chess_both_list))  # 反列表
                self.board = [[0 for n in xrange(self.size_y)] for m in xrange(self.size_x)]  # 棋盘阵列图
                for x, y in self.chess_white_list:
                    self.board[x-1][y-1] = 2
                for x, y in self.chess_black_list:
                    self.board[x-1][y-1] = 1
                self.last_pos = self.chess_black_list[len(self.chess_black_list)-1]  # 最近1个落子的位置
            elif len(self.chess_black_list) == 1:
                self.chess_white_list = self.chess_white_list[:len(self.chess_white_list)-1]  # 白棋列表
                self.chess_black_list = self.chess_black_list[:len(self.chess_black_list)-1]  # 黑棋列表
                self.chess_both_list = self.chess_white_list + self.chess_black_list  # 白棋和黑棋列表
                self.chess_list_opp = list(set(self.chess_list_all)-set(self.chess_both_list))  # 反列表
                self.board = [[0 for n in xrange(self.size_y)] for m in xrange(self.size_x)]  # 棋盘阵列图
                for x, y in self.chess_black_list:
                    self.board[x-1][y-1] = 1
                self.last_pos = self.chess_black_list[len(self.chess_black_list)-1]  # 最近1个落子的位置


def main():
    game = ChessPlay()

if __name__ == '__main__':
    main()

