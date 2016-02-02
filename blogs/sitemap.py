#!/home/xingming/pyvirt/bin/python
#-*- coding:utf-8 -*-

#############################################
# File Name: sitemap.py
# Author: xiaoh
# Mail: p.mars@163.com 
# Created Time:  2016-01-10 15:21:43
#############################################

import os, sys, re


def main():
    if len(sys.argv) < 2:
        print '没有指定待整理的文件，程序即将退出！'
        return
    filename = sys.argv[1]

    if not os.path.isfile(filename):
        print '指定的整理文件错误，程序即将退出！'
        return

    sitefile = '/home/xingming/gitpro/blogs/xiaoh_sitemap.xml'
    if len(sys.argv) > 2:
        if not os.path.isfile(sitefile):
            print '指定的地图文件错误，程序即将退出！'
        else:
            sitefile = sys.argv[2]

    with open(sitefile) as f:
        sitecon = f.readlines()

    r = re.compile("([a-zA-Z0-9_-]*/)*([^\\/]*?)\.[a-zA-Z0-9_-]*$")
    html = r.match(filename).group(2).replace('-', '/', 3)

    if ''.join(sitecon).find(html) != -1:
        return

    sitecon.insert(-1, '    <url>\n')
    sitecon.insert(-1, '        <loc>http://www.xiaoh.me/%s/</loc>\n' % html)
    sitecon.insert(-1, '        <changefreq>daily</changefreq>\n')
    sitecon.insert(-1, '        <priority>0.8</priority>\n')
    sitecon.insert(-1, '    </url>\n')

    with open(sitefile, 'w') as f:
        f.writelines(sitecon)

if __name__ == "__main__":
    main()

