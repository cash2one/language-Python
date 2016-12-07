#!/usr/bin/env python
# coding: utf-8

from baidu.api.base import ApiSDKJsonClient

class AccountService(ApiSDKJsonClient):
    def __init__(self):
        ApiSDKJsonClient.__init__(self, 'sms', 'service', 'AccountService')

    def getAccountInfo(self, getAccountInfoRequest=None):
        return self.execute('getAccountInfo', getAccountInfoRequest)
