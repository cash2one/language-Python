# -*- coding: utf-8 -*-
#!/usr/bin/env python

import sys, time
from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from scrapy.http import Request
from chebaba.items import AutohomeArticleItem
import urllib, urllib2, json
from simplemysql import SimpleMysql

AUTOHOME_ARTICLE_URL = ''
ALL_DEALERS = []

def doPost(url, data):
    if not data: return
    request = urllib2.Request(url, urllib.urlencode(data))
    response = urllib2.urlopen(request).read()
    result = json.loads(response)
    print '\t', result['error'], result['msg']

class AutohomeArticleSpider(BaseSpider):
    reload(sys)
    sys.setdefaultencoding('utf-8')

    name = 'autohomearticle'
    allowed_domains = ['dealer.autohome.com.cn']
    urls = []
    for dealer in ALL_DEALERS:
        urls.append('http://dealer.autohome.com.cn/' + str(dealer) + '/newslist.html')
    start_urls = urls

    def parse(self, response):
        sel = Selector(response)

        trs = sel.xpath('//dl[@class="promot-dl "]/dd/p/a/@href').extract()
        for tr in trs:
            url = response.urljoin(tr)
            yield Request(url, self.parseArticle)

        np = sel.xpath('//a[@class="page-next "]/@href').extract()
        if np:
            url = response.urljoin(np[0])
            yield Request(url, self.parse)

    def parseArticle(self, response):
        sel = Selector(response)

        item = AutohomeArticleItem()
        item['title'] = sel.xpath('//p[@class="title-text"]/text()').extract()[0]
        item['content'] = sel.xpath('//div[@class="dealertext"]').extract()[0]
        item['series_name'] = sel.xpath('//input[@id="SeriesName"]/@value').extract()[0]
        item['brand_id'] = 2
        print item['title'], item['series_name'], item['content'],
        doPost(AUTOHOME_ARTICLE_URL, item)
