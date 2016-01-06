#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: edsConfig.py
# Author: xingming
# Mail: huoxm@zetyun.com 
# Created Time:  2016-01-06 17时56分14秒
#############################################

class edsConfig:
    def __init__(self, conf=None):
        self.ehc_setting = {}
        self.ehc_setting['name'] = ''
        self.ehc_setting['description'] = ''
        self.ehc_setting['id'] = None
        self.ehc_setting['vpc_id'] = None
        self.ehc_setting['status'] = None

        self.ehc_setting['user_setting'] = {}
        self.ehc_setting['user_setting']['user_id'] = None

        self.ehc_setting['cloud_setting'] = {}
        self.ehc_setting['cloud_setting']['password'] = None
        self.ehc_setting['cloud_setting']['type'] = 'aliyun'
        self.ehc_setting['cloud_setting']['region'] = 'cn-beijing'
        self.ehc_setting['cloud_setting']['zone'] = 'cn-beijing-a'
        self.ehc_setting['cloud_setting']['cidr'] = '192.168.0.0/24'
        self.ehc_setting['cloud_setting']['disk_size'] = 100

        self.ehc_setting['hadoop_setting'] = {}
        self.ehc_setting['hadoop_setting']['cluster_type'] = None
        self.ehc_setting['hadoop_setting']['master_type'] = None
        self.ehc_setting['hadoop_setting']['slave_type'] = None
        self.ehc_setting['hadoop_setting']['slave_num'] = 0
        
        self.ehc_setting['command_setting'] = {}
        self.ehc_setting['command_setting']['id'] = None
        self.ehc_setting['command_setting']['name'] = None
        self.ehc_setting['command_setting']['description'] = None
        self.ehc_setting['command_setting']['type'] = None
        self.ehc_setting['command_setting']['conf'] = None
