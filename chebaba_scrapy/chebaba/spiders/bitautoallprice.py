# -*- coding: utf-8 -*-
#!/usr/bin/env python

import sys, urllib, urllib2, demjson
from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from scrapy.http import Request
from chebaba.items import BitautoAllPriceItem
from simplemysql import SimpleMysql

ISSAVE = True
ISPOST = False
API_ADDRESS = 'http://120.26.67.45/api/price'
API_ADDRESS = 'http://e4s.stg.dongfeng-nissan.com.cn:81/api/service/offerPrice'

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

def doSave(db, item):
    if not db: return None
    return db.insert('bitauto_allprice', item)

def getBrandsEnName(json):
    srcs = demjson.decode(json)['brand']
    brands = []
    for src in srcs:
        for s in srcs[src]:
            if int(s['num']) > 0:
                tmp = 'http://dealer.bitauto.com' + s['url'] + '?BizModes=0'
                brands.append(tmp)
    return brands

class BitautoAllPriceSpider(BaseSpider):
    reload(sys)
    sys.setdefaultencoding('utf-8')

    name = 'bitautoallprice'
    allowed_domains = ['dealer.bitauto.com']
    start_urls = ['http://api.car.bitauto.com/CarInfo/getlefttreejson.ashx?tagtype=jingxiaoshang']

    def parse(self, response):
        js = response.body.lstrip('JsonpCallBack').lstrip('(').rstrip(')')
        brands = getBrandsEnName(js)
        for brand in brands:
            yield Request(brand, self.parseDealer)

    def parseDealer(self, response):
        sel = Selector(response)
        trs = sel.xpath('//ul[@class="jxs-list"]/li[@class="clearfix"]')
        for tr in trs:
            tmp = tr.xpath('div[@class="intro-box"]/div[@class="p-tit"]/a/@href').extract()[0]
            if 'dealer.bitauto.com' in tmp:
                did = filt(tmp, '.com/', '/?')
                tmp = 'http://dealer.bitauto.com/' + did + '/cars.html'
                yield Request(tmp, self.parsePrice)

        np = sel.xpath('//div[@class="the_pages"]/div/a')
        while np and (np[-1].xpath('text()').extract()[0] == u'下一页'):
            tmp = np[-1].xpath('@href').extract()[0]
            tmp = response.urljoin(tmp)
            yield Request(tmp, self.parseDealer)

    def parsePrice(self, response):
        sel = Selector(response)

        item = BitautoAllPriceItem()
        item['city'] = filt(sel.xpath('//div[@class="adress"]/text()').extract()[0], u'地址：', u'市')
        item['dealer'] = sel.xpath('//div[@class="info"]/h1/text()').extract()[0]
        item['dealerid'] = filt(response.url, '.com/', '/')

        db = SimpleMysql(host = '127.0.0.1:5029', db = 'wholenetwork', user = 'root', passwd = '')
        trs = sel.xpath('//div[@class="car_list"]')
        for tr in trs:
            tmp = tr.xpath('div/div[@class="car_top"]/h3/a')
            item['brand'] = tmp.xpath('text()').extract()[0]
            item['brandid'] = filt(tmp.xpath('@href').extract()[0], 'cars_', '.html')
            prices = tr.xpath('div/div[@class="car_price"]/table/tbody/tr')
            for price in prices:
                if not price.xpath('td'): continue    # filt th rows
                item['model'] = price.xpath('td[1]/a/@title').extract()[0]
                item['modelid'] = filt(price.xpath('td[1]/a/@href').extract()[0], 'price_detail/', '.html')
                item['oprice'] = price.xpath('td[2]/text()').extract()[0].replace(u' ','').replace('\r\n','').replace(u'万','')
                item['price'] = price.xpath('td[4]/a/text()').extract()[0].replace('\r\n','').replace(u' ','').replace(u'万','')
                item['off'] = price.xpath('td[3]/em/text()').extract()[0].replace('\r\n','').replace(u' ','').replace(u'万','').replace(u'↓','')

                if ISSAVE: doSave(db, item)
                if ISPOST: doPost(API_ADDRESS, item)

        np = sel.xpath('//div[@id="pager"]/a')
        while np and (np[-1].xpath('text()').extract()[0] == u'下一页'):
            url = np[-1].xpath('@href').extract()[0]
            url = response.urljoin(url)
            yield Request(url, self.parsePrice)
