#!/home/xingming/pyvirt/bin/python
#-*- coding:utf-8 -*-

#############################################
# File Name: edsCluster.py
# Author: xiaoh
# Mail: p.mars@163.com 
# Created Time:  2016-01-06 18:03:18
#############################################

import ConfigParser
import requests, json

cf = ConfigParser.ConfigParser()

class edsCluster:
    def __init__(self, confPath, token=None):
        cf.read(confPath)
        self.createURL = cf.get('eds', 'createURL')
        self.describeURL = cf.get('eds', 'describeURL')
        self.startURL = cf.get('eds', 'startURL')
        self.rebootURL = cf.get('eds', 'rebootURL')
        self.stopURL = cf.get('eds', 'stopURL')
        self.terminateURL = cf.get('eds', 'terminateURL')
        self.deleteURL = cf.get('eds', 'deleteURL')

        self.token = token

    def create(self, conf, token=None):
        if token:
            self.token = token
        header = {'Content-Type':'application/json', 'X-AUTH-TOKEN':self.token}
        return requests.post(self.createURL, data=json.dumps(conf), headers=header)

    def describe(self, conf, token=None):
        if token:
            self.token = token
        header = {'Content-Type':'application/json', 'X-AUTH-TOKEN':self.token}
        return requests.post(self.describeURL, data=json.dumps(conf), headers=header)

    def start(self, edsId, token=None):
        if token:
            self.token = token
        header = {'Content-Type':'application/json', 'X-AUTH-TOKEN':self.token}
        return requests.get(self.startURL + edsId, headers=headers)

    def reboot(self, edsId, token=None):
        if token:
            self.token = token
        header = {'Content-Type':'application/json', 'X-AUTH-TOKEN':self.token}
        return requests.get(self.rebootURL + edsId, headers=header)

    def stop(self, edsId, token=None):
        if token:
            self.token = token
        header = {'Content-Type':'application/json', 'X-AUTH-TOKEN':self.token}
        return requests.get(self.stopURL + edsId, headers=header)

    def terminate(self, edsId, token=None):
        if token:
            self.token = token
        header = {'Content-Type':'application/json', 'X-AUTH-TOKEN':self.token}
        return requests.get(self.terminateURL + edsId, headers=header)

    def delete(self, edsId, token=None):
        if token:
            self.token = token
        header = {'Content-Type':'application/json', 'X-AUTH-TOKEN':self.token}
        return requests.get(self.deleteURL + edsId, headers=header)
