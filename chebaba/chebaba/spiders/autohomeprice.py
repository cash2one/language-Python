# -*- coding: utf-8 -*-
#!/usr/bin/env python

import sys, time
from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from scrapy.utils.url import urljoin_rfc
from scrapy.http import Request
from chebaba.items import AutohomePriceItem
import urllib, urllib2, json
from simplemysql import SimpleMysql

AUTOHOME_PRICE_URL = ''
ALL_DEALERS = []

def filt(string, start, end):
    i = string.find(start) + len(start)
    j = string[i:].find(end)
    return string[i : i + j]

class AutohomePriceSpider(BaseSpider):
    reload(sys)
    sys.setdefaultencoding('utf-8')

    name = 'autohomeprice'
    allowed_domains = ['dealer.autohome.com.cn']
    urls = []
    for dealer in ALL_DEALERS:
        urls.append('http://dealer.autohome.com.cn/' + str(dealer) + '/price.html')
    start_urls = urls

    def parse(self, response):
        sel = Selector(response)
        trs = sel.xpath('//div[@class="carprice-cont"]/dl[@class="price-dl"]')
        item = AutohomePriceItem()
        item['dealer'] = sel.xpath('//div[@class="text-main"]/text()').extract()[0]
        item['dealerid'] = sel.xpath('//li[@id="nav_0"]/a/@href').extract()[0].replace('/', '')
        print '\n[', ALL_DEALERS.index(int(item['dealerid'])) + 1, '/', len(ALL_DEALERS), ']',\
              'dealer:', item['dealer'], 'dealerid:', item['dealerid']

        data = {}
        db = SimpleMysql(
            host = '127.0.0.1',
            db = 'wholenetwork',
            user = 'root',
            passwd = 'root'
            )
        for tr in trs:
            item['brand'] = tr.xpath('dt[@class="fn-clear"]/div[@class="name"]/p/a/text()').extract()[0]
            item['brandid'] = filt(tr.xpath('dt[@class="fn-clear"]/div[@class="name"]/p/a/@href').extract()[0], 'cn/', '/')
            print '\tbrand:', item['brand'], '|', 'brandid:', item['brandid']
            prices = tr.xpath('dd/table/tr')
            for price in prices:
                tmp = price.xpath('td[2]/p/text()').extract()
                if not tmp: continue  # filt th row
                else: item['oprice'] = tmp[0]
                item['oprice'] = item['oprice'].replace(u'万','')
                tmp = price.xpath('td[3]/div[@class="this-number red"]/a[1]/text()').extract()
                if not tmp: tmp = price.xpath('td[3]/p/a/text()').extract()
                item['price'] = tmp[0].replace(u'万','').replace(u' ','')
                tmp = price.xpath('td[1]/a/text()').extract()[0]
                item['model'] = tmp[:tmp.find('<')]
                item['modelid'] = filt(price.xpath('td[1]/a/@href').extract()[0], 'spec_', '.')
                print '\t\tmodel:', item['model'], '|', 'modelid:', item['modelid'], '|', 'price:', item['price'], '|', 'oprice:', item['oprice'],

                data['dealer_id'] = item['dealerid']
                data['dealer_name'] = item['dealer']
                data['id'] = item['modelid']
                data['title'] = item['model']
                data['zprice'] = item['oprice']
                data['price'] = item['price']

                request = urllib2.Request(AUTOHOME_PRICE_URL, urllib.urlencode(data))
                response = urllib2.urlopen(request).read()
                result = json.loads(response)
                print '\t', result['error'], result['msg']

                db.insert('autohome_price', item)
