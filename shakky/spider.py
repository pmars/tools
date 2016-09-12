#!/usr/bin/python
#-*- coding:utf-8 -*-

#############################################
# File Name: spider.py
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
import json, os, sys, psutil
from crontab import CronTab
import ConfigParser
from superv import SpiderHelper


class Spider(tornado.web.RequestHandler):
    @log
    def get(self):
        '''status of spider'''
        name = self.get_argument('name')

        if not SpiderHelper(name).exists():
            self.write(status_code(Status.service_not_found))
            return

        cron = CronTab(user=True)
        jobs = cron.find_comment(name)
        job_list = [format_job(job) for job in jobs]

        if len(job_list) == 0:
            self.write(status_code(Status.service_not_found))
            return

        log = status_service(name)
        msg_list = log.split('\n')[-2].split()
        if msg_list[1] != 'RUNNING':
            self.write(status_code(more_msg='Service not running now.', obj = job_list[0]))
            return

        pid = int(msg_list[3][:-1])
        pro = psutil.Process(pid)

        times = pro.cpu_times()
        create_time = time.localtime(pro.create_time())
        pmem = pro.memory_info()
        job = {
            "job_msg" : job_list[0],
            "cmdline" : pro.cmdline(),
            "cpu_percent" : pro.cpu_percent(),
            "cpu_times" : {
                "children_system" : times.children_system,
                "children_user" : times.children_user,
                "system" : times.system,
                "user" : times.user
            },
            "is_running" : pro.is_running(),
            "pid" : pid,
            "running_time" : msg_list[5],
            "create_time" : time.strftime('%Y-%m-%d %H:%M:%S', create_time),
            "memory_info" : {
                "rss" : pmem.rss,
                "vms" : pmem.vms,
                "shared" : pmem.shared,
                "text" : pmem.text,
                "lib" : pmem.lib,
                "data" : pmem.data,
                "dirty" : pmem.dirty
            },
            "status" : pro.status(),
            "username" : pro.username()
        }
        self.write(status_code(obj=job))

    @log
    def put(self):
        '''create one spider'''
        cron = CronTab(user=True)
        name = self.get_argument('name')
        mins = self.get_argument('mins', '0')
        hour = self.get_argument('hour', '0')
        days = self.get_argument('days', '*')
        month = self.get_argument('month', '*')
        week = '*'

        print name, mins, hour, days, month, week

        service_dir = os.path.join(sys.path[0], 'services', name)
        if os.path.exists(service_dir):
            self.write(json.dumps({'code':1,'message':'service has exists'}))
            return

        mkdir_p(service_dir)
        filename = ''
        for meta in self.request.files['script']:
            filename = os.path.join(service_dir, meta['filename'])
            with open(filename, 'wb') as out_file:
                out_file.write(meta['body'])

            if filename.endswith('tar.gz'):
                cmd = 'cd %s && tar -xzf %s' % (service_dir, os.path.basename(filename))
                run_cmd(cmd)

        command = 'python %s' % filename
        for meta in self.request.files['command']:
            command = meta['body']
        print command

        print create_service(name, command)

        super_conf_file = os.path.join(sys.path[0], 'supervisor.conf')
        command = "supervisorctl -c %s start %s" % (super_conf_file, name)
        job = cron.new(command = command, comment = name)
        job.setall('%s %s %s %s %s' % (mins, hour, days, month, week))
        cron.write()

        self.write(json.dumps({'job':format_job(job)}))

    @log
    def delete(self):
        '''remove one spider'''
        name = self.get_argument('name')
        cron = CronTab(user=True)
        jobs = cron.find_comment(name)
        [job.delete() for job in jobs]
        cron.write()

        remove_service(name)
        self.write('{}')

class SpiderStart(tornado.web.RequestHandler):
    @log
    def get(self):
        name = self.get_argument('name')
        log = start_service(name)
        msg_list = log.split('\n')[-2].split()
        msg_list[3] = msg_list[3][:-1]
        self.write(status_code(obj = msg_list))

class SpiderModify(tornado.web.RequestHandler):
    @log
    def get(self):
        '''create one spider'''
        name = self.get_argument('name')
        mins = self.get_argument('mins', '0')
        hour = self.get_argument('hour', '0')
        days = self.get_argument('days', '*')
        month = self.get_argument('month', '*')

        cron = CronTab(user=True)
        for job in cron.find_comment(name):
            job.setall('%s %s %s %s *' % (mins, hour, days, month))
        cron.write()

        self.write(status_code(obj=format_job(job)))

class SpiderList(tornado.web.RequestHandler):
    @log
    def get(self):
        cron = CronTab(user=True)
        job_list = [format_job(job) for index, job in enumerate(cron)]
        self.write(status_code(obj=job_list))

    @log
    def delete(self):
        cron = CronTab(user=True)
        [job.delete() for index, job in enumerate(cron)]
        cron.write()
        remove_service_all()
        self.write(status_code())

class SpiderLog(tornado.web.RequestHandler):
    @log
    def get(self):
        name = self.get_argument('name')
        line = self.get_argument('line', 100)

        service_work_dir = os.path.join(sys.path[0], 'services', name)

        if not os.path.exists(service_work_dir):
            self.write(status_code(Status.service_not_found))
            return

        service_log_path = os.path.join(service_work_dir, 'stdout.log')

        if not os.path.exists(service_log_path):
            self.write(status_code(more_msg = "there is not logging now."))
            return

        log = run_cmd('tail -n %s %s' % (line, service_log_path))
        self.write(status_code(obj = log.rstrip().split('\n')))

