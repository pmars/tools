#!/bin/bash

#############################################
# File Name: blog-jekyll-test.sh
# Author: xiaoh
# mail: xiaoh@about.me
# Created Time:  2016-03-22 16:14:26
#############################################

if [ $# -lt 1 ] ; then
    echo '输入待提交的博客路径'
    exit 1
fi

dir=/home/xingming/gitpro/blogs
file=$1

cd $dir
git add $file
git commit -m "modify $file for test jekyll script"
git push

echo "All work done"
