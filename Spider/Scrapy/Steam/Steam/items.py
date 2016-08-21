# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SteamItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    appid = scrapy.Field()
    url = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    name = scrapy.Field()
    platform = scrapy.Field()
    release = scrapy.Field()
    summary = scrapy.Field()
    summary_detail = scrapy.Field()
    discount = scrapy.Field()
    price = scrapy.Field()
    price_old = scrapy.Field()


class SteamDescItem(scrapy.Item):
    url = scrapy.Field()
    id = scrapy.Field()
    desc = scrapy.Field()
    player = scrapy.Field()
    tag = scrapy.Field()
