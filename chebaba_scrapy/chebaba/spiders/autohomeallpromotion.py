# -*- coding: utf-8 -*-
#!/usr/bin/env python

# scrapy crawl autohomeallpromotion -s JOBDIR=autohomeallpromotion

import sys, time
from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from scrapy.http import Request
from chebaba.items import AutohomeAllPromotionItem
import urllib, urllib2#, json
#from simplemysql import SimpleMysql
from HTMLParser import HTMLParser

#db = SimpleMysql(host = '127.0.0.1', db = 'wholenetwork', user = 'root', passwd = 'root')
PAGE_COUNT = 10
API_ADDRESS = 'http://localhost/api/promotion'

def doPost(url, item):
    if not item: return
    request = urllib2.Request(url, urllib.urlencode(item))
    response = urllib2.urlopen(request).read()
    #return json.loads(response)
'''
def doSave(item):
    item['prices'] = str(item['prices']).replace("u'", "'")
    return db.insert('autohome_allpromotion', item)
'''
def filt(string, start, end):
    if not string: return
    i = string.find(start) + len(start)
    j = string[i:].find(end)
    return string[i : i + j]

def stripTags(html):
    html = html.strip().strip('\r').strip('\n').strip(u' ')
    result = []
    parser = HTMLParser()
    parser.handle_data = result.append
    parser.feed(html)
    parser.close()
    return ''.join(result)

class AutohomeAllPromotionSpider(BaseSpider):
    reload(sys)
    sys.setdefaultencoding('utf-8')

    name = 'autohomeallpromotion'
    allowed_domains = ['dealer.autohome.com.cn']
    start_urls = ['http://dealer.autohome.com.cn/china/']

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
        promotions = sel.xpath('//p[@class="name font-yh"]')
        for promotion in promotions:
            url = response.urljoin(promotion.xpath('a/@href').extract()[0])
            yield Request(url, self.parsePromotion)

        np = sel.xpath('//a[@class="page-next "]/@href').extract()
        pn = sel.xpath('//div[@class="page dealer-page"]/a[@class="current"]/text()').extract()
        if np and pn:
            if int(pn[0]) <= PAGE_COUNT:
                yield Request(response.urljoin(np[0]), self.parsePromotionList)

    def parsePromotion(self, response):
        sel = Selector(response)
        item = AutohomeAllPromotionItem()

        tmp = sel.xpath('//p[@class="cont-time"]/text()')
        if not tmp: tmp = sel.xpath('//span[@class="red"]/text()')
        if not tmp: return
        tmp = tmp.extract()[0].replace(u'促销时间', '')
        if u'.' in tmp: tmp = tmp.split(u'-')   # 2015.05.31-2015.06.04
        else: tmp = tmp.split(u' - ')           # 2015-05-31 - 2015-06-04
        item['datefrom'] = tmp[0]
        item['dateto'] = tmp[1]

        tmp = sel.xpath('//div[@class="dealertext"]/p[2]')
        if tmp: item['content'] = stripTags(tmp.extract()[0])
        else: return

        item['city'] = sel.xpath('//div[@class="breadnav"]/a[2]/text()').extract()[0]
        item['title'] = sel.xpath('//p[@class="title-text"]/text()').extract()[0]

        tmp = sel.xpath('//input[@id="SeriesName"]/@value').extract()
        if tmp: item['series_name'] = tmp[0]
        else: tmp = sel.xpath('//p[@class="name-text font-yh"]/a/text()').extract()
        if not tmp: return
        item['series_name'] = tmp[0]

        tmp = sel.xpath('//input[@id="SeriesId"]/@value').extract()
        if tmp: item['series_id'] = tmp[0]
        else:
            tmp = sel.xpath('//p[@class="name-text font-yh"]/a/@href').extract()
            if tmp: item['series_id'] = filt(tmp[0], 'b_', '.')
            else: return

        tmp = sel.xpath('//div[@class="brandtree-name"]')
        tmps = ''
        for t in tmp: tmps += t.xpath('p[@class="text"]/text()').extract()[0] + ','
        item['brand'] = tmps[:-1]
        item['pageurl'] = response.url

        tables = sel.xpath('//div[@class="dealertext"]/table/tbody/tr')
        ts = []
        if tables:
            for table in tables:
                t = {}
                tmp = table.xpath('td[4]/a/@href')
                if not tmp: continue # filt th row
                t['modelid'] = filt(tmp.extract()[0], 'order_'+item['series_id']+'_', '.')
                t['model'] = table.xpath('td[1]/text()').extract()[0].replace(item['series_name'] + ' ', '').replace(u' ', '')
                t['off'] = stripTags(table.xpath('td[3]').extract()[0].replace(u'↓', '').replace('\r\n', '').replace(u' ', ''))
                ts.append(t)
        item['prices'] = ts
        item['brand_id'] = 2
        item['dealer'] = sel.xpath('//div[@class="text-main"]/text()').extract()[0]
        item['dealerid'] = sel.xpath('//li[@id="nav_0"]/a/@href').extract()[0].replace('/', '')
        #tmp = doPost(API_ADDRESS, item)
        doPost(API_ADDRESS, item)
        #if doSave(item):
        #print '\t', 'city:', item['city'], 'dealer:', item['dealer'], item['series_name'], item['title'], tmp['error'], tmp['msg']
