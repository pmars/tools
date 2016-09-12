#!/usr/bin/python
#-*- coding:utf-8 -*-

#############################################
# File Name: rest.py
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

import tornado.ioloop
import tornado.web
from machine import *
from spider import *

def make_app():
    return tornado.web.Application([
        ("/api/v1/machine", Machine),
        ("/api/v1/cpu", CPU),
        ("/api/v1/memory", Memory),
        ("/api/v1/disk", Disk),
        ("/api/v1/network", Network),
        ("/api/v1/spider", Spider),
        ("/api/v1/spiderlist", SpiderList),
        ("/api/v1/spiderstart", SpiderStart),
        ("/api/v1/spidermodify", SpiderModify),
        ("/api/v1/spiderlog", SpiderLog),
    ], autoreload=True)

if __name__ == '__main__':
    app = make_app()
    app.listen(8004)
    tornado.ioloop.IOLoop.current().start()

