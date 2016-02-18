#!/usr/bin/python
#-*- coding:utf-8 -*-

#############################################
# File Name: ingestion_sql.py
# Author: xiaoh
# Mail: xiaoh@about.me 
# Created Time:  2016-02-03 18:17:44
#############################################


from prettytable import PrettyTable
import click, requests, json, time


@click.command()
@click.option('-h', '--host', required=True, help='Host of server')
@click.option('-p', '--port', default=18789, help='Post of server')
@click.option('-e', '--engine', default='mpp', 
        type=click.Choice(['mpp', 'hive']), help='Engine type')
@click.option('-d', '--db', required=True, help='Database name [mpp, hive]')
@click.option('-q', '--query', required=True, help='Query string')
def cli(host, port, engine, db, query):
    click.echo('host:%s, port:%s, engine:%s, db:%s, query:%s' % (host, port, engine, db, query))
    url = "http://%s:%s/v1/query" % (host, port)

    db_engine_map = {
        "mpp" : "pg",
        "hive" : "hive"
    }
    post_data = {"lang":db_engine_map[engine], "db": db, "query":query}
    r = requests.post(url, data=json.dumps(post_data))
#    click.echo("Response Status:%s" % r.status_code)
    if r.ok:
        js = r.json()
        if js['code'] == -1:
            click.echo('[ERROR] Query Failed: %s' % js['message'])
            return
        while True:
            time.sleep(2)
            status_json = _get_result(host, port, js['message'])
            if not status_json:
                click.echo("[ERROR] Invalid response: %s" % status_json.content)
                return
            if status_json['code'] == -1:
                click.echo("[ERROR] Query Failed: %s" % status_json['message'])
                return
            if status_json['code'] == 1 and status_json['dataSetList']:
                for data_set in status_json['dataSetList']:
                    _echo_result(data_set)
                break
            elif status_json['message'] == 'Processing':
                click.echo("Query results now, status:%s" % status_json['message'])
            else:
                click.echo("[ERROR] Invalid response: %s" % status_json)
                return
    else:
        click.echo("[ERROR] Query Failed: %s" % r.content)
        return
    print 'Query DONE'

def _echo_result(data_list):
    table = PrettyTable([column['name'] for column in data_list['columnHeaders']])
    for row in data_list['rows']:
        table.add_row([column['value'] for column in row['row']])
    click.echo(table)

def _get_result(host, port, uid):
    url = "http://%s:%s/v1/status?id=%s" % (host, port, uid)
    r = requests.get(url)
    if r.ok:
        return r.json()
    return None


if __name__ == "__main__":
    cli()

