#!/home/xingming/pyvirt/bin/python
#-*- coding:utf-8 -*-

#############################################
# File Name: test.py
# Author: xiaoh
# Mail: p.mars@163.com 
# Created Time:  2016-01-06 21:24:54
#############################################

import edsCluster

token = 'your token for eds'

c = edsCluster.edsCluster(token)

r = c.describe({'ehc_setting':{'id':'e-3c925011e585f5'}})

print r.content

