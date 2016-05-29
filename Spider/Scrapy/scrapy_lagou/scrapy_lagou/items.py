# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyLagouItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    city = scrapy.Field()  # 城市
    industryField = scrapy.Field()  # 公司领域
    education = scrapy.Field()  # 学历要求
    workYear = scrapy.Field()  # 工作年限
    positionAdvantage = scrapy.Field()  # 职位诱惑
    createTime = scrapy.Field()  # 发布时间
    salary = scrapy.Field()  # 待遇
    salaryMin = scrapy.Field()  # 最低待遇
    salaryMax = scrapy.Field()  # 最高待遇
    positionName = scrapy.Field()  # 职位
    companyName = scrapy.Field()  # 公司
    companySize = scrapy.Field()  # 公司规模
    financeStage = scrapy.Field()  # 公司发展
    jobNature = scrapy.Field()  # 全职or实习
    positionType = scrapy.Field()  # 工作类型
    district = scrapy.Field()  # 工作地区
    companyLabelList = scrapy.Field()  # 工作福利
    positionId = scrapy.Field()  # url ID
    positionURL = scrapy.Field()  # url
    positionDescription = scrapy.Field()  # 工作描述


class LagouDescription(scrapy.Item):
    positionId = scrapy.Field()  # url ID
    positionURL = scrapy.Field()  # url
    positionDescription = scrapy.Field()  # 工作描述
