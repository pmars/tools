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
        self.name = ''
        self.description = ''
        self.eds_id = None
        self.vpc_id = None
        self.status = None

        self.user_setting = {}
        self.user_setting['user_id'] = None

        self.cloud_setting = {}
        self.cloud_setting['password'] = None
        self.cloud_setting['type'] = 'aliyun'
        self.cloud_setting['region'] = 'cn-beijing'
        self.cloud_setting['zone'] = 'cn-beijing-a'
        self.cloud_setting['cidr'] = '192.168.0.0/24'
        self.cloud_setting['disk_size'] = 100

        self.hadoop_setting = {}
        self.hadoop_setting['cluster_type'] = None
        self.hadoop_setting['master_type'] = None
        self.hadoop_setting['slave_type'] = None
        self.hadoop_setting['slave_num'] = 0
        
        self.command_setting = {}
        self.command_setting['id'] = None
        self.command_setting['name'] = None
        self.command_setting['description'] = None
        self.command_setting['type'] = None
        self.command_setting['conf'] = None

    def getJson(self):
        return {
            'ehc_setting': {
                'name':self.name, 
                'description':self.description, 
                'id':self.eds_id,
                'vpc_id':self.vpc_id,
                'status':self.status,
                'cloud_setting':self.cloud_setting, 
                'hadoop_setting':self.hadoop_setting, 
                'command_setting':self.command_setting
            }
        }
