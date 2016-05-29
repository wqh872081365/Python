#!/usr/bin/env python
# -*- coding:utf-8 -*-

import scrapy
import json
import sys
import re
import time
from scrapy_lagou.items import ScrapyLagouItem
from scrapy_lagou.items import LagouDescription


class Lagou_Job_Spider(scrapy.Spider):
    name = 'lagou_job'
    allowed_domains = ['lagou.com']

    kds = ['Python', 'Java', 'PHP', 'C', 'C++', '.NET', 'C#', 'Android', 'iOS', 'Hadoop', 'Node.js', 'Go', 'VB',
           'JavaScript', 'ASP', 'MySQL', 'Oracle', 'MongoDB', u'数据挖掘', u'大数据', u'机器学习']  # 爬取方向
    citys = ['上海', '北京', '杭州', '深圳', '广州', '南京', '苏州', '天津', '无锡', '宁波', '厦门', '成都']  # 爬取城市

    # start_urls = [
    #     'http://www.lagou.com/jobs/list_Python?px=new&city=%E4%B8%8A%E6%B5%B7'
    # ]
    totalPageCount = 0  # 总页数
    curpage = 1  # 当前页
    curcity = 0  # 当前城市
    curkd = 0  # 当前方向

    kd = kds[curcity]  # POST数据
    city = citys[curkd]  # POST数据

    def start_requests(self):
        # 首个爬取数据
        return [scrapy.http.FormRequest("http://www.lagou.com/jobs/positionAjax.json?px=new&city="+self.city,
                                        formdata={'pn': str(self.curpage), 'kd': self.kd},
                                        callback=self.parse)]

    def parse(self, response):
        # jobs爬取函数
        '''
        f = open('index.html', 'w')
        f.write(response.body)
        f.close()


        for sel in response.xpath('//*[@id="s_position_list"]/ul/li/div[1]/div[1]/div[1]/a/@href'):
            print sel
            url = sel.extract()
            print url
            # yield scrapy.http.Request(url, callback=self.parse_list)
        '''
        # print response.body_as_unicode()
        json_jobs = json.loads(response.body_as_unicode())
        # print json_jobs
        json_jobs = json_jobs['content']['positionResult']['result']
        # 调用body_as_unicode()是为了能处理unicode编码的数据
        self.totalPageCount = (json.loads(response.body_as_unicode())['content']['positionResult']['totalCount']-1)/15+1
        if self.totalPageCount > 15:
            self.totalPageCount = 15
        for json_job in json_jobs:
            job = ScrapyLagouItem()
            job['city'] = json_job['city'].encode('utf-8')
            job['industryField'] = json_job['industryField'].encode('utf-8')
            job['education'] = json_job['education'].encode('utf-8')
            job['workYear'] = json_job['workYear'].encode('utf-8')
            job['positionAdvantage'] = json_job['positionAdvantage'].encode('utf-8')
            job['createTime'] = json_job['createTime'].encode('utf-8')
            job['salary'] = json_job['salary'].encode('utf-8')
            if '-' in json_job['salary'].encode('utf-8'):
                job['salaryMin'] = json_job['salary'].split('-', 1)[0].encode('utf-8')
                job['salaryMax'] = json_job['salary'].split('-', 1)[1].encode('utf-8')
            job['positionName'] = json_job['positionName'].encode('utf-8')
            job['companyName'] = json_job['companyName'].encode('utf-8')
            job['companySize'] = json_job['companySize'].encode('utf-8')
            job['financeStage'] = json_job['financeStage'].encode('utf-8')
            job['jobNature'] = json_job['jobNature'].encode('utf-8')
            job['positionType'] = json_job['positionType'].encode('utf-8')
            if json_job['district']:
                job['district'] = json_job['district'].encode('utf-8')
            job['companyLabelList'] = '\n'.join(json_job['companyLabelList']).encode('utf-8')

            job['positionId'] = str(json_job['positionId']).encode('utf-8')
            job['positionURL'] = 'http://www.lagou.com/jobs/'+str(json_job['positionId'])+'.html'
            # job['positionDescription'] = ''

            # job['title'] = response.xpath('//dt').extract()[0].encode('utf-8')
            # job['position'] = response.xpath('//').extract()[2].encode('utf-8').lstrip().rstrip()
            # job['salaryMin'] = job['salary'].split('-', 1)[0]
            # job['publishSource'] = response.xpath('//').extract()[0].encode('utf-8').split(' ', 1)[1]
            # job['workAddress'] = ''.join(response.xpath('').extract()).encode('utf-8').strip().replace(' ', '').replace('\n', '')
            # str = json.dumps(dict(job), ensure_ascii=False)  # json设置为非ascii解析,变为unicode
            # str = unicode.encode(str, 'utf-8')
            # str = eval(str)
            # str = ScrapyLagouItem(str)
            # print job['workAddress']
            yield job

            yield scrapy.Request(job['positionURL'], callback=self.parse_desc)

        if self.curpage < self.totalPageCount:
            self.curpage += 1
            yield scrapy.http.FormRequest("http://www.lagou.com/jobs/positionAjax.json?px=new&city="+self.city,
                                          formdata={'pn': str(self.curpage), 'kd': self.kd},
                                          callback=self.parse)

        elif self.curkd < len(self.kds)-1:
            self.curpage = 1
            self.totalPageCount = 0
            self.curkd += 1
            self.kd = self.kds[self.curkd]
            yield scrapy.http.FormRequest("http://www.lagou.com/jobs/positionAjax.json?px=new&city="+self.city,
                                          formdata={'pn': str(self.curpage), 'kd': self.kd},
                                          callback=self.parse)

        elif self.curcity < len(self.citys)-1:
            self.curpage = 1
            self.totalPageCount = 0
            self.curkd = 0
            self.curcity += 1
            self.kd = self.kds[self.curkd]
            self.city = self.citys[self.curcity]
            yield scrapy.http.FormRequest("http://www.lagou.com/jobs/positionAjax.json?px=new&city="+self.city,
                                          formdata={'pn': str(self.curpage), 'kd': self.kd},
                                          callback=self.parse)

    def parse_desc(self, response):
        # 工作描述爬取函数
        desc = LagouDescription()
        re_id = re.compile(r'\d{4,7}')
        desc['positionId'] = (re.search(re_id, response.url)).group()
        desc['positionURL'] = response.url
        subtree_root = response.xpath('//*[@id="container"]/div[1]/dl[1]/dd[2]')
        desc['positionDescription'] = ''.join([text.extract().strip() for text in subtree_root.xpath('.//text()')]).strip().replace('\n', '').encode('utf-8')
        # print desc['positionDescription']
        yield desc
