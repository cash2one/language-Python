#!/usr/bin/env python

import smtplib
from email.mime.text import MIMEText
import urllib, lxml.html
import json
import time
import sqlite3

report_to = '****@msn.com'
dollar = 6.07179288
MIN = 190
MAX = 230

def send_mail(send_to, subject, body):
    mail_host = 'smtp.163.com'
    mail_user = ''
    mail_pass = ''
    mail_prefix = '163.com'
    mail_subject = ''
    mail_body = ''

    me = mail_user + '<' + mail_user + '@' + mail_prefix + '>'
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = me
    msg['To'] = send_to

    try:
        s = smtplib.SMTP()
        s.connect(mail_host)
        s.login(mail_user, mail_pass)
        s.sendmail(me, send_to, msg.as_string())
        s.close()
        return True
    except Exception, e:
        print str(e)
        return False

def get_indicator1():
    url = 'https://www.okcoin.com/api/ticker.do?symbol=ltc_cny'
    return json.loads(lxml.html.fromstring(urllib.urlopen(url).read()).text)

def get_indicator2():
    url = 'https://btc-e.com/api/2/ltc_usd/ticker'
    return json.loads(lxml.html.fromstring(urllib.urlopen(url).read()).text)

def init_database1():
    return '''
    CREATE TABLE IF NOT EXISTS OKCOIN (
        ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        SELL FLOAT NOT NULL,
        BUY FLOAT NOT NULL,
        LAST FLOAT NOT NULL,
        VOL FLOAT NOT NULL,
        HIGH FLOAT NOT NULL,
        LOW FLOAT NOT NULL,
        RECORDTIME TIMESTAMP DEFAULT(DATETIME('NOW', 'LOCALTIME')) NOT NULL
    );
    '''

def init_database2():
    return '''
    CREATE TABLE IF NOT EXISTS BTCE (
        ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        HIGH FLOAT NOT NULL,
        LOW FLOAT NOT NULL,
        AVG FLOAT NOT NULL,
        VOL FLOAT NOT NULL,
        VOL_CUR FLOAT NOT NULL,
        LAST FLOAT NOT NULL,
        BUY FLOAT NOT NULL,
        SELL FLOAT NOT NULL,
        RECORDTIME TIMESTAMP DEFAULT(DATETIME('NOW', 'LOCALTIME')) NOT NULL
    );
    '''

def insert_database1(json_string):
    return 'INSERT INTO OKCOIN (SELL, BUY, LAST, VOL, HIGH, LOW) VALUES (' + \
        str(json_string['sell']) + ',' + str(json_string['buy']) + ',' + \
        str(json_string['last']) + ',' + str(json_string['vol']) + ',' + \
        str(json_string['high']) + ',' + str(json_string['low']) + ');'

def insert_database2(json_string):
    return 'INSERT INTO BTCE (HIGH, LOW, AVG, VOL, VOL_CUR, LAST, BUY, SELL) VALUES (' + \
        str(json_string['high']) + ',' + str(json_string['low']) + ',' + \
        str(json_string['avg']) + ',' + str(json_string['vol']) + ',' + \
        str(json_string['vol_cur']) + ',' + str(json_string['last']) + ',' + \
        str(json_string['buy']) + ',' + str(json_string['sell']) + ');'

def format(host, output, trans):
    string = '\033[5;33;40m' + host + ': \033[0m\033[7;33;40m' + output + '\033[0m'
    if trans == '' or trans == None: return string
    return string + '~\033[4;33;40m' + trans + '\033[0m'

def current():
    return time.strftime('%Y-%m-%d %X', time.localtime(time.time()))#time.ctime()

if __name__ == '__main__':
    sent = False

    conn = sqlite3.connect('litecoin.db')
    conn.isolation_level = None

    conn.execute(init_database1())
    conn.execute(init_database2())

    while True:
        try:
            result1 = get_indicator1()
            result2 = get_indicator2()
            ind = result1['ticker']['last']
            sss1 = '[OKCoin] \r\n'
            sss2 = '[BTC-e] \r\n'
            for item in result1['ticker']:
                sss1 += item + ': ' + str(result1['ticker'][item]) + '\r\n'
            for item in result2['ticker']:
                sss2 += item + ': ' + str(result2['ticker'][item]) + '\r\n'

            if float(ind) <= MIN or float(ind) >= MAX:
                if sent == False:
                    send_mail(report_to, 'INDICATOR: ' + str(ind), current() +\
                              '\r\n' + sss1 + '\r\n' + sss2)
                    sent = True
                    print '=====> mail to', report_to, 'has been sent'
            else:
                sent = False

            conn.execute(insert_database1(result1['ticker']))
            conn.execute(insert_database2(result2['ticker']))
            print current(), '\t', format('OKCoin', str(result1['ticker']['last']), ''), '\t',\
                  format('BTC-e', str(result2['ticker']['last']), str(result2['ticker']['last'] * dollar))
        except Exception, e:
            print current(), '\t', 'Exit status:', e
            #break
        time.sleep(7)

    conn.commit()
    conn.close()
