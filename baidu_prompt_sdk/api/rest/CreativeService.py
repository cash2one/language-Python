#!/usr/bin/env python
# coding: utf-8

from baidu.api.base import ApiSDKJsonClient

class CreativeService(ApiSDKJsonClient):
    def __init__(self):
        ApiSDKJsonClient.__init__(self, 'sms', 'service', 'CreativeService')

    def getCreative(self, getCreativeInfoRequest=None):
        return self.execute('getCreative', getCreativeInfoRequest)
