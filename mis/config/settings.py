#!/usr/bin/env python
# coding: utf-8

import web
from main import app

web.config.debug = False

db = web.database(dbn='mysql', host='127.0.0.1', port=3306, db='mis', user='root', pw='root')

config = web.storage(
	email = 'a@ie9.org',
	site_name = 'site name',
	site_desc = 'site description',
	static = '/static',
)

session = web.session.Session(app, web.session.DiskStore('session'), initializer={'username': None})
if not web.config.get('_session'): web.config._session = session
else: session = web.config._session
# web.config.session_parameters['cookie_name'] = 'session_id'
# web.config.session_parameters['cookie_domain'] = None
# web.config.session_parameters['timeout'] = 60,
# web.config.session_parameters['ignore_expiry'] = True
# web.config.session_parameters['ignore_change_ip'] = True
# web.config.session_parameters['secret_key'] = 'fLjUfxqXtfNoIldA0A0J'
# web.config.session_parameters['expired_message'] = 'Session expired'

render = web.template.render(
	'view/',
	base = 'layout',
	cache = False,
	globals={'session': session},
)
