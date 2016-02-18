#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests, click

@click.command()
@click.option('-h', '--host', required=True, help='Host of data center')
@click.option('-u', '--user', required=True, help='User of data center')
@click.option('-a', '--auth_token', required=True, help='Token of user')
@click.option('-d', '--db', required=True, help='Database name')
@click.option('-t', '--table', required=True, help='Table name')
@click.option('-v', '--version', default='v1', help='RestAPI version Default:[v1]')
def create_update_schema(host, user, auth_token, db, table, version):
    """
        Create ingestion service for upload data
    """
    _create_update_schema(host, db, table)

def _create_update_schema(host, db, table):
    """
    Create or Update Table Schema.

    :return: None
    """
    url = "http://%s:7080/v1/table/create/%s/%s" % (host, db, table)
    schema_body = {
        "table_name": "demo_table",
        "schema" : {
            "source_date": "DATE",
            "source_host": "STRING",
            "ua": "STRING",
            "referer": "STRING",
            "e": "STRING",
            "site": "STRING",
            "cpi": "STRING",
            # "localtimestamp": "TIMESTAMP",
            "ltimestamp": "TIMESTAMP",
            "tags": "STRING",
            "uuid": "STRING",
            "ip": "STRING",
            "ssid": "STRING"
        }
    }
    params = {
        "owner": "demo"
    }
    r = requests.post(url, params = params, json = body)
    print r.status_code
    print r.content

def main():
    create_update_schema()

if __name__ == "__main__":
    main()
