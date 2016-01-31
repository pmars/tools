#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: xiaoh
# Mail: p.mars@163.com
# Created Time:  2015-12-11 01:25:34 AM
#############################################


from setuptools import setup, find_packages
import edsmodule

setup(
    name = "edsmodule",
    version = edsmodule.__version__,
    keywords = ("eds", "datacanvas", "xiaoh", "module", "ehc", "aps"),
    description = "the tool for export or import modules of datacanvas eds service",
    long_description = "the tool for export or import modules of datacanvas eds service",
    license = "MIT Licence",

    url = "http://xiaoh.me",
    author = "xiaoh",
    author_email = "xiaoh@about.me",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ["click", "plumbum", "requests"],

    scripts = ['bin/edsmodule']
#    entry_points = {
#        'console_scripts': [
#            'edsmodule = edsmodule.edsmodule:edsModule'
#        ]
#    }
)

