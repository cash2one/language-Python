#!/bin/env python
# coding: utf-8

import urllib2
from PIL import Image

def download(url):
    f = urllib2.urlopen(url)
    fn = url.split('/')[-1]
    with open(fn, 'wb') as flow: flow.write(f.read())
    img = Image.open(fn)
    w, h = img.size
    img.crop((0, 0, w, h - 20)).save(fn)

if __name__ == '__main__':

    remote_url = 'http://dealer2.autoimg.cn/dealerdfs/g16/M13/BC/7A/620x0_1_q87_autohomedealer__wKjBx1YrMRGABOCRAAw_ZGYFrlQ580.jpg'

    download(remote_url)

