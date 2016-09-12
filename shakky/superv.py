#!/usr/bin/python
#-*- coding:utf-8 -*-

#############################################
# File Name: superv.py
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
import os, sys
import ConfigParser
from supervisor.supervisorctl import main as supervisor_ctl_main


class SpiderHelper():
    def __init__(self, name, command=None):
        self.service_name = name
        self.service_command = command

        self.root_dir = os.getcwd() if not sys.path[0] else sys.path[0]
        self.super_conf_dir = os.path.join(self.root_dir, 'conf.d')
        self.service_conf_dir = os.path.join(self.root_dir, 'services')

        self.super_conf_file = os.path.join(self.root_dir, 'supervisor.conf')

        self.service_work_dir = os.path.join(self.service_conf_dir, self.service_name)
        self.service_conf_file = os.path.join(self.super_conf_dir, self.service_name + '.conf')

    def exists(self):
        return os.path.exists(self.service_work_dir)

    def create(self):
        super_conf = {
            "command" : self.service_command,
            "process_name" : self.service_name,
            "directory" : self.service_work_dir,
            "stdout_logfile" : os.path.join(self.service_work_dir, 'stdout.log'),
            "stderr_logfile" : os.path.join(self.service_work_dir, 'stderr.log'),
            "autostart" : False,
            "startsecs" : "3",
            "stdout_logfile_maxbytes" : "20MB",
            "stdout_logfile_backups" : "2"
        }
        config = ConfigParser.RawConfigParser()
        section_name = "program:" + self.service_name
        config.add_section(section_name)
        config.add_section('supervisorctl')
        for key in super_conf:
            config.set(section_name, key, super_conf[key])
        with open(self.service_conf_file, 'wb') as config_file:
            config.write(config_file)

        print "Executing : supervisorctl reread '%s' ..." % self.service_name
        supervisor_ctl_main(args=["-c", self.super_conf_file, "reread", self.service_name])
        print "Executing : supervisorctl update '%s' ..." % self.service_name
        supervisor_ctl_main(args=["-c", self.super_conf_file, "update", self.service_name])

    def start(self):
        if not os.path.exists(self.service_work_dir):
            print 'service not exists'
            return
        print "Executing : supervisorctl reread '%s' ..." % self.service_name
        supervisor_ctl_main(args=["-c", self.super_conf_file, "reread", self.service_name])
        print "Executing : supervisorctl update '%s' ..." % self.service_name
        supervisor_ctl_main(args=["-c", self.super_conf_file, "update", self.service_name])
        print "Executing : supervisorctl start '%s' ..." % self.service_name
        supervisor_ctl_main(args=["-c", self.super_conf_file, "start", self.service_name])
        print "Executing : supervisorctl status '%s' ..." % self.service_name
        supervisor_ctl_main(args=["-c", self.super_conf_file, "status", self.service_name])

    def status(self):
        print "Executing : supervisorctl status '%s' ..." % self.service_name
        supervisor_ctl_main(args=["-c", self.super_conf_file, "status", self.service_name])

    def remove(self):
        run_cmd('rm -rf %s' % self.service_conf_file)
        run_cmd('rm -rf %s' % self.service_work_dir)

        print "Executing : supervisorctl stop '%s' ..." % self.service_name
        supervisor_ctl_main(args=["-c", self.super_conf_file, "stop", self.service_name])
        print "Executing : supervisorctl status '%s' ..." % self.service_name
        supervisor_ctl_main(args=["-c", self.super_conf_file, "status", self.service_name])


    def remove_all(self):
        run_cmd('rm -rf %s/*' % self.super_conf_dir)
        run_cmd('rm -rf %s/*' % self.service_conf_dir)

        print "Executing : supervisorctl reread '%s' ..." % self.service_name
        supervisor_ctl_main(args=["-c", self.super_conf_file, "reread", self.service_name])
        print "Executing : supervisorctl update '%s' ..." % self.service_name
        supervisor_ctl_main(args=["-c", self.super_conf_file, "update", self.service_name])

