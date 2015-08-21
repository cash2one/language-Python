#!/usr/bin/env python
# coding: utf-8

prefix = 'controller.'

urls = (
	'/',          prefix + 'mis.Index',
	'/login',     prefix + 'mis.Login',
	'/register',  prefix + 'mis.Register',
	'/logout',    prefix + 'mis.Logout',
)
