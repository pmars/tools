#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: xiaoh
# Mail: p.mars@163.com
# Created Time:  2015-12-11 01:25:34 AM
#############################################

from setuptools import setup, find_packages
import fcon

setup(
    name = "fcon",
    version = fcon.__version__,
    keywords = ("find", "fcon", "xiaoh", "search", "content"),
    description = "show the files which contains the content you want to search.",
    long_description = "show the files which contains the content you want to search.",
    license = "MIT Licence",

    url = "https://github.com/pmars/tools/tree/master/fcon",
    author = "xiaoh",
    author_email = "xiaoh@about.me",

    packages = ['fcon'],
    package_data = {
    },
    include_package_data = True,
    platforms = "any",
    install_requires = ["click"],

    scripts = ['bin/fcon']
#    entry_points = {
#        'console_scripts': [
#            'fcon = bin/fcon'
#        ]
#    }
)

