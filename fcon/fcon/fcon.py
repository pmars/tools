#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: fcon.py
# Author: xiaoh
# Mail: p.mars@163.com
# Created Time:  2015-11-20 02:51:31 PM
#############################################

import sys, os, re, string
import click

__version__ = "0.0.1"

def version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo("Version: %s" % __version__)
    ctx.exit()

@click.command()
@click.option('-v', '--version', is_flag=True, is_eager=True, callback=version, expose_value=False)
@click.option('-p', '--search_path', default=os.getcwd(), help='Path for searching default:[%s]' % os.getcwd())
@click.option('-f', '--file_reg', default='', help='Regex string for searching files pattern default:[\'\']')
@click.option('-r', '--con_reg', default='', help='Regex string for searching content pattern default:[\'\']')
@click.option('--output/--no-output', default=False, help='Output logs default:[False]')
def cli(search_path, file_reg, con_reg, output):
    if not os.path.isdir(search_path):
        click.echo('[ERROR] Path for searching ERROR')
        return
    try:
        fr = re.compile(file_reg)
    except:
        click.echo('[ERROR] Regex string for searching files ERROR')
        return

    try:
        cr = re.compile('.*%s.*' % con_reg)
    except:
        click.echo('[ERROR] Regex string for searching content ERROR')
        return

    files = find_files(search_path, fr)

    for fi in files:
        if output:
            click.echo('SEARCHING FILE: "%s"' % fi)
        if is_text_file(fi):
            with open(fi) as f:
                lines = f.readlines()
                for index in xrange(len(lines)):
                    line = lines[index]
                    if cr.match(line):
                        click.echo("%3s, %s" % (str(index+1), line[0:-1]))

    click.echo('SEARCHING DONE.')

def find_files(dirPath, r):
    files = []
    for fd in os.listdir(dirPath):
        path = os.path.join(dirPath, fd)
        if os.path.isdir(path):
            files = files + find_files(path, r)
        else:
            if r.match(path):
                files.append(path)
    return files


text_char = "".join(map(chr, range(32, 127)) + list("\n\r\t\b"))
null_trans = string.maketrans("", "")
def is_text_file(filename, block_size=512):
    with open(filename) as f:
        s = f.read(block_size)
        if "\0" in s:       # if exist \0，binary file
            return False
        if not s:           # empty, text file
            return True
        t = s.translate(null_trans, text_char)
        return len(t)/len(s) < 0.3  # remove char over, less than 30% then text file

if __name__ == "__main__":
    cli()

