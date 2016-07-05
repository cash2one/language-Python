# -*- coding: utf-8 -*-
#!/usr/bin/env python

import sys, urllib, urllib2, json
from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from scrapy.http import Request
from chebaba.items import AutohomeAllPriceItem
from simplemysql import SimpleMysql
from scrapy import log

ISSAVE = False
ISPOST = False
API_ADDRESS = ''
API_ADDRESS = ''

def filt(string, start, end):
    i = string.find(start) + len(start)
    j = string[i:].find(end)
    return string[i : i + j]

def doPost(url, item):
    data = {}
    data['dealer_name'] = item['dealer']
    data['dealer_id'] = item['dealerid']
    data['series_name'] = item['brand']
    data['series_id'] = item['brandid']
    data['title'] = item['model']
    data['id'] = item['modelid']
    data['zprice'] = item['oprice']
    data['price'] = item['price']
    request = urllib2.Request(url, urllib.urlencode(data))
    response = urllib2.urlopen(request).read()
    return json.loads(response)

class AutohomeAllPriceSpider(BaseSpider):
    reload(sys)
    sys.setdefaultencoding('utf-8')

    name = 'autohomeallprice2'
    allowed_domains = ['dealer.autohome.com.cn']
    start_urls = ['http://dealer.autohome.com.cn/china/']
    if ISPOST: start_urls = ['http://dealer.autohome.com.cn/china/0_63_0_92_1.html']

    def parse(self, response):
        sel = Selector(response)
        dlrs = sel.xpath('//h3[@class="dealer-cont-title"]/a[1]/@href').extract()
        for dlr in dlrs:
            url = response.urljoin('price.html').replace('china', filt(dlr, '.cn/', '/'))
            yield Request(url, self.parsePrice)

        np = sel.xpath('//a[@class="page-item-next"]/@href').extract()
        if np: yield Request(response.urljoin(np[0]), self.parse)

    def parsePrice(self, response):
        sel = Selector(response)
        trs = sel.xpath('//div[@class="carprice-cont"]/dl[@class="price-dl"]')
        item = AutohomeAllPriceItem()
        item['city'] = sel.xpath('//div[@class="breadnav"]/a[2]/text()').extract()[0]
        item['dealer'] = sel.xpath('//div[@class="text-main"]/text()').extract()[0]
        item['dealerid'] = sel.xpath('//li[@id="nav_0"]/a/@href').extract()[0].replace('/', '')
        tmp = sel.xpath('//div[@class="brandtree-name"]')
        tmps = ''
        for t in tmp: tmps += t.xpath('p[@class="text"]/text()').extract()[0] + ','
        item['manu'] = tmps[:-1]
        log.msg(item['city'] + ', ' + item['dealer'] + ', ' + item['manu'])

        db = SimpleMysql(host = '127.0.0.1:5029', db = 'wholenetwork', user = 'root', passwd = '')
        for tr in trs:
            item['brand'] = tr.xpath('dt[@class="fn-clear"]/div[@class="name"]/p/a/text()').extract()[0]
            item['brandid'] = filt(tr.xpath('dt[@class="fn-clear"]/div[@class="name"]/p/a/@href').extract()[0], 'cn/', '/')

            prices = tr.xpath('dd/table/tr')
            for price in prices:
                tmp = price.xpath('td[2]/p/text()').extract()
                if not tmp: continue  # filt th row
                else: item['oprice'] = tmp[0]
                item['oprice'] = item['oprice'].replace(u'万','')
                tmp = price.xpath('td[3]/div[@class="this-number red"]/a[1]/text()').extract()
                if not tmp: tmp = price.xpath('td[3]/p/a/text()').extract()
                item['price'] = tmp[0].replace(u'万','').replace(u' ','')
                item['pubdate'] = price.xpath('td[5]/text()').extract()[0].replace(u' ','').replace('\r\n','')
                tmp = price.xpath('td[1]/a/text()').extract()[0]
                item['model'] = tmp[:tmp.find('<')]
                item['modelid'] = filt(price.xpath('td[1]/a/@href').extract()[0], 'spec_', '.')

                if ISSAVE: db.insert('autohome_allprice', item)

                if ISPOST:
                    tmb = doPost(API_ADDRESS, item)
                    log.msg('\t' + str(tmb['error']) + ', ' + tmb['msg'])
