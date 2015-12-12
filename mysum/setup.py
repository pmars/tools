#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: xingming
# Mail: huoxm@zetyun.com 
# Created Time:  2015-12-10 11:25:34 AM
#############################################


from setuptools import setup, find_packages

setup(
    name = "sumi",
    version = "0.4",
    keywords = ("pip", "sum", "sumi", "xiaoh"),
    description = "sum function",
    long_description = open('sumi.py').read(),
    license = "MIT Licence",

    url = "http://xiaoh.me",
    author = "xiaoh",
    author_email = "huoxingming@gmail.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = []
)

