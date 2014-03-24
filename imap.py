import imaplib, string, email

if __name__ == '__main__':
	m = imaplib.IMAP4("xxxxxxxxxxxx")
	try:
		try:
			m.login('username', 'password')
		except Exception, e:
			print 'login error: ', e
			m.close()

		result, message = m.select()
		typ, data = m.search(None, 'All')
		for num in string.split(data[0]):
			try:
				typ, data = m.fetch(num, '(RFC822)')
				msg = email.message_from_string(data[0][1])
				print 'From: ', msg['From']
				print 'Subject: ', msg['Subject']
				print 'Date: ', msg['Date']
				print '-------------------------------------------------\n'
			except Exception, e:
				print 'got msg error: ', e

		m.logout()
		m.close()
	except Exception, e:
		print 'imap err: ', e
		m.close()
