#!/home/xingming/pyvirt/bin/python
#-*- coding:utf-8 -*-

#############################################
# File Name: flumeAPI.py
# Author: xiaoh
# Mail: xiaoh@about.me 
# Created Time:  2016-01-20 16:50:20
#############################################

import requests
from flask import Flask, request, jsonify
from flumeHelper import *

app = Flask(__name__)
cmd = "python -c 'from flumeHelper import {function}; {function}(\"{db}\",\"{table}\");'"

@app.route('/v1/api/<dbname>/<tablename>/create')
def create(dbname, tablename):
    print 'create api running now.'

    out = runCmd(cmd.format(function='start', db=dbname, table=tablename))
    print out
    state = formatOutput(out)
    return status(state)

@app.route('/v1/api/<dbname>/<tablename>/start')
def start(dbname, tablename):
    print 'start api running now.'
    out = runCmd(cmd.format(function='start', db=dbname, table=tablename))
    print out
    state = formatOutput(out)
    return status(state)

@app.route('/v1/api/<dbname>/<tablename>/stop')
def stop(dbname, tablename):
    print 'stop api running now.'
    out = runCmd(cmd.format(function='stop', db=dbname, table=tablename))
    print out
    state = formatOutput(out)
    return status(state)

@app.route('/v1/api/<dbname>/<tablename>/restart')
def restart(dbname, tablename):
    print 'restart api running now.'
    out = runCmd(cmd.format(function='restart', db=dbname, table=tablename))
    print out
    state = formatOutput(out)
    return status(state)

@app.route('/v1/api/<dbname>/<tablename>/status')
def status(dbname, tablename):
    print 'status api running now.'
    out = runCmd(cmd.format(function='status', db=dbname, table=tablename))
    print out
    state = formatOutput(out)
    return status(state)

@app.route('/v1/api/token', methods=['POST'])
def token():
    if not request.json:
        print 'not json'
        return status('no json format', 10001)
    username = request.json.get('username', None)
    token = request.json.get('token', None)
    print username, token
    if not username or not token:
        return status('Please provide a username and token', 10002)
    redis_set(username, token, True)
    return status('set token done.')

def status(msg, code=0):
    return jsonify({'message':msg, 'code':code})

def formatOutput(out):
    sl = out.split('\n')
    state = sl[-2].split()
    if len(state) > 1:
        return "%s:%s" % (state[0], state[1])
    return "%s:%s" % (state[0], 'Exception')

    return subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout.read()

def getToken():
    requests.get('http://hosttoservice/api/ehc/gettoken')
    pass

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8001, debug=True)
