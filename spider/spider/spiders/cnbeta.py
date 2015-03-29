# -*- coding: utf-8 -*-
from scrapy.spider import BaseSpider
from scrapy.selector import Selector
import sys
from simplemysql import SimpleMysql

class DealerSpider(BaseSpider):
	name = 'cnbeta'
	allowed_domains = ['www.cnbeta.com']
	urls = []
	for i in range(300000, 310000):
		urls.append('http://www.cnbeta.com/articles/' + str(i) + '.htm')
	start_urls = urls

	def parse(self, response):
		reload(sys)
		sys.setdefaultencoding('utf-8')
		sel = Selector(response)
		item = sel.xpath("//section[@class='article_content']")

		#conn = SimpleMysql(host="127.0.0.1", charset='utf8', db='scrapy_demo', user='root', passwd='')
		#conn.query('''CREATE TABLE IF NOT EXISTS `cnbeta` ( `ID` int unsigned NOT NULL AUTO_INCREMENT PRIMARY KEY, `author` varchar(255) NOT NULL,
		#	`date` varchar(255), `source` varchar(255), `intro` text, `content` text, `url` varchar(255));''')

		title  = ''
		author = ''
		date   = ''
		source = ''
		url    = ''
		intro  = ''
		content= ''

		tmp = item.xpath("//h2[@id='news_title']/text()").extract()
		if len(tmp) > 0:
			title = tmp[0]

		f = open(title + '.txt', 'wb')

		tmp = item.xpath("//span[@class='author']/text()").extract()
		if len(tmp) > 0:
			author = tmp[0]

		tmp = item.xpath("//span[@class='date']/text()").extract()
		if len(tmp) > 0:
			date = tmp[0]

		tmp = item.xpath("//span[@class='where']/text()").extract()
		if len(tmp) > 0:
			source = tmp[0]

		url = response.url

		strong = item.xpath("div[@class='introduction']/p/strong/text()").extract()
		for i in strong:
			intro = intro + i

		part = item.xpath("div[@class='introduction']/p/text()").extract()
		for i in part:
			intro = intro + i

		cont = item.xpath("//div[@class='content']/p").extract()
		for i in cont:
			content = content + i

		#conn.insert("cnbeta", {'author': author, 'date':date, 'source':source, 'intro':intro, 'content':content, 'url':url})

		f.write(title + '\r\n\r\n')
		f.write(author + '\r\n\r\n')
		f.write(date + '\r\n\r\n')
		f.write(source + '\r\n\r\n')
		f.write(intro + '\r\n\r\n')
		f.write(content + '\r\n\r\n')
		f.write(url + '\r\n\r\n')
		f.write(str(response.request.headers))
		f.close()
