#!/usr/bin/python
#-*- coding:utf-8 -*-

#############################################
# File Name: hbase-cli.py
# Author: xiaoh
# Mail: xiaoh@about.me
# Created Time:  2016-04-01 15:52:35
#############################################

import click
import happybase

def pretty_print(msg):
    print msg.ljust(60, '*')

def put_row(table, column_family, value):
    pretty_print('insert one row to hbase, value:%s' % value)
    table.put('row_%s' % value, {
            '%s:name' % column_family:'name_%s' % value,
            '%s:addr' % column_family:'addr_%s' % value})

def put_rows(table, column_family, row_lines=3, start=0):
    pretty_print('insert rows to hbase now')
    for i in range(row_lines):
        put_row(table, column_family, i + start)

@click.group()
def cli():
    pass

@cli.command()
@click.option('-h', '--host', help='hbase thrift host', default='localhost')
@click.option('-p', '--port', help='hbase thrift port', default=9090)
@click.option('-t', '--table', help='hbase table name', required=True)
@click.option('-f', '--family', help='hbase table column family name', required=True)
@click.option('-l', '--line', help='number of data you want to insert', default=3)
@click.option('-s', '--start', help='start number of row', default=0)
def random_put(host, port, table, family, line, start):
    '''
       put random data(name,addr) to hbase table
    '''
    conn = happybase.Connection(host, port)
    table = conn.table(table)
    put_rows(table, family, line, start)

if __name__ == "__main__":
    cli()

