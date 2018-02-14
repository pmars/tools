#! /bin/bash

log_path=/home/wwwroot/library.metricschina.com/logs
pid_path=/usr/local/nginx/logs/nginx.pid
date_str=`date -d yesterday +%Y%m%d`
echo ${date_str}

echo "mv ${log_path}/access_general.log ${log_path}/access_general.${date_str}.log"
mv ${log_path}/access_general.log ${log_path}/access_general.${date_str}.log

kill -USR1 `cat ${pid_path}`

echo "work done"
