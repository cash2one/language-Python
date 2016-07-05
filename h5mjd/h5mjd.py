#!/usr/bin/env python
# coding: utf-8

from lxml import html, etree
import urllib2
import sys, time, json, logging
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtWebKit import *

class Render(QWebPage):
    def __init__(self, url):
        try:
            self.app = QApplication(sys.argv)
            QWebPage.__init__(self)
            self.loadFinished.connect(self._loadFinished)
            self.mainFrame().load(QUrl(url))
            self.app.exec_()
        except Exception, e:
            logging.error(e)

    def userAgentForUrl(self, url):
        return 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.10 Safari/537.36'

    def _loadFinished(self, result):
        self.frame = self.mainFrame()
        self.app.quit()

def getItem(url):
    try:
        r = Render(url)
        dom = html.fromstring(str(r.frame.toHtml().toUtf8()))
        if len(dom.xpath('//title/text()')) < 1: return None
        item = {}
        item['brand'] = dom.xpath('//div[@class="u_inf"]/b[@class="um"]/text()')[0]
        item['total'] = dom.xpath('//div[@class="u_inf"]/a[@class="more"]/span/text()')[0]
        item['title'] = dom.xpath('//div[@class="pos art_inner"]/h1/text()')[0]
        item['pubon'] = dom.xpath('//div[@class="pos art_inner"]/b/text()')[0]
        return item
    except Exception, e:
        print e
        return None

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    logging.basicConfig(level=logging.INFO, format='%(message)s', filename=‘h5mjd.log', filemode='a')

    url = 'http://h5.m.jd.com/active/faxian/html/innerpage.html?id=' + sys.argv[1]
    print url
    t = getItem(url)
    if t:
        t['url'] = url
        logging.info(json.dumps(t, ensure_ascii=False))

