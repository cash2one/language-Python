# -*- coding: utf-8 -*-
#!/usr/bin/env python

import logging
from sleekxmpp import ClientXMPP
from sleekxmpp.exceptions import IqError, IqTimeout
import ssl

class EchoBot(ClientXMPP):
	def __init__(self, jid, password):
		ClientXMPP.__init__(self, jid, password)

		self.add_event_handler('session_start', self.session_start)
		self.add_event_handler('message', self.message)
		self.ssl_version = ssl.PROTOCOL_SSLv3

	def session_start(self, event):
		self.send_presence()

		try:
			self.get_roster()
		except IqError as err:
			logging.error('There was an error getting the roster')
			logging.error(err.iq['error']['condition'])
			self.disconnect()
		except IqTimeout:
			logging.error('Server is taking too long to response')
			self.disconnect()

	def message(self, msg):
		if msg['type'] in ('chat', 'normal'):
			msg.reply('Thanks for sending %(body)s' % msg).send()

if __name__ == '__main__':
	logging.basicConfig(level = logging.DEBUG, format = '%(levelname) - 8s %(message)s')
	xmpp = EchoBot('user1@s239840', '123456')
	xmpp.connect()
	xmpp.process(block=True)
