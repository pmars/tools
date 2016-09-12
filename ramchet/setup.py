#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: xiaoh
# Mail: p.mars@163.com
# Created Time:  2015-12-11 01:25:34 AM
#############################################

from setuptools import setup, find_packages
import ramchet

setup(
    name = "ramchet",
    version = ramchet.__version__,
    keywords = ("zetyun", "eds", "aps", "update", "ramchet"),
    description = "update all components of eds and aps.",
    long_description = open('README.md').read(),
    license = "MIT Licence",

    url = "http://cloud.zetyun.com",
    author = "xiaoh",
    author_email = "xiaoh@about.me",

    packages = ['ramchet'],
    package_data = {
    },
    include_package_data = True,
    platforms = "any",
    install_requires = ["click"],

    scripts = ['bin/ramchet']
#    entry_points = {
#        'console_scripts': [
#            'ramchet = bin/ramchet'
#        ]
#    }
)

