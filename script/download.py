#!/usr/bin/python
#-*- coding:utf-8 -*-

#############################################
# File Name: download.py
# Author: xiaoh
# Mail: xiaoh@about.me
# Created Time:  2016-06-18 11:12:28
#############################################

import sys, os, traceback
import shutil, time, uuid
import requests, functools
import logging, logging.handlers

def _mkdir(_dir):
    if not os.path.exists(_dir):
        os.mkdir(_dir)

root_dir = sys.path[0]
logs_dir = os.path.join(root_dir, 'logs')
file_dir = os.path.join(root_dir, 'file')
_mkdir(logs_dir)
_mkdir(file_dir)

logging.basicConfig(format='[%(asctime)s %(levelname)s %(filename)s:%(lineno)d] %(message)s', datefmt='%m-%d %H:%M')
logger = logging.getLogger('Download')
handler = logging.handlers.RotatingFileHandler(
        filename=os.path.join(logs_dir, 'download.log'),
        maxBytes=10240000,
        backupCount=3)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

def log(func):
    @functools.wraps(func)
    def wrapper(*args, **kw):
        logger.info('Excute %s() now. Params:%s' % (func.__name__, str(args[1:])))
        result = func(*args, **kw)
        logger.debug('Function: %s() done. Result:%s' % (func.__name__, result))
        return result
    return wrapper

@log
def down_page(url, callback, encode='utf-8', params=None):
    logger.info('download page "%s" now, callback function:%s, encoding:%s' % (url, callback, encode))
    try_times = 3
    while(try_times):
        try_times = try_times - 1
        header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/        537.36'}
        try:
            req = requests.get(url, headers=header, timeout=10)
            if req.status_code == 200:
                logger.debug('Download "%s" success, content length:%s' % (url, len(req.content)))
                callback(url, req.content.decode(encode), params=params)
                break
            else:
                logger.debug('Download "%s" failed with status_code:%s' % (url, req.status_code))
                time.sleep(1)
        except:
            logger.error(traceback.format_exc())
            time.sleep(1)

@log
def down_file(url, save_path=None, save_dir=None):
    logger.info('Download file "%s" now, save_path:%s, save_dir:%s' % (url, save_path, save_dir))
    file_path = save_path
    if not file_path:
        file_name = uuid.uuid1().get_hex()[0:12] + os.path.splitext(url)[-1]
        save_dir = save_dir if save_dir else file_dir
        file_path = os.path.join(save_dir, file_name)
    logger.info('Download file "%s" now, save to "%s"' % (url, file_path))
    try_times = 3
    while(try_times):
        try_times = try_times - 1
        header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/        537.36'}
        try:
            req = requests.get(url, stream=True, timeout=10)
            if req.status_code == 200:
                logger.debug('Download "%s" success, content length:%s' % (url, len(req.content)))
                with open(file_path, 'wb') as f:
                    req.raw.decode_content = True
                    shutil.copyfileobj(req.raw, f)
                return file_path
            else:
                logger.debug('Download "%s" failed with status_code:%s' % (url, req.status_code))
        except:
            logger.error(traceback.format_exc())
            time.sleep(1)
        return None

