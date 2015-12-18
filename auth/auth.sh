#!/bin/bash

#############################################
# File Name: auth.sh
# Author: xiaoh
# mail: p.mars@163.com
# Created Time:  2015-12-18 02:18:03
#############################################

# make sure you have install ansible
# or
# sudo apt-get install python-pip
# sudo apt-get install python-virtualenv
# virtualenv pyvirt
# source pyvirt/bin/activate
# pip install ansible


if [ $# -lt 3 ] ; then
    echo 'input host, name, password please'
    exit
fi

host=$1
name=$2
pass=$3

if [ $name == 'root' ] ; then
    path='/root'
else
    path="/home/$name"
fi

echo 'init hosts file'
echo "[all]" > /tmp/hosts.tmp
echo "$host ansible_ssh_user=$name  ansible_ssh_pass=$pass  ansible_connection=paramiko" >> /tmp/hosts.tmp

echo "ansible to $host"
ansible all -i /tmp/hosts.tmp -m copy -a "src=~/.ssh/id_rsa.pub dest=/tmp/key"
ansible all -i /tmp/hosts.tmp -m shell -a "mkdir -p $path/.ssh"
ansible all -i /tmp/hosts.tmp -m shell -a "cat /tmp/key >> $path/.ssh/authorized_keys"
ansible all -i /tmp/hosts.tmp -m shell -a "rm /tmp/key"

echo "clear hosts file"
rm /tmp/hosts.tmp

exit
