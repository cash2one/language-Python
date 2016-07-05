#!/usr/bin/env python

import lxml.html
import urllib2

def get_title(addr):
    return lxml.html.fromstring(urllib2.urlopen(addr).read()).xpath('//p[@class="ft1 c2"]')[0].text

if __name__ == '__main__':
    for i in range(1000):
        try:
            a = get_title('http://wechat.giftyou.me/article_item?id=' + str(i))
            print i, '\t', a
        except Exception, e:
            continue
            
