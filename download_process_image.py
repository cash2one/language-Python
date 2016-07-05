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

    remote_url = ''

    download(remote_url)

