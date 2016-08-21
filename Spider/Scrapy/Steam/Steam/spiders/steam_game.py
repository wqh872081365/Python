#!/usr/bin/env python
# -*- coding:utf-8 -*-

import scrapy
from Steam.items import SteamItem
from Steam.items import SteamDescItem

import re


class Steam_Spider(scrapy.Spider):
    name = 'steam_game'
    allowed_domains = ['store.steampowered.com', 'cdn.steamstatic.com.8686c.com/steam/apps']

    start_urls = [
        'http://store.steampowered.com/search/?page=1'
    ]

    PageCount = 1  # 总页数
    curpage = 1  # 当前页

    """
    def start_requests(self):
        # 首个爬取数据
        return [scrapy.http.FormRequest("http://store.steampowered.com/search/",
                                        formdata={'page': str(self.curpage)},
                                        callback=self.parse)]
    """

    def parse(self, response):
        # 爬取函数
        '''
        for sel in response.xpath('//*[@id="s_position_list"]/ul/li/div[1]/div[1]/div[1]/a/@href'):
            print sel
            url = sel.extract()
            print url
            # yield scrapy.http.Request(url, callback=self.parse_list)
        '''

        page_desc = response.xpath('//*[@id="search_result_container"]/div[3]/div[1]/text()').extract()[0].strip()
        res = re.compile(r'([0-9]+)')
        res_page = re.findall(res, page_desc)

        self.PageCount = int(res_page[2])/25+1

        for sel in response.xpath('//*[@id="search_result_container"]/div[2]/a'):
            game = SteamItem()
            game['appid'] = sel.xpath('@data-ds-appid').extract()[0]
            game_id = game['appid']
            game['url'] = sel.xpath('@href').extract()[0]

            game['image_urls'] = sel.xpath('div[1]/img/@src').extract()

            game['name'] = sel.xpath('div[2]/div[1]/span/text()').extract()[0]
            game['platform'] = sel.xpath('div[2]/div[1]/p/span/@class').extract()[0][13:]
            game['release'] = sel.xpath('div[2]/div[2]/text()').extract()[0]
            game['summary'] = sel.xpath('div[2]/div[3]/span/@data-store-tooltip').extract()[0].split('<br>')[0]
            game['summary_detail'] = sel.xpath('div[2]/div[3]/span/@data-store-tooltip').extract()[0].split('<br>')[1]

            if sel.xpath('div[2]/div[4]/div[1]/span'):
                game['discount'] = sel.xpath('div[2]/div[4]/div[1]/span/text()').extract()[0]
                game['price'] = sel.xpath('div[2]/div[4]/div[2]/text()').extract()[1].strip()
                game['price_old'] = sel.xpath('div[2]/div[4]/div[2]/span/strike/text()').extract()[0].strip()
            else:
                game['price'] = sel.xpath('div[2]/div[4]/div[2]/text()').extract()[0].strip()
                game['discount'] = u'0'
                game['price_old'] = game['price']

            yield scrapy.http.Request("http://store.steampowered.com/apphoverpublic/"+game_id+'?l=schinese&pagev6=true',
                                      callback=self.parse_js)

            yield game

        if self.curpage < self.PageCount:
            self.curpage += 1
            print self.curpage
            yield scrapy.http.Request("http://store.steampowered.com/search/?page="+str(self.curpage),
                                      callback=self.parse)

    def parse_js(self, response):
        des = SteamDescItem()
        des['url'] = response.url
        res = re.compile(r'([0-9]+)')
        des['id'] = re.findall(res, des['url'])[0]

        des['desc'] = response.xpath('//*[@id="hover_desc"]/text()').extract()[0].strip()

        if response.xpath('//*[@id="hover_app_'+des['id']+'"]/div[3]/div[2]/div/img/@src'):
            des['player'] = ''
            player = response.xpath('//*[@id="hover_app_'+des['id']+'"]/div[3]/div[2]/div/img/@src').extract()
            if 'http://store.akamai.steamstatic.com/public/images/v6/ico/ico_singlePlayer.png' in player:
                des['player'] += 'singlePlayer '
            if 'http://store.akamai.steamstatic.com/public/images/v6/ico/ico_multiPlayer.png' in player:
                des['player'] += 'multiPlayer '
            if 'http://store.akamai.steamstatic.com/public/images/v6/ico/ico_coop.png' in player:
                des['player'] += 'coop '

        des['tag'] = ', '.join(response.xpath('//*[@id="hover_app_'+des['id']+'"]/div[4]/div/div/text()').extract())
        yield des

