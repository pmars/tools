#!/usr/bin/python
#-*- coding:utf-8 -*-

#############################################
# File Name: machine.py
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

from tools import *
import tornado.web
import psutil, datetime
import platform


class Machine(tornado.web.RequestHandler):
    @log
    def get(self):
        '''infomation of server'''
        machine_info = {
            "time":psutil.time.strftime('%Y-%m-%d %H:%M:%S'),
            "version":[v for v in platform.dist()],
            "boot_time":datetime.datetime.fromtimestamp(psutil.boot_time())
                        .strftime("%Y-%m-%d %H:%M:%S")
        }
        self.write(status_code(Status.success, obj = machine_info))

class CPU(tornado.web.RequestHandler):
    @log
    def get(self):
        '''infomation of CPU'''
        times = psutil.cpu_times()
        cpu_info = {
            "count":psutil.cpu_count(),
            "phy_count":psutil.cpu_count(logical=False),
            "percent":'%s%%' % psutil.cpu_percent(),
            "times":{
                "user":times.user,
                "system":times.system,
                "nice":times.nice,
                "idle":times.idle,
                "iowait":times.iowait
            }
        }
        self.write(status_code(Status.success, obj = cpu_info))

class Memory(tornado.web.RequestHandler):
    @log
    def get(self):
        '''infomation of memory'''
        virtual = psutil.virtual_memory()
        swap = psutil.swap_memory()
        memory_info = {
            "memory":{
                "total"     :format_num(virtual.total),
                "available" :format_num(virtual.available),
                "percent"   :'%s%%' % virtual.percent,
                "used"      :format_num(virtual.used),
                "free"      :format_num(virtual.free),
                "active"    :format_num(virtual.active),
                "inactive"  :format_num(virtual.active),
                "buffers"   :format_num(virtual.buffers),
                "cached"    :format_num(virtual.cached)
            },
            "swap":{
                "total"     :format_num(swap.total),
                "used"      :format_num(swap.used),
                "free"      :format_num(swap.free),
                "percent"   :'%s%%' % swap.percent,
                "sin"       :format_num(swap.sin),
                "sout"      :format_num(swap.sout)
            }
        }
        self.write(status_code(Status.success, obj = memory_info))

class Disk(tornado.web.RequestHandler):
    @log
    def get(self):
        '''infomation of disk'''
        disk_info = {}
        disk_info["partitions"] = []
        for partition in psutil.disk_partitions():
            disk_info["partitions"].append({
                "divice":partition.device,
                "mountpoint":partition.mountpoint,
                "fstype":partition.fstype,
                "opts":partition.opts
                })
        counter = psutil.disk_io_counters()
        disk_info['io_counters'] = {
            "read_count":counter.read_count,
            "write_count":counter.write_count,
            "read_bytes":counter.read_bytes,
            "write_bytes":counter.write_bytes,
            "read_time":counter.read_time,
            "write_time":counter.write_time,
            "read_merged_count":counter.read_merged_count,
            "write_merged_count":counter.write_merged_count,
            "busy_time":counter.busy_time
        }
        self.write(status_code(Status.success, obj = disk_info))

class Network(tornado.web.RequestHandler):
    @log
    def get(self):
        '''infomation of network'''
        counter = psutil.net_io_counters()
        network_info = {
            "bytes_sent":counter.bytes_sent,
            "bytes_recv":counter.bytes_recv,
            "packets_sent":counter.packets_sent,
            "packets_recv":counter.packets_recv,
            "errin":counter.errin,
            "errout":counter.errout,
            "dropin":counter.dropin,
            "dropout":counter.dropout
        }
        self.write(status_code(Status.success, obj = network_info))

