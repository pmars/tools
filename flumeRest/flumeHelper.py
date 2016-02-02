#!/home/xingming/pyvirt/bin/python
#-*- coding:utf-8 -*-

#############################################
# File Name: flumeHelper.py
# Author: xiaoh
# Mail: xiaoh@about.me 
# Created Time:  2016-01-20 16:30:58
#############################################

import redis
import socket
import subprocess
import os, errno
import ConfigParser
from supervisor.supervisorctl import main as supervisor_ctl_main

rd = redis.Redis()
flumePorts = 'FLUME_PORTS'

serviceRoot = '/path/to/service/'
superConfFile = os.path.join(serviceRoot, "supervisor.conf")

def _update_conf(dbName, tableName):
    serviceName = "%s_%s" % (dbName, tableName)
    ########################
    # generate flume.conf
    ########################
    rootDir = os.path.join(serviceRoot, 'services', serviceName)
    varDir = os.path.join(serviceRoot, 'var', serviceName)
    _mkdir_p(rootDir)
    _mkdir_p(varDir)
    flumeConf = os.path.join(rootDir, "flume.conf")
    checkpointDir = os.path.join(varDir, 'file-channel', 'checkpoint')
    dataDir = os.path.join(varDir, 'file-channel', 'data')
    newPort = _get_new_port()
    with open(flumeConf, 'w') as f:
        f.write(flumeTemplate.format(localPort=newPort, dbName=dbName, tableName=tableName, checkpointDir=checkpointDir, dataDir=dataDir))

    ##############################
    # generate supervisor handler
    ##############################
    superConfDir = os.path.join(serviceRoot, 'conf.d')
    flumeCmd = "flume-ng agent --conf {confPath} --conf-file {confFile} --name a1 -Dflume.root.logger=INFO,console -Djava.net.preferIPv4Stack=true".format(confPath=rootDir, confFile=flumeConf)
    superConf = {
        "command" : flumeCmd,
        "process_name" : serviceName,
        "directory" : rootDir,
        "stdout_logfile" : os.path.join(rootDir, "stdout_log"),
        "stderr_logfile" : os.path.join(rootDir, "stderr_log")
    }
    config = ConfigParser.RawConfigParser()
    sectionName = "program:"+serviceName
    config.add_section(sectionName)
    for key in superConf:
        config.set(sectionName, key, superConf[key])
    superConfPath = os.path.join(superConfDir, serviceName + ".conf")
    with open(superConfPath, "wb") as configfile:
        config.write(configfile)
    return newPort

def restart(dbName, tableName):
    stop(dbName, tableName)
    start(dbName, tableName)

def start(dbName, tableName):
    serviceName = "%s_%s" % (dbName, tableName)
    newPort = _update_conf(dbName, tableName)

    print "Executing : supervisorctl reread '%s' ..." % serviceName
    supervisor_ctl_main(args=["-c", superConfFile, "reread", serviceName])
    print "Executing : supervisorctl update '%s' ..." % serviceName
    supervisor_ctl_main(args=["-c", superConfFile, "update", serviceName])
    print "Executing : supervisorctl start '%s' ..." % serviceName
    supervisor_ctl_main(args=["-c", superConfFile, "start", serviceName])
    print "Executing : supervisorctl status '%s' ..." % serviceName
    supervisor_ctl_main(args=["-c", superConfFile, "status", serviceName])
    redis_set(serviceName, newPort)

def stop(dbName, tableName):
    serviceName = "%s_%s" % (dbName, tableName)
    _redis_del_port(serviceName)

    print "Executing : supervisorctl stop '%s' ..." % serviceName
    supervisor_ctl_main(args=["-c", superConfFile, "stop", serviceName])
    print "Executing : supervisorctl status '%s' ..." % serviceName
    supervisor_ctl_main(args=["-c", superConfFile, "status", serviceName])

    _clear_files(serviceName)

def status(dbName, tableName):
    serviceName = "%s_%s" % (dbName, tableName)

    print "Executing : supervisorctl status '%s' ..." % serviceName
    supervisor_ctl_main(args=["-c", superConfFile, "status", serviceName])

def _clear_files(serviceName):
    rootDir = os.path.join(serviceRoot, 'services', serviceName)
    varDir = os.path.join(serviceRoot, 'var', serviceName)
    superConf = os.path.join(serviceRoot, 'conf.d', serviceName + '.conf')
    runCmd('rm -rf %s' % rootDir)
    runCmd('rm -rf %s' % varDir)
    runCmd('rm -rf %s' % superConf)

def runCmd(cmd):
    return subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout.read()

def _get_new_port(startPort=10000, endPort=60000):
    usedPorts = _redis_list_ports()
    for port in xrange(startPort, endPort):
        if str(port) in usedPorts or port_is_openning(port):
            continue
        return port
    raise Exception('PortOver', 'all port used')

def redis_set(name, port, token=False):
    if not token:
        rd.sadd(flumePorts, port)
    rd.set(name, port)

def _redis_get_port(name):
    return rd.get(name)

def _redis_del_port(name):
    port = _redis_get_port(name)
    rd.delete(name)
    rd.srem(flumePorts, port)

def _redis_list_ports():
    return rd.smembers(flumePorts)

def port_is_openning(port):
    line = int(runCmd('netstat -an | grep %s | wc -l' % port).splitlines()[0])
    print 'Port:%s is Listen: (%s)' % (port, line > 0)
    return line > 0

def _mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: 
            raise

flumeTemplate = """
# Web ------> Logger

# Name the components on this agent
a1.sources = r1
a1.sinks = k1
a1.channels = c1

# Describe/configure the source
a1.sources.r1.type = http
a1.sources.r1.port = {localPort}
a1.sources.r1.interceptors = i1
a1.sources.r1.interceptors.i1.type = timestamp

#######################
# Sink : HDFS
#######################
a1.sinks.k1.type = hdfs
a1.sinks.k1.hdfs.path = /ingestion/{dbName}/{tableName}/%Y-%m-%d/%H
a1.sinks.k1.hdfs.filePrefix = ing
a1.sinks.k1.hdfs.round = true
a1.sinks.k1.hdfs.roundValue = 10
a1.sinks.k1.hdfs.roundUnit = minute

a1.sinks.k1.hdfs.rollInterval = 60
a1.sinks.k1.hdfs.rollCount = 8192
a1.sinks.k1.hdfs.idleTimeout = 60
a1.sinks.k1.hdfs.writeFormat = Text
a1.sinks.k1.hdfs.fileType = DataStream


#######################
# Channel
#######################
a1.channels.c1.capacity = 10000000
a1.channels.c1.transactionCapacity = 100000
a1.channels.c1.type = file
a1.channels.c1.checkpointDir = {checkpointDir}
a1.channels.c1.dataDirs = {dataDir}

# Bind the source and sink to the channel
a1.sources.r1.channels = c1
a1.sinks.k1.channel = c1
"""
