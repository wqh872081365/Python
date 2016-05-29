# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import sys
from scrapy_lagou.items import ScrapyLagouItem
from scrapy_lagou.items import LagouDescription
from scrapy.exceptions import DropItem
# from scrapy import signals
# from scrapy.xlib.pydispatch import dispatcher
from scrapy.exceptions import CloseSpider

import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi

from scrapy import log

'''
class ScrapyLagouPipeline(object):
    def process_item(self, item, spider):
        return item
'''


class JsonWriterPipeline(object):
    # json数据保存

    def __init__(self):
        self.file1 = None
        self.job = ''
        self.job_temp = []

        # self.file2 = None
        self.number = 1  # 爬取后保存的数量
        # self.url_dict = {}

        # dispatcher.connect(self.open_spider, signals.spider_opened)
        # dispatcher.connect(self.close_spider, signals.spider_closed)

    '''
    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"  # json设置为非ascii解析
        self.file.write(line)
        return item
    '''

    def process_item(self, item, spider):
        if type(item) == ScrapyLagouItem:
            line = json.dumps(dict(item), ensure_ascii=False) + "\n"  # json设置为非ascii解析
            self.job_temp.append(line)
        elif type(item) == LagouDescription:
            url = item['positionURL']
            desc = item['positionDescription']
            for k, v in enumerate(self.job_temp):
                if url in v:
                    self.job = v.replace('}', ', "positionDescription": "'+desc+' '+str(self.number)+'"}')
                    self.file1.write(self.job)
                    # self.url_dict[str(self.number)] = url
                    # url_cur = str(self.url_dict) + "\r"  # json设置为非ascii解析
                    # self.file2.write(json.dumps(url_cur))
                    # self.url_dict = {}
                    self.number += 1
                    self.job_temp.pop(k)
                    break
        return item

    def open_spider(self, spider):
        self.file1 = open('lagou_jobs.json', 'w')
        # self.file2 = open('lagou_urls.json', 'w')

    def close_spider(self, spider):
        self.file1.close()
        # self.file2.close()


class MySQLLaGouPipeline(object):
    # MySQL数据保存

    def __init__(self):
        self.dbpool = adbapi.ConnectionPool("MySQLdb", host="127.0.0.1", user="root", passwd="password", db="lagou_job",
                                            charset='utf8', use_unicode=False, cursorclass=MySQLdb.cursors.DictCursor)

    def process_item(self, item, spider):
        db = self.dbpool.runInteraction(self._insert_recode, item)
        db.addErrback(self._handle_error, item, spider)
        return item

    def _insert_recode(self, conn, item):
        # 将爬取的数据插入到MySQL
        if type(item) == ScrapyLagouItem:
            item['positionDescription'] = ''
            conn.execute("""INSERT IGNORE INTO lagou_jobs(city, industryField, education, workYear, positionAdvantage,
            createTime, salary, salaryMin, salaryMax, positionName, companyName, companySize, financeStage, jobNature,
            positionType, district, companyLabelList, positionId, positionURL, positionDescription) VALUES ('%s','%s',
            '%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')""" %
            (item['city'], item['industryField'], item['education'], item['workYear'],
            item['positionAdvantage'], item['createTime'], item['salary'], item['salaryMin'],
            item['salaryMax'], item['positionName'], item['companyName'], item['companySize'],
            item['financeStage'], item['jobNature'], item['positionType'], item['district'],
            item['companyLabelList'], item['positionId'], item['positionURL'], item['positionDescription']))

        elif type(item) == LagouDescription:
            # print item['positionDescription'], 2
            conn.execute("UPDATE lagou_jobs SET positionDescription = '%s' WHERE positionId = '%s'" % (item['positionDescription'], item['positionId']))

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        self.dbpool.close()

    def _handle_error(self, error, item, spider):
        log.err(error)


class DuplicatesPipeline(object):
    # 去重

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        # print type(item)
        if type(item) == ScrapyLagouItem:
            if item['positionId'] in self.ids_seen:
                raise DropItem("Duplicate item found: %s" % item['positionId'])
            else:
                self.ids_seen.add(item['positionId'])
            # print self.ids_seen

        elif type(item) == LagouDescription:
            pass

        return item

