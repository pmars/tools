#!/usr/bin/python
#-*- coding:utf-8 -*-

#############################################
# File Name: tools.py
# Author: xiaoh
# Mail: xiaoh@about.me
# Created Time:  2016-04-26 00:59:05
#############################################

###########################################################
#                                                         #
#                         _oo8oo_                         #
#                        o8888888o                        #
#                        88" . "88                        #
#                        (| -_- |)                        #
#                        0\  =  /0                        #
#                      ___/'==='\___                      #
#                    .' \\|     |// '.                    #
#                   / \\|||  :  |||// \                   #
#                  / _||||| -:- |||||_ \                  #
#                 |   | \\\  -  /// |   |                 #
#                 | \_|  ''\---/''  |_/ |                 #
#                 \  .-\__  '-'  __/-.  /                 #
#               ___'. .'  /--.--\  '. .'___               #
#            ."" '<  '.___\_<|>_/___.'  >' "".            #
#           | | :  `- \`.:`\ _ /`:.`/ -`  : | |           #
#           \  \ `-.   \_ __\ /__ _/   .-` /  /           #
#       =====`-.____`.___ \_____/ ___.`____.-`=====       #
#                         `=---=`                         #
#                                                         #
#                佛祖保佑         永无BUG                 #
#                                                         #
###########################################################

import functools
import time, os
import subprocess


class Status():
    success = (0, '')
    exception = (10000, 'exception occurs')
    service_not_found = (10100, 'spider not found')


def log(func):
    @functools.wraps(func)
    def wrapper(*args, **kw):
        print '%s run %s() now. args:%s, kw:%s' % (
            time.strftime('%Y-%m-%d %H:%M:%S'), func.__name__, args, kw)
        return func(*args, **kw)
    return wrapper

def format_num(mem, tag='k'):
    mem = float(mem)
    if tag == 'b':
        if mem/8 > 1:
            return format_num(mem/8, 'k')
        else:
            return '%.2f %s' % (mem, tag)
    if tag == 'k':
        if mem/1024 > 1:
            return format_num(mem/1024, 'K')
        else:
            return '%.2f %s' % (mem, tag)
    elif tag == 'K':
        if mem/1024 > 1:
            return format_num(mem/1024, 'M')
        else:
            return '%.2f %s' % (mem, tag)
    elif tag == 'M':
        if mem/1024 > 1:
            return format_num(mem/1024, 'G')
        else:
            return '%.2f %s' % (mem, tag)
    else:
        return '%.2f %s' % (mem, tag)

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

def run_cmd(cmd):
    return subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout.read()

def format_job(job):
    return {
        'minute' : str(job.minute),
        'hour' : str(job.hour),
        'days' : str(job.day),
        'month' : str(job.month),
        'command' : job.command,
        'comment' : job.comment
    }

cmd = "python -c 'from superv import SpiderHelper; sh = SpiderHelper(\"{name}\",\"{command}\"); sh.{function}();'"
def create_service(service_name, command):
    return run_cmd(cmd.format(name=service_name, command=command, function='create'))

def start_service(service_name):
    return run_cmd(cmd.format(name=service_name, command='', function='start'))

def status_service(service_name):
    return run_cmd(cmd.format(name=service_name, command='', function='status'))

def remove_service(service_name):
    return run_cmd(cmd.format(name=service_name, command='', function='remove'))

def remove_service_all():
    return run_cmd(cmd.format(name='all', command='', function='remove_all'))

def status_code(code = Status.success, more_msg = '', obj = None):
    return {
        'code' : code[0],
        'message' : code[1] + more_msg,
        'result' : obj
    }

