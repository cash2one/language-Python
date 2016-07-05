# -*- coding: utf-8 -*-
#!/usr/bin/env python

import sys
from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from scrapy.http import Request
from simplemysql import SimpleMysql

host='127.0.0.1'
user='root'
pswd='root'
dbname='wholenetwork'
tablename='allcars'

def filt(string, start, end):
	i = string.find(start) + len(start)
	j = string[i:].find(end)
	return string[i : i + j]

class AllCars(BaseSpider):
	reload(sys)
	sys.setdefaultencoding('utf-8')

	name = 'allcars'
	allowed_domains = ['car.autohome.com.cn']
	start_urls = ['http://car.autohome.com.cn/']

	def parse(self, response):
		sel = Selector(response)
		cars = sel.xpath('//div[@class="brandcont-open fn-hide"]/span[@class="open-name"]/a/@href').extract()
		for car in cars:
			brand = filt(response.urljoin(car), 'list-0-0-0-0-0-0-0-0-', '-')
			yield Request('http://car.autohome.com.cn/price/brand-' + brand + '.html', self.getSeries)

	def getSeries(self, response):
		sel = Selector(response)

		item = {}
		item['brand'] = sel.xpath('//h2[@class="fn-left name"]/a/text()').extract()[0]

		db = SimpleMysql(host = host, db = dbname, user = user, passwd = pswd)
		fs = sel.xpath('//div[@class="carbradn-cont fn-clear"]/dl')
		for f in fs:
			item['factory'] = f.xpath('dt/a/text()').extract()[0]
			ts = f.xpath('dd/div[@class="list-dl-name"]')
			ss = f.xpath('dd/div[@class="list-dl-text"]')

			for i in range(len(ts)):
				item['cartype'] = ts[i].xpath('text()').extract()[0].replace(u'：', '')
				temp1 = ''
				temp2 = ''
				qs = ss[i].xpath('a/text()').extract()
				for q in qs:
					if u'停售' in q:
						temp1 += q.replace(u'(停售)', '').strip() + ','
					else:
						temp2 += q + ','
				item['halts'] = temp1[:-1]
				item['series'] = temp2[:-1]
				db.insert(tablename, item)
				self.logger.info(item)
