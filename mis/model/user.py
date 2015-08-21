#!/usr/bin/env python
# coding: utf-8

from config.settings import db
import hashlib, datetime

table = 'user'

class User:
	def __init__(self):
		pass

	def checkLogin(self, username, password):
		password1 = hashlib.md5(password).hexdigest()
		myvar = dict(username=username, password1=password1)
		result = db.select(table, myvar, where='username=$username and password=$password1')
		return result

	def register(self, username, password, email):
		password1 = hashlib.md5(password).hexdigest()
		result = db.insert(table, username=username, password=password1, email=email, joindate=datetime.datetime.utcnow())
		return result
