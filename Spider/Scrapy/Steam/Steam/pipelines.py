# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import sys
from Steam.items import SteamItem
from Steam.items import SteamDescItem
from scrapy.exceptions import DropItem
# from scrapy import signals
# from scrapy.xlib.pydispatch import dispatcher
from scrapy.exceptions import CloseSpider

import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi

from scrapy import log


class SteamPipeline(object):
    def process_item(self, item, spider):
        return item


class MySQLSteamPipeline(object):
    # MySQL数据保存

    def __init__(self):
        self.dbpool = adbapi.ConnectionPool("MySQLdb", host="127.0.0.1", user="root", passwd="password", db="steam_game",
                                            charset='utf8', use_unicode=False, cursorclass=MySQLdb.cursors.DictCursor)

    def process_item(self, item, spider):
        db = self.dbpool.runInteraction(self._insert_recode, item)
        db.addErrback(self._handle_error, item, spider)
        return item

    def _insert_recode(self, conn, item):
        # 将爬取的数据插入到MySQL
        if type(item) == SteamItem and item['images']:

            conn.execute("""INSERT IGNORE INTO game(appid, url, image_urls, image_path, name, platform, released,
            summary, summary_detail, discount, price, price_old) VALUES ('%s', '%s', '%s' ,'%s','%s', '%s','%s','%s',
            '%s', '%s','%s','%s')""" % (item['appid'].encode('utf-8'), item['url'].encode('utf-8'),
                                        item['image_urls'][0].encode('utf-8'), item['images'][0]['path'],
                                        item['name'].replace("'", "''").encode('utf-8'),
                                        item['platform'].replace("'", "''").encode('utf-8'),
                                        item['release'].encode('utf-8'),
                                        item['summary'].replace("'", "''").encode('utf-8'),
                                        item['summary_detail'].replace("'", "''").encode('utf-8'),
                                        item['discount'].encode('utf-8'),
                                        item['price'].replace("'", "''").encode('utf-8'),
                                        item['price_old'].replace("'", "''").encode('utf-8'),))

        elif type(item) == SteamDescItem:

            conn.execute("""UPDATE game SET des='%s', player='%s', tag='%s' WHERE appid='%s'""" %
                         (item['desc'].replace("'", "''").encode('utf-8'), item['player'],
                          item['tag'].replace("'", "''").encode('utf-8'), item['id']))

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        self.dbpool.close()

    def _handle_error(self, error, item, spider):
        log.err(error)

