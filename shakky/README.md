---
layout:     post
title:      "shakky Rest API"
subtitle:   "shakky REST-API LIST"
date:       2016-05-02 02:34:50
author:     "xiaoh"
header-img: "img/post-bg-default.jpg"
tags:
    - shakky
    - readme
---

# shakky 模块

---

shakky 是一个脚本（命令等）定时执行的 WebService 框架，它提供了 RestAPI 来帮助开发人员更容易的将脚本设置成一个定时任务。

---

## Rest-API

### 系统信息

##### CPU

URL | `/api/v1/cpu`
方法| GET
简介|查看系统CPU使用信息

---

##### Machine

URL | `/api/v1/machine`
方法| GET 
简介| 查看系统综合信息

---

##### Memory

URL | `/api/v1/memory`
方法| GET
简介| 看系统内存信息

---

##### Disk

URL | `/api/v1/disk`
方法| GET
简介| 查看系统磁盘信息

---

##### Network

URL | `/api/v1/network`
方法| GET 
简介| 查看系统网络信息

---

##### Spider

###### 查看爬虫信息

URL | `/api/v1/spider?name=<spider_name>`
方法| GET
简介| 返回相关爬虫的所有信息

###### 创建爬虫

URL | `/api/v1/spider?name=<spider_name>&mins=<mins>&hour=<hour>&days=<days>&month=<month>`
files| {"command":`<spider_running_command>`, "script":`<stream_of_file>`}
方法| PUT
简介|上传一个爬虫脚本(爬虫脚本可以是一个.tar.gz文件)，创建爬虫

###### 删除爬虫

URL | `/api/v1/spider?name=<spider_name>`
方法| DELETE
简介| 通过爬虫名称删除爬虫

---

##### SpiderModify

URL | `/api/v1/spidermodify?name=<spider_name>&mins=<mins>&hour=<hour>&days=<days>&month=<month>`
方法| GET
简介| 修改爬虫的执行时间

---

##### SpiderStart

URL | `/api/v1/spiderstart?name=<spider_name>`
方法| GET
简介| 通过爬虫名称启动一个爬虫

---

##### SpiderLog

URL | `/api/v1/spiderlog?name=<spider_name>&line=<line>`
方法| GET
简介| 获取爬虫的LOG

---

##### SpiderList

###### 查看爬虫列表

URL | `/api/v1/spiderlist`
方法| GET
简介| 列出所有爬虫脚本信息

###### 删除所有爬虫

URL | `api/v1/spiderlist`
方法| DELETE
简介| 删除所有爬虫

---

## Contact

If you have any questions, welcome to send an email to <a class="email" href="mailto:xiaoh@about.me">xiaoh@about.me</a>

---

## Blog

Welcom to my blog: http://www.xiaoh.me

---

### END

