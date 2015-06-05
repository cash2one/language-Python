# -*- coding: utf-8 -*-
from scrapy.spider import BaseSpider
from scrapy.selector import Selector
import sys
from simplemysql import SimpleMysql

# I don't know the reason why the data cannot be written into db,
# so all the data crawled was generated into a sql script file.

SCRIPT_FILE = 'chinadealers.sql'

class DealerSpider(BaseSpider):
	name = 'dealer'
	allowed_domains = ['http://dealer.autohome.com.cn/china/']
	urls = []
	for i in range(1696):
		urls.append('http://dealer.autohome.com.cn/china/0_0_0_0_' + str(i) + '.html')
	start_urls = urls

	script = open(SCRIPT_FILE, 'w')
	script.write('DROP TABLE IF EXISTS mapdealer;\n')
	script.write("CREATE TABLE IF NOT EXISTS `mapdealer` (`Id` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,`dealerid` int(11) DEFAULT NULL COMMENT '经销商编号',`dealername` varchar(255) DEFAULT NULL COMMENT '经销商名称',`dealerbrand` varchar(255) DEFAULT NULL COMMENT '经销商品牌',`dealerfullname` varchar(255) DEFAULT NULL COMMENT '经销商公司全名',`dealercity` varchar(255) DEFAULT NULL COMMENT '经销商城市',`remoteid` int(11) DEFAULT NULL COMMENT '服务器经销商编号',`remotename` varchar(255) DEFAULT NULL COMMENT '服务器经销商名称');\n")
	script.close()

	def parse(self, response):
		reload(sys)
		sys.setdefaultencoding('utf-8')

		sel = Selector(response)
		part = sel.xpath('//div[@class="dealer-cont  js-dealer"]')
		#conn = SimpleMysql(host="127.0.0.1", db='locoyspider', user='root', passwd='123456')
		#conn.query("CREATE TABLE IF NOT EXISTS `mapdealer` (`Id` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,`dealerid` int(11) DEFAULT NULL COMMENT '经销商编号',`dealername` varchar(255) DEFAULT NULL COMMENT '经销商名称',`dealerfullname` varchar(255) DEFAULT NULL COMMENT '经销商公司全名',`dealercity` varchar(255) DEFAULT NULL COMMENT '经销商城市',`remoteid` int(11) DEFAULT NULL COMMENT '服务器经销商编号',`remotename` varchar(255) DEFAULT NULL COMMENT '服务器经销商名称');")

		script = open(SCRIPT_FILE, 'a')
		for item in part:
			dealerid = dealername = dealerfullname = dealercity = dealerbrand = ''

			tmp = item.xpath('div/h3/a')
			if len(tmp) > 1: tmp = tmp[-1]
			dealerid = tmp.xpath('@js-did').extract()[0]
			dealername = tmp.xpath('@js-dname').extract()[0]
			dealerfullname = tmp.xpath('text()').extract()[0]
			dealercity = tmp.xpath('@js-darea').extract()[0]
			dealerbrand = item.xpath('div/dl/dd/div[1]/@title').extract()[0]

			print '==>', dealerid, dealername, dealerfullname, dealercity, dealerbrand
			script.write('INSERT INTO mapdealer(dealerid, dealername, dealerfullname, dealercity, dealerbrand) VALUES ('+dealerid+', \''+dealername+'\', \''+dealerfullname+'\', \''+dealercity+'\', \''+dealerbrand+'\');\n')
			#print conn.insert("mapdealer", { 'dealerid': dealerid, 'dealername':dealername, 'dealerfullname':dealerfullname, 'dealercity':dealercity })

		script.close()
