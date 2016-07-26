#!/usr/bin/env python
# coding: utf-8

from lxml import html, etree
import sys, logging, requests, socket

class IP:
    # 构造函数
    def __init__(self):
        self.url = 'http://www.runoob.com/w3cnote/google-ip.html'
        self.skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.skt.settimeout(10)

    # 基于lxml解析网页内容
    def get_all_ip(self):
        return html.fromstring(
            requests.get(self.url).text
        ).xpath('//td/a/text()')

    # 基于socket库检查网络连接情况
    def connective(self, ip, port=80):
        try:
            return self.skt.connect_ex((ip, port)) == 0
        except Exception, e:
            return False

    # 析构函数中关闭socket
    def __del__(self):
        if self.skt:
            self.skt.close()

if __name__ == '__main__':
    # 重新加载编码设置
    reload(sys)
    sys.setdefaultencoding('utf-8')

    # 设置打印及输出文件的日志属性
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] %(levelname)s: %(message)s',
        filename='googleip.log',
        filemode='a',
    )
    console = logging.StreamHandler()
    console.setFormatter(
        logging.Formatter(
            fmt='[%(asctime)s] %(levelname)s: %(message)s',
        )
    )
    logging.getLogger('').addHandler(console)

    # 获取所有IP并逐一检查可用性
    ip = IP()
    ips = ip.get_all_ip()
    for p in [80, 443]:
        for i in ips:
            if ip.connective(i, p):
                if p == 80:
                    logging.info('http://%s' % i)
                elif p == 443:
                    logging.info('https://%s' % i)
