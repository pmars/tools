#!/home/xingming/pyvirt/bin/python
#-*- coding:utf-8 -*-

#############################################
# File Name: marktitle.py
# Author: xiaoh
# Mail: p.mars@163.com 
# Created Time:  2015-12-15 00:22:15
#############################################

import sys, os
import re

def main():
    if len(sys.argv) < 2:
        print '没有指定待整理的文件，程序即将退出！'
        return
    filename = sys.argv[1]
    
    if not os.path.isfile(filename):
        print '指定的整理文件错误，程序即将退出！'
        return

    content = ''
    with open(filename) as f:
        content = f.readlines()

    ticon = ''
    title = []
    catereg = re.compile('(?i)#+\s*(catelog|目录)')
    titlereg = re.compile('(?i)#+\s*\[([^]]+)\]\(#([^)]+)\)')
    match = False
    startMatch = False
    for line in content:
        # 查看是否需要生成目录
        if catereg.match(line):
            startMatch = True
        # 目录代码块不做工作
        if startMatch and line.startswith('---'):
            match = True
        # 如果需要生成目录
        if match:
            # 如果不是目录块，跳过
            tr = titlereg.match(line)
            if not tr:
                continue
            # 判断是几层标题
            length = 0
            while line.startswith('#'):
                length = length + 1
                line = line[1:]
            # 找到引用中的英文，加到链接进去
            en=''.join(re.compile('[^a-zA-Z0-9 ]').split(tr.group(1)))
            while en.startswith(' '):
                en = en[1:]
            en = en.replace(' ', '-')
            line = '[' + tr.group(1) + '](#' + en.lower() + tr.group(2).lower() + ')\n'
            # 清除上面的小标题（保证title里面都是从大到小的顺序）
            while len(title) > 0 and title[len(title)-1] >= length:
                title.pop()
            title.append(length)
            # 将此标题加入到目录表
            font = ''
            for i in range(1, len(title)):
                 font = font + '    '
            ticon = ticon + font + '0. ' + line

    upcon = ''
    catapart = False
    for line in content:
        if catereg.match(line):
            upcon = upcon + line
            upcon = upcon + '\n'
            upcon = upcon + ticon
            upcon = upcon + '\n'
            catapart = True
        if catapart and line.startswith('---'):
            catapart = False

        if catapart:
            continue

        upcon = upcon + line

    with open(filename, 'w') as f:
        f.write(upcon)

if __name__ == "__main__":
    main()

