# -*- coding: utf-8 -*-
from scrapy.spider import BaseSpider
from scrapy.selector import Selector
import sys
from simplemysql import SimpleMysql

class DealerSpider(BaseSpider):
	name = 'dealer'
	allowed_domains = ['http://dealer.autohome.com.cn/china/']
	urls = []
	for i in range(1648):
		urls.append('http://dealer.autohome.com.cn/china/0_0_0_0_' + str(i) + '.html')
	start_urls = urls

	def parse(self, response):
		reload(sys)
		sys.setdefaultencoding('utf-8')
		sel = Selector(response)
		part = sel.xpath("//div[@class='dealer-cont  js-dealer']")
		conn = SimpleMysql(host="127.0.0.1", charset='utf8', db='wholenetwork', user='root', passwd='')
		for item in part:
			conn.query('''CREATE TABLE IF NOT EXISTS `dealers` ( `ID` int unsigned NOT NULL AUTO_INCREMENT PRIMARY KEY, `dealer` varchar(255) NOT NULL,
				`brand` varchar(255), `phone` varchar(255), `saleto` varchar(255), `address` varchar(255), `did` varchar(255), `dcity` varchar(255), `dname` varchar(255));''')
			dealer = brand = phone = address = did = dcity = dname = ''
			tmp = item.xpath("div/h3/a/text()").extract()
			if len(tmp) > 1: dealer = tmp[-1]
			elif len(tmp) < 1: dealer = ''
			else: dealer = tmp[0]

			tmp = item.xpath("div/dl/dd/div[1]/@title").extract()
			if len(tmp) < 1: brand = ''
			else: brand = tmp[0]

			tmp = item.xpath("div/dl/dd/div[2]/span[@class='dealer-api']/span[@class='dealer-api-phone']/text()").extract()
			if len(tmp) < 1: phone = ''
			else: phone = tmp[0]

			tmp = sel.xpath("//i[@class='icon icon-salebp']/@title").extract()
			if len(tmp) < 1: tmp = ''
			else: saleto = tmp[0]

			tmp = item.xpath("div/dl/dd/div[3]/@title").extract()
			if len(tmp) < 1: address = ''
			else: address = tmp[0]

			tmp = item.xpath("//h3[@class='dealer-cont-title']/a[1]/@js-did").extract()
			if len(tmp) < 1: did = ''
			else: did = tmp[0]

			tmp = item.xpath("//h3[@class='dealer-cont-title']/a[1]/@js-darea").extract()
			if len(tmp) < 1: dcity = ''
			else: dcity = tmp[0]

			tmp = item.xpath("//h3[@class='dealer-cont-title']/a[1]/@js-dname").extract()
			if len(tmp) < 1: dname = ''
			else: dname = tmp[0]

			print did, dname, dcity, dealer
			conn.insert("dealers", {'dealer': dealer, 'brand':brand, 'phone':phone, 'saleto':saleto, 'address':address, 'did':did, 'dname':dname, 'dcity':dcity})
