#!/usr/bin/env python
# coding: utf-8

import json
import requests

class AuthHeader():
    def __init__(self, username=None, password=None, token=None, target=None, accessToken=None): 
        self.username=username
        self.password=password
        self.token=token
        self.target=target
        self.accessToken=accessToken
        self.action='API-SDK'

    def setUsername(self, username):
        self.username = username

    def setPassword(self, password):
        self.password = password

    def setToken(self, token):
        self.token = token

    def setTarget(self, target):
        self.target = target

    def setAccessToken(self, accessToken):
        self.accessToken = accessToken

class JsonEnvelop():
    def __init__(self, header=None, body=None): 
        self.header = header
        self.body = body

    def setHeader(self, header):
        self.header = header

    def setBody(self, body):
        self.body = body

class ApiSDKJsonClient:
    def __init__(self, productline, version, service):
        try:
            self.__productline = productline
            self.__version = version
            self.__service = service

            self.__url = 'https://api.baidu.com'
            self.__action = 'API-SDK'
            self.__username = None
            self.__password = None
            self.__token = None
            self.__target = None
            self.__accessToken = ''
        except Exception as e:
            raise e

    def setUsername(self, username):
        self.__username = username

    def setPassword(self, password):
        self.__password = password

    def setToken(self, token):
        self.__token = token

    def setTarget(self, target):
        self.__target = target

    def setAccessToken(self, accessToken):
        self.__accessToken = accessToken

    @staticmethod
    def get_params(obj):
        return obj.__dict__

    def execute(self, method, request):
        try:
            url = '%s/json/%s/%s/%s/%s' % (self.__url, self.__productline, self.__version, self.__service, method)
            header = AuthHeader(username=self.__username, password=self.__password, token=self.__token, target=self.__target, accessToken=self.__accessToken)
            jsonStr = json.dumps(
                JsonEnvelop(header, request and request or {}),
                default=ApiSDKJsonClient.get_params,
                skipkeys=True)
            r = requests.post(url, data=jsonStr, headers={'content-type': 'application/json;charset=utf-8'})
            return r.json()
        except Exception as e:
            raise e
