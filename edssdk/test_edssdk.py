#!/home/xingming/pyvirt/bin/python
#-*- coding:utf-8 -*-

#############################################
# File Name: test_edssdk.py
# Author: xiaoh
# Mail: p.mars@163.com 
# Created Time:  2016-01-07 11:54:53
#############################################

import json
from edssdk import edsCluster, edsConfig

token = 'your token of eds service'

def getEds():
    conf = edsConfig.edsConfig()
    cluster = edsCluster.edsCluster('eds.conf', token)
    return conf, cluster

def create():
    conf, cluster = getEds()
    conf.name = 'test edssdk'
#    conf.cloud_setting['region'] = 'cn-hangzhou'
#    conf.cloud_setting['zone'] = 'cn-hangzhou-a'
    conf.hadoop_setting['master_type'] = 'ecs.s2.large'
    conf.hadoop_setting['slave_type'] = 'ecs.s2.large'
    r = cluster.create(conf.getJson())
    if not r.ok:
        print 'requests post error'
    js = json.loads(r.content)
    print js['result']['ehc_setting']['id']
    with open('/tmp/edsid', 'w') as f:
        f.write(js['result']['ehc_setting']['id'])

def describe():
    with open('/tmp/edsid') as f:
        edsId = f.read()
    conf, cluster = getEds()
    conf.eds_id = edsId
    r = cluster.describe(conf.getJson())
    if not r.ok:
        print 'requests post error'
        return
    js = json.loads(r.content)
    print js['result'][0]['status']

def exception():
    with open('/tmp/edsid') as f:
        edsId = f.read()
    conf, cluster = getEds()
    conf.eds_id = edsId
    r = cluster.describe(conf.getJson())
    if not r.ok:
        print 'requests post error'
        return
    js = json.loads(r.content)
    print js['result'][0]['err_info']

def start():
    with open('/tmp/edsid') as f:
        edsId = f.read()
    conf, cluster = getEds()
    r = cluster.start(edsId)
    if not r.ok:
        print 'requests get error'
    else:
        print 'eds startting now.'

def reboot():
    with open('/tmp/edsid') as f:
        edsId = f.read()
    conf, cluster = getEds()
    r = cluster.reboot(edsId)
    if not r.ok:
        print 'requests get error'
    else:
        print 'eds reboot now.'

def stop():
    with open('/tmp/edsid') as f:
        edsId = f.read()
    conf, cluster = getEds()
    r = cluster.stop(edsId)
    if not r.ok:
        print 'requests get error'
    else:
        print 'eds stop now.'

def terminate():
    with open('/tmp/edsid') as f:
        edsId = f.read()
    conf, cluster = getEds()
    r = cluster.terminate(edsId)
    if not r.ok:
        print 'requests get error'
    else:
        print 'eds terminate now.'

def delete():
    with open('/tmp/edsid') as f:
        edsId = f.read()
    conf, cluster = getEds()
    r = cluster.delete(edsId)
    if not r.ok:
        print 'requests get error'
    else:
        print 'eds delete now.'

def main():
    while True:
        command = raw_input("input command(create,describe,exception,start,stop,reboot,terminate,delete,quit):")
        if command == 'create':
            create()
        elif command == 'describe':
            describe()
        elif command == 'exception':
            exception()
        elif command == 'start':
            start()
        elif command == 'reboot':
            reboot()
        elif command == 'stop':
            stop()
        elif command == 'terminate':
            terminate()
        elif command == 'delete':
            delete()
        elif command == 'quit':
            break
        else:
            print 'command error'
    print 'program will be quit now.'

if __name__ == "__main__":
    main()

