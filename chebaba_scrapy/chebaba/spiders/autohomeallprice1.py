# -*- coding: utf-8 -*-
#!/usr/bin/env python

import sys, json
from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from scrapy.http import Request
from chebaba.items import AutohomeAllPriceItem
from simplemysql import SimpleMysql

host='127.0.0.1'
user='root'
pswd='root'
dbname='wholenetwork'
tablename='autohome_allprice'

def filt(string, start, end):
    i = string.find(start) + len(start)
    j = string[i:].find(end)
    return string[i : i + j]

class AutohomeAllPriceSpider(BaseSpider):
    reload(sys)
    sys.setdefaultencoding('utf-8')

    name = 'baojia'
    allowed_domains = ['dealer.autohome.com.cn']
    start_urls = ['http://dealer.autohome.com.cn/china/']

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
        tmp = sel.xpath('//div[@class="brandtree-name"]')

        tmps = ''
        for t in tmp: tmps += t.xpath('p[@class="text"]/text()').extract()[0] + ','
        item['manu'] = tmps[:-1]
        self.logger.info(u'经销商：' + item['dealer'] + u'，\t\t\t\t主营品牌：' + item['manu'])

        trs = sel.xpath('//div[@class="carprice-cont"]/dl[@class="price-dl"]')
        for tr in trs:
            item['brand'] = tr.xpath('dt[@class="fn-clear"]/div[@class="name"]/p/a/text()').extract()[0]
            item['brandid'] = filt(tr.xpath('dt[@class="fn-clear"]/div[@class="name"]/p/a/@href').extract()[0], 'cn/', '/')
            item['cartype'] = tr.xpath('dt/div[@class="info"]/p[2]/text()').extract()[0]

            db = SimpleMysql(host = host, db = dbname, user = user, passwd = pswd)
            prices = tr.xpath('dd/table/tr')
            for price in prices:
                tmp = price.xpath('td[2]/p/text()').extract()
                if not tmp: continue  # filt th row
                item['oprice'] = tmp[0].replace(u'万','')

                tmp = price.xpath('td[3]/div[@class="this-number red"]/a/text()').extract()
                if not tmp: tmp = price.xpath('td[3]/p/a/text()').extract()
                item['price'] = tmp[0].replace(u'万','').strip()

                tmp = price.xpath('td[1]/a/text()').extract()[0]
                item['model'] = tmp[:tmp.find('<')]

                item['modelid'] = filt(price.xpath('td[1]/a/@href').extract()[0], 'spec_', '.')

                db.insert(tablename, item)
                #self.logger.info(json.dumps(dict(item)))
