import scrapy
import re
from Scrapy_Study1.items import ScrapyStudy1Item


class DmozSpider(scrapy.spiders.Spider):
    name = 'dmoz'
    allowed_urls = ['dmoz.org']
    start_urls = [
        'http://www.dmoz.org/Computers/Programming/Languages/Python/Books/',
        'http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/'
    ]


#    def parse(self, response):
#        filename = response.url.split('/')[-2]
#        with open(filename, 'wb') as f:
#            f.write(response.body)


    def parse(self, response):
        for sel in response.xpath('//ul[@class="directory-url"]/li'):
            item = ScrapyStudy1Item()
            item['title'] = sel.xpath('a/text()').extract()
            item['link'] = sel.xpath('a/@href').extract()
            item['desc'] = sel.xpath('text()').re('-\s[^\n]*\\r')
            yield item
