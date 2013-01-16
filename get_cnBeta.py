#!/usr/bin/env python

import lxml.html
import urllib2
import lxml.etree

#url='http://www.cnbeta.com'

def getList(addr):
    dom = lxml.html.fromstring(urllib2.urlopen(addr).read())
    tre = dom.xpath('//dt[@class="topic"]/a')
    res = len(tre)
    result = []
    for index in range(res):
    	result.append([str(index + 1), addr + tre[index].get('href'), tre[index].getchildren()[0].text])
    return result

#print getList(url)[0][2]

#con='http://www.cnbeta.com/articles/222586.htm'

def getContent(addr):
    dom = lxml.html.fromstring(urllib2.urlopen(addr).read())
    title = dom.xpath('//h3[@id="news_title"]')
    content = dom.xpath('//div[@id="news_content"]')
    return [title[0].text, content[0].text_content()]

#res = getContent(con)
#print res[0] + '\n' + res[1]

url='http://www.cnbeta.com'
l = getList(url)
for item in l:
    res = getContent(item[1])
    print res[0] + '\n' + res[1]
