# -*- coding: utf-8 -*-
#!/usr/bin/env python

# scrapy crawl autohomeallpromotion
# scrapy crawl autohomeallpromotion -s JOBDIR=autohomeallpromotion

import sys, datetime, urllib, urllib2, json
from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from scrapy.http import Request
from chebaba.items import AutohomeAllPromotionTitleItem
from simplemysql import SimpleMysql
from HTMLParser import HTMLParser

ISSAVE = False
ISPOST = False
NISSAN_ONLY = False
if ISSAVE: db = SimpleMysql(host = '127.0.0.1:5029', db = 'wholenetwork', user = 'root', passwd = '')

def doSave(item):
    #return db.insert('autohome_allpromotiontitle', item)
    return db.insertOrUpdate('autohome_allpromotiontitle', item, ['titleid','pubdate'])

def getBrands(array):
    if not array: return None
    brands = []
    for a in array:
        if a:
            brands.append(a.extract())
    return brands

def getBrand(brands, title):
    if (not brands) or (not title): return None
    for brand in brands:
        if brand in title: return brand
    return None

def filt(string, start, end):
    if not string: return
    i = string.find(start) + len(start)
    j = string[i:].find(end)
    return string[i : i + j]

class AutohomeAllPromotionSpider(BaseSpider):
    reload(sys)
    sys.setdefaultencoding('utf-8')

    name = 'autohomeallpromotiontitle'
    allowed_domains = ['dealer.autohome.com.cn']
    start_urls = ['http://dealer.autohome.com.cn/china/']
    if NISSAN_ONLY:
        start_urls = [
            'http://dealer.autohome.com.cn/china/0_63_0_92_1.html',    #东风日产
            'http://dealer.autohome.com.cn/china/0_63_0_73_1.html',    #进口日产
        ]

    def parse(self, response):
        sel = Selector(response)
        dlrs = sel.xpath('//h3[@class="dealer-cont-title"]/a[1]/@href').extract()
        for dlr in dlrs:
            url = response.urljoin('newslist.html').replace('china', filt(dlr, '.cn/', '/'))
            yield Request(url, self.parsePromotionList)

        np = sel.xpath('//a[@class="page-item-next"]/@href').extract()
        if np: yield Request(response.urljoin(np[0]), self.parse)

    def parsePromotionList(self, response):
        sel = Selector(response)
        item = AutohomeAllPromotionTitleItem()
        ISNEXT = True

        item['city'] = sel.xpath('//div[@class="breadnav"]/a[2]/text()').extract()[0]
        item['dealer'] = sel.xpath('//div[@class="text-main"]/text()').extract()[0]
        item['dealerid'] = sel.xpath('//li[@id="nav_0"]/a/@href').extract()[0].replace('/', '')
        tmp = sel.xpath('//div[@class="brandtree-name"]')
        tmps = ''
        for t in tmp: tmps += t.xpath('p[@class="text"]/text()').extract()[0] + ','
        item['manu'] = tmps[:-1]
        brands = sel.xpath('//div[@class="screen"]/dl[2]/dd/a/text()')
        self.logger.info(item['city'] + ', ' + item['manu'] + ', ' + item['dealer'])

        lsts = sel.xpath('//div[@class="dealeron-cont"]/dl/dd')
        for lst in lsts:
            item['pubdate'] = lst.xpath('p[@class="date"]/span/text()').extract()[0].replace(u'发布时间：', '')
            ISNEXT = datetime.datetime.strptime(item['pubdate'], "%Y-%m-%d").date() >= datetime.date(2015,6,1)
            item['title'] = lst.xpath('p[@class="name font-yh"]/a/text()').extract()[0]
            item['titleid'] = filt(lst.xpath('p[@class="name font-yh"]/a/@href').extract()[0], 'news_', '.html')
            item['pageurl'] = response.urljoin(lst.xpath('p[@class="name font-yh"]/a/@href').extract()[0])
            item['brand'] = getBrand(getBrands(brands), item['title'])
            #self.logger.info('\t' + str(ISNEXT) + ', ' + item['pubdate'] + '\t' + item['title'])
            if item['brand'] and ISSAVE and ISNEXT: doSave(item)

        if ISNEXT:
            np = sel.xpath('//a[@class="page-next "]/@href').extract()
            if np: yield Request(response.urljoin(np[0]), self.parsePromotionList)
