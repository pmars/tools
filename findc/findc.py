#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: findc.py
# Author: xingming
# Mail: p.mars@163.com
# Created Time:  2015-11-20 02:51:31 PM
#############################################

import sys, os, re
import optparse

parser = optparse.OptionParser()
parser.add_option(
        "-d",
        "--dir",
        dest="dirPath",
        help="dir for searching [default:%default]",
        metavar="DIRPATH",
        default=os.getcwd())
parser.add_option(
        "-f",
        "--file",
        dest="filename",
        help="filename for searching(option)",
        metavar="FILE")
parser.add_option(
        "-r",
        "--regex",
        dest="regex",
        default="",
        help="regex for matching files [default:'%default']",
        metavar="REGEX")
parser.add_option(
        "-c",
        "--content",
        dest="content",
        help="content for searching",
        metavar="CONTENT")
parser.add_option(
        "-q",
        "--quiet",
        dest="quiet",
        default=False,
        help="don't print logs",
        action="store_false",
        metavar="QUIET")

(options, args) = parser.parse_args()

def findc():
    dirPath = options.dirPath
    filename = options.filename
    regex = options.regex
    content = options.content
    quiet = options.quiet

    if not content:
        print '[warning] input content for searching please'
        parser.print_help()
        return

    try:
        r = re.compile(regex)
    except:
        print '[error] regex error'
        parser.print_help()
        return

    try:
        rc = re.compile('^.*' + content)
    except:
        print '[error] content not regex'
        parser.print_help()
        return

    files = []
    if filename:
        files.append(filename)
    elif os.path.isdir(dirPath):
        files = findFiles(dirPath, r)
    else:
        print '[error] input right path for searching'
        parser.print_help()
        return

    for fi in files:
        if not quiet:
            print 'search file:%s' % fi
        with open(fi) as f:
            for line in f.readlines():
                line = line[:len(line)-1]
                if rc.match(line):
                    print '%s: %s' % (fi, line)
    print 'all content match over.'

def findFiles(dirPath, r):
    files = []
    for fd in os.listdir(dirPath):
        path = os.path.join(dirPath, fd)
        if os.path.isdir(path):
            for f in findFiles(path, r):
                files.append(f)
        else:
            if r.match(path):
                files.append(path)
    return files


if __name__ == "__main__":
    findc()

