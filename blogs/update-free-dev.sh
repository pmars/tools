#!/bin/bash

#############################################
# File Name: update-free-dev.sh
# Author: xiaoh
# mail: xiaoh@about.me
# Created Time:  2016-03-21 13:17:40
#############################################

blog=2016-03-22-free-dev.markdown
root=/home/xingming/gitpro

cd $root/free-for-dev
git fetch upstream
git merge upstream/master

cat $root/tools/blogs/free-for-dev-header.md > $root/blogs/_posts/$blog
cat $root/free-for-dev/README.md | awk 'BEGIN {
    flag = 0;
}
{
    if (length($0) == 0) {
        flag = 0;
    }

    if (flag) {
        print "";
        flag = 0;
    }

    flag = 1;

    if (match($0, /\s*\*/) > 0){
        flag = 0;
    }

    if (length($0) == 0) {
        flag = 0;
    }

    gsub("```", "*");
    print $0;
}' >> $root/blogs/_posts/$blog

cd $root/blogs
badd _posts/$blog

git add _posts/$blog
git commit -m 'update free-for-dev blog'
git push

echo 'All work done'
