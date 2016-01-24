#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: xiaoh
# Mail: p.mars@163.com
# Created Time:  2015-12-11 01:25:34 AM
#############################################


from setuptools import setup, find_packages

setup(
    name = "edsmodule",
    version = "0.1.1",
    keywords = ("eds", "datacanvas", "xiaoh", "module", "ehc", "aps"),
    description = "the tool for export or import modules of datacanvas eds service",
    long_description = "the tool for export or import modules of datacanvas eds service",
    license = "MIT Licence",

    url = "http://xiaoh.me",
    author = "xiaoh",
    author_email = "p.mars@163.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ["requests", "screwjack"],

    scripts = [],
    entry_points = {
        'console_scripts': [
            'edsmodule = edsmodule.edsmodule:edsModule'
        ]
    }
)

