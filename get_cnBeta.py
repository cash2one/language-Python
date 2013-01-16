#!/usr/bin/env python

import lxml.html
import urllib2
import lxml.etree

url='http://www.cnbeta.com'

dom = lxml.html.fromstring(urllib2.urlopen(url).read())
tre = dom.xpath('//dt[@class="topic"]/a')
res = len(tre)

for index in range(res):
	print index + 1, url + tre[index].get('href'), tre[index].getchildren()[0].text

