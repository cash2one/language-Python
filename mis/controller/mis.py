#!/usr/bin/env python
# coding: utf-8

import web
from config.settings import render
from config.settings import session
from model.user import User

def login_required(func):
	def Function(*args):
		if web.config.get('_session') != 'admin':
			return render.login()
		return func(*args)
	return Function

class Index:
	@login_required
	def GET(self):
		return render.index()

class Login:
	def GET(self):
		return render.login()

	def POST(self):
		data = web.input()
		username, password = data.username, data.password
		user = User()
		if user.checkLogin(username, password):
			web.setcookie(username, True, 60)
			session.username = username
			return render.index()
		return render.login()

class Logout:
	def GET(self):
		return render.index()

class Register:
	def GET(self):
		return render.register()

	def POST(self):
		data = web.input()
		username, password, email = data.username, data.password, data.email
		user = User()
		if user.register(username, password, email):
			return render.login()
		return render.register()
