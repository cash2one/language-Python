#!/usr/bin/env python

import smtplib
from email.mime.text import MIMEText

mail_list=['', '']
mail_host=''
mail_user=''
mail_pass=''
mail_prefix=''
mail_subject=''
mail_body=''

def send_mail(send_to, subject, body):
    me = mail_user + '<' + mail_user + '@' + mail_prefix + '>'
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = me
    msg['To'] = ';'.join(send_to)

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

if __name__ == '__main__':
    if send_mail(mail_list, mail_subject, mail_body):
        print 'OK!'
    else:
        print 'Failed!'

