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
cf.read('eds.conf')

createURL = cf.get('eds', 'createURL')
describeURL = cf.get('eds', 'describeURL')
startURL = cf.get('eds', 'startURL')
rebootURL = cf.get('eds', 'rebootURL')
stopURL = cf.get('eds', 'stopURL')
terminateURL = cf.get('eds', 'terminateURL')
deleteURL = cf.get('eds', 'deleteURL')

class edsCluster:
    def __init__(self, token):
        self.token = token

    def create(self, conf, token=None):
        if token:
            self.token = token
        header = {'Content-Type':'application/json', 'X-AUTH-TOKEN':self.token}
        return requests.post(createURL, data=json.dumps(conf), headers=header)

    def describe(self, conf, token=None):
        if token:
            self.token = token
        header = {'Content-Type':'application/json', 'X-AUTH-TOKEN':self.token}
        return requests.post(describeURL, data=json.dumps(conf), headers=header)

    def start(self, edsId, token=None):
        if token:
            self.token = token
        header = {'Content-Type':'application/json', 'X-AUTH-TOKEN':self.token}
        return requests.get(startURL + edsId, headers=headers)

    def reboot(self, edsId, token=None):
        if token:
            self.token = token
        header = {'Content-Type':'application/json', 'X-AUTH-TOKEN':self.token}
        return requests.get(rebootURL + edsId, headers=header)

    def stop(self, edsId, token=None):
        if token:
            self.token = token
        header = {'Content-Type':'application/json', 'X-AUTH-TOKEN':self.token}
        return requests.get(stopURL + edsId, headers=header)

    def terminate(self, edsId, token=None):
        if token:
            self.token = token
        header = {'Content-Type':'application/json', 'X-AUTH-TOKEN':self.token}
        return requests.get(terminateURL + edsId, headers=header)

    def delete(self, edsId, token=None):
        if token:
            self.token = token
        header = {'Content-Type':'application/json', 'X-AUTH-TOKEN':self.token}
        return requests.get(deleteURL + edsId, headers=header)
