#!/usr/bin/python
#-*- coding:utf-8 -*-

#############################################
# File Name: tools.py
# Author: xiaoh
# Mail: xiaoh@about.me
# Created Time:  2016-02-16 14:55:55
#############################################

import smtplib
import ConfigParser
from email import encoders
from email.header import Header
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import parseaddr, formataddr
import traceback, time

from_addr = 'huoxm@zetyun.com'
password = 'HUOxingming1112'
smtp_serv = 'smtp.office365.com'
to_addr = ['p.mars@163.com']

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr(( \
        Header(name, 'utf-8').encode(), \
        addr.encode('utf-8') if isinstance(addr, unicode) else addr))

def send_text():
    msg = MIMEText('hello, send by script coding by xiaoh.', 'plain', 'utf-8')
    msg['From'] = _format_addr(u'Datacanvas <%s>' % from_addr)
    msg['To'] = _format_addr(u'管理员 <%s>' % to_addr)
    msg['Subject'] = Header(u'来自SMTP的问候……', 'utf-8').encode()
    send(msg)

def send_html(subject, html):
    try:
        msg = MIMEText(html, 'html', 'utf-8')
        msg['From'] = _format_addr(u'实现网<%s>' % from_addr)
        msg['To'] = _format_addr(u'Master <p.mars@163.com>')
        msg['Subject'] = Header(subject, 'utf-8').encode()
        send(msg)
    except Exception as e:
        traceback.print_exc()
        print type(e)
        print e.message

def format_type(name):
    return  name if isinstance(name, unicode) else unicode(name, 'utf-8')

def send(msg):
    server = smtplib.SMTP(smtp_serv, 587) # 25为SMTP协议的默认端口
    server.ehlo()
    server.starttls()
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, to_addr, msg.as_string())
    server.quit()

def main():
#    send_text()
    send_html('name', 'description', 'api_url', 'result', 'owner', 'priority')
#    send_attachment()
#    send_image()
#    send_multi()
    print 'hello'

if __name__ == "__main__":
    main()
