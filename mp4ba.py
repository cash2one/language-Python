#!/usr/bin/env python
# coding: utf-8

'''
@author Tom
@date 2016-09-26
@desc crawl movie resources from mp4ba and save their links to a single log file - simple example
@license MIT
TODO:
    1. optimize logical process
    2. transfer the movies to your own baidu cloud storage
'''

import requests
import re
import logging

'''
    @desc get all links from homepage
    @param home - home url
'''
def get_lists(home=None):
    return re.findall(r'show.php\?hash\=\w+', home)

'''
    @desc filt the baidu link and password out from detail pages
    @param text - detail page dom content
'''
def get_resource(text=None):
    link = re.search(r'http:\/\/pan.baidu.com\/s\/\w+', text)
    pswd = re.search(ur'密码：\w+', text)
    if link and pswd: return '%s %s' % (link.group(), pswd.group()[-4:])

if __name__ == '__main__':
    # log init config
    logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s', filename='mp4ba.log', filemode='a')
    HOME_URL = 'http://www.mp4ba.com/'

    lst = get_lists(requests.get(HOME_URL).text)

    for l in lst:
        url = requests.compat.urljoin(HOME_URL, l)
        print url
        logging.info('%s | %s' % (url, get_resource(requests.get(url).text)))
