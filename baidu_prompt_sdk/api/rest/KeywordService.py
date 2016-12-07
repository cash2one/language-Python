#!/usr/bin/env python
# coding: utf-8

from baidu.api.base import ApiSDKJsonClient

class KeywordService(ApiSDKJsonClient):
    def __init__(self):
        ApiSDKJsonClient.__init__(self, 'sms', 'service', 'KeywordService')

    def getWord(self, getWordInfoRequest=None):
        return self.execute('getWord', getWordInfoRequest)
