#!/home/xingming/pyvirt/bin/python
#-*- coding:utf-8 -*-

#############################################
# File Name: flumeDemo.py
# Author: xiaoh
# Mail: xiaoh@about.me 
# Created Time:  2016-02-01 15:10:05
#############################################

import click, requests, json
import uuid, random

@click.group()
def cli():
    pass

@click.command()
@click.option('-h', '--host', required=True, help='Host of data center')
@click.option('-p', '--port', required=True, help='Port of data center')
@click.option('-u', '--user', required=True, help='User of data center')
@click.option('-a', '--auth_token', required=True, help='Token of user')
@click.option('-d', '--db', required=True, help='Database name')
@click.option('-t', '--table', required=True, help='Table name')
@click.option('-v', '--version', default='v1', help='RestAPI version Default:[v1]')
def create(host, port, user, auth_token, db, table, version):
    _get_request(host, port, user, auth_token, db, table, version, "create")

@click.command()
@click.option('-h', '--host', required=True, help='Host of data center')
@click.option('-p', '--port', required=True, help='Port of data center')
@click.option('-u', '--user', required=True, help='User of data center')
@click.option('-a', '--auth_token', required=True, help='Token of user')
@click.option('-d', '--db', required=True, help='Database name')
@click.option('-t', '--table', required=True, help='Table name')
@click.option('-v', '--version', default='v1', help='RestAPI version Default:[v1]')
def start(host, port, user, auth_token, db, table, version):
    _get_request(host, port, user, auth_token, db, table, version, "start")

@click.command()
@click.option('-h', '--host', required=True, help='Host of data center')
@click.option('-p', '--port', required=True, help='Port of data center')
@click.option('-u', '--user', required=True, help='User of data center')
@click.option('-a', '--auth_token', required=True, help='Token of user')
@click.option('-d', '--db', required=True, help='Database name')
@click.option('-t', '--table', required=True, help='Table name')
@click.option('-v', '--version', default='v1', help='RestAPI version Default:[v1]')
def stop(host, port, user, auth_token, db, table, version):
    _get_request(host, port, user, auth_token, db, table, version, "stop")

@click.command()
@click.option('-h', '--host', required=True, help='Host of data center')
@click.option('-p', '--port', required=True, help='Port of data center')
@click.option('-u', '--user', required=True, help='User of data center')
@click.option('-a', '--auth_token', required=True, help='Token of user')
@click.option('-d', '--db', required=True, help='Database name')
@click.option('-t', '--table', required=True, help='Table name')
@click.option('-v', '--version', default='v1', help='RestAPI version Default:[v1]')
def restart(host, port, user, auth_token, db, table, version):
    _get_request(host, port, user, auth_token, db, table, version, "restart")

@click.command()
@click.option('-h', '--host', required=True, help='Host of data center')
@click.option('-p', '--port', required=True, help='Port of data center')
@click.option('-u', '--user', required=True, help='User of data center')
@click.option('-a', '--auth_token', required=True, help='Token of user')
@click.option('-d', '--db', required=True, help='Database name')
@click.option('-t', '--table', required=True, help='Table name')
@click.option('-v', '--version', default='v1', help='RestAPI version Default:[v1]')
def status(host, port, user, auth_token, db, table, version):
    _get_request(host, port, user, auth_token, db, table, version, "status")

@click.command()
@click.option('-h', '--host', required=True, help='Host of data center')
@click.option('-p', '--port', required=True, help='Port of data center')
@click.option('-u', '--user', required=True, help='User of data center')
@click.option('-a', '--auth_token', required=True, help='Token of user')
@click.option('-v', '--version', default='v1', help='RestAPI version Default:[v1]')
def token(host, port, user, auth_token, version):
    _set_token(host, port, user, auth_token, version)

@click.command()
@click.option('-h', '--host', required=True, help='Host of data center')
@click.option('-p', '--port', required=True, help='Port of data center')
@click.option('-u', '--user', required=True, help='User of data center')
@click.option('-a', '--auth_token', required=True, help='Token of user')
@click.option('-d', '--db', required=True, help='Database name')
@click.option('-t', '--table', required=True, help='Table name')
@click.option('--times', default=1, help='Times for upload data')
@click.option('--lines', default=1, help='Lines of upload data per time')
@click.option('-v', '--version', default='v1', help='RestAPI version Default:[v1]')
def post(host, port, user, auth_token, db, table, times, lines, version):
    _post(host, port, user, auth_token, db, table, times, lines, version)

@click.command()
@click.option('-h', '--host', required=True, help='Host of data center')
@click.option('-p', '--port', required=True, help='Port of data center')
@click.option('--lines', default=1, help='Lines of upload data per time')
def flume(host, port, lines):
    url = "http://%s:%s" % (host, port)
    data = _get_random_data(lines)
    post_data = []
    for body in data:
        post_data.append({"body":json.dumps(body)})
    r = requests.post(url, data=json.dumps(post_data))
    click.echo(r.status_code)
    if r.ok:
        click.echo(r.text)

cli.add_command(flume)
cli.add_command(create)
cli.add_command(start)
cli.add_command(stop)
cli.add_command(restart)
cli.add_command(status)
cli.add_command(token)
cli.add_command(post)

def _post(host, port, user, auth_token, db, table, times, lines, version):
    headers = {'X-USERNAME':user, 'X-AUTH-TOKEN':auth_token}
    url = "http://%s:%s/%s/%s/%s" % (host, port, version, db, table)
    r = None
    for time in xrange(times):
        data = _get_random_data(lines)
        r = requests.post(url, data=json.dumps(data), headers=headers)

        if times % max(1,times/5) == 0:
            print r.text

def _get_random_data(lines):
    data = []
    for i in xrange(lines):
        data.append({'name':uuid.uuid1().get_hex()[2:8], 'age':random.randint(0,200)})
    return data

def _set_token(host, port, user, auth_token, version):
    headers = {'content-type':'application/json'}
    data = {'username':user, 'token':auth_token}
    url = "http://%s:%s/%s/api/token" % (host, port, version)
    r = requests.post(url, data=json.dumps(data), headers=headers)
    print "Response Status:%s" % r.status_code
    if r.ok:
        print r.json()

def _get_request(host, port, user, auth_token, db, table, version, action):
    headers = {"X-USERNAME":user, "X-AUTH-TOKEN":auth_token}
    url = "http://%s:%s/%s/api/%s/%s/%s" % (host, port, version, db, table, action)
    r = requests.get(url, headers=headers)
    print "Response Status:%s" % r.status_code
    if r.ok:
        print r.json()

if __name__ == "__main__":
    cli()

