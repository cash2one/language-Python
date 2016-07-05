# -*- coding: utf-8 -*-
#!/usr/bin/env python

import sys, urllib, urllib2, json
from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from scrapy.http import Request
from chebaba.items import AutohomeAllPriceItem

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

    name = 'autohomeallprice'
    allowed_domains = ['dealer.autohome.com.cn']
    start_urls = ['http://dealer.autohome.com.cn/china/']
    if ISPOST: start_urls = ['http://dealer.autohome.com.cn/china//0_63_0_92_1.html']

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
        item = AutohomeAllPriceItem()
        item['city'] = sel.xpath('//div[@class="breadnav"]/a[2]/text()').extract()[0]
        item['dealer'] = sel.xpath('//div[@class="text-main"]/text()').extract()[0]
        item['dealerid'] = sel.xpath('//li[@id="nav_0"]/a/@href').extract()[0].replace('/', '')
        item['manu'] = ','.join(sel.xpath('//div[@class="brandtree-name"]/p[@class="text"]/text()').extract())
        self.logger.info(item['city'] + ', ' + item['dealer'] + ', ' + item['manu'])

        trs = sel.xpath('//div[@class="carprice-cont"]/dl[@class="price-dl"]')
        for tr in trs:
            item['brand'] = tr.xpath('dt[@class="fn-clear"]/div[@class="name"]/p[@class="name-text font-yh"]/a/text()').extract()[0]
            item['brandid'] = filt(tr.xpath('dt[@class="fn-clear"]/div[@class="name"]/p[@class="name-text font-yh"]/a/@href').extract()[0], 'cn/', '/')
            prices = tr.xpath('dd/table/tr')
            for price in prices:
                if price.xpath('th/text()'): continue
                item['model'] = price.xpath('td[1]/a/text()').extract()[0]
                item['modelid'] = filt(price.xpath('td[1]/a/@href').extract()[0], 'spec_', '.')
                item['oprice'] = price.xpath('td[2]/p/text()').extract()[0].replace(u'万','')
                if price.xpath('td[3]/div[@class="this-number red"]/a/text()'): item['price'] = price.xpath('td[3]/div[@class="this-number red"]/a/text()').extract()[0].replace(u'万','')
                else: item['price'] = price.xpath('td[3]/p/text()').extract()[0].replace(u'万','')
                # item['pubdate'] = price.xpath('td[5]/text()').extract()[0].replace(u' ','').replace('\r\n','')

                if ISPOST:
                    tmb = doPost(API_ADDRESS, item)
                    self.logger.info(json.dumps(dict(item), ensure_ascii=False))
