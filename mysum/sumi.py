#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: sum.py
# Author: xingming
# Mail: huoxm@zetyun.com 
# Created Time:  2015-12-10 10:23:50 AM
#############################################

def sum(*values):
    s = 0
    for v in values:
        i = int(v)
        s = s + i
    print s

def output():
    print 'http://xiaoh.me'
