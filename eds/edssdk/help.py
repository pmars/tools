#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: help.py
# Author: xingming
# Mail: huoxingming@gmail.com
# Created Time:  2015-12-11 01:23:50 AM
#############################################

import sys

def sum(*values):
    s = 0
    for v in values:
        i = int(v)
        s = s + i
    print s

def output():
    print 'http://xiaoh.me'


def main():
    print 'this is main()'
    print sys.argv[1:]

if __name__ == "__main__":
    main()
