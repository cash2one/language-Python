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
		conn = SimpleMysql(host="127.0.0.1", charset='utf8', db='scrapy_demo', user='root', passwd='')
		for item in part:
			conn.query('''CREATE TABLE IF NOT EXISTS `CHINA` ( `ID` int unsigned NOT NULL AUTO_INCREMENT PRIMARY KEY, `dealer` varchar(255) NOT NULL,
				`brand` varchar(255), `phone` varchar(255), `saleto` varchar(255), `address` varchar(255));''')
			dealer1 = brand1 = phone1 = address1 = ''
			dealer = item.xpath("div/h3/a/text()").extract()
			if len(dealer) > 1: dealer1 = dealer[-1]
			elif len(dealer) < 1: dealer1 = ''
			else: dealer1 = dealer[0]

			brand = item.xpath("div/dl/dd/div[1]/@title").extract()
			if len(brand) < 1: brand1 = ''
			else: brand1 = brand[0]

			phone = item.xpath("div/dl/dd/div[2]/span[@class='dealer-api']/span[@class='dealer-api-phone']/text()").extract()
			if len(phone) < 1: phone1 = ''
			else: phone1 = phone[0]

			saleto = sel.xpath("//i[@class='icon icon-salebp']/@title").extract()
			if len(saleto) < 1: saleto = ''
			else: saleto1 = saleto[0]

			address = item.xpath("div/dl/dd/div[3]/@title").extract()
			if len(address) < 1: address1 = ''
			else: address1 = address[0]

			print dealer1
			conn.insert("CHINA", {'dealer': dealer1, 'brand':brand1, 'phone':phone1, 'saleto':saleto1, 'address':address1})
