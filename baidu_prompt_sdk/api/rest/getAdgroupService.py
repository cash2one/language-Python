#!/usr/bin/env python
# coding: utf-8

from baidu.api.base import ApiSDKJsonClient

class AdgroupService(ApiSDKJsonClient):
    def __init__(self):
        ApiSDKJsonClient.__init__(self, 'sms', 'service', 'AdgroupService')

    def getAdgroup(self, getAdgroupInfoRequest=None):
        return self.execute('getAdgroup', getAdgroupInfoRequest)
