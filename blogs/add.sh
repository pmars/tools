#!/bin/bash

#############################################
# File Name: add.sh
# Author: xiaoh
# mail: xiaoh@about.me
# Created Time:  2016-01-27 16:15:52
#############################################


if [ $# -lt 1 ] ; then
    echo '输入你想添加的文件'
    exit
fi

echo '开始执行添加程序'
echo '添加文件为：'$1

scriptdir=/home/xingming/gitpro/tools/blogs
python $scriptdir/marktitle.py $1
python $scriptdir/sitemap.py $1

echo '添加程序已完成'
exit
