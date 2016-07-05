#!/usr/bin/env python
# coding: utf-8

import web
from config.urls import urls

if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()
