#!/usr/bin/env python
# coding: utf-8

from baidu.api.base import ApiSDKJsonClient

class CampaignService(ApiSDKJsonClient):
    def __init__(self):
        ApiSDKJsonClient.__init__(self, 'sms', 'service', 'CampaignService')

    def getCampaign(self, getCampaignInfoRequest=None):
        return self.execute('getCampaign', getCampaignInfoRequest)
