#!/usr/bin/env python

URL='http://www.cnbeta.com'

from bs4 import BeautifulSoup
import urllib2

webpage = urllib2.urlopen(URL)
soup = BeautifulSoup(webpage, fromEncoding="GBK")

print webpage.info()
for link in soup.find_all('a'):
    print link.get('href')
    print link.contents

