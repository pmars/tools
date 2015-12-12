#!/bin/bash

#############################################
# File Name: init.sh
# Author: xingming
# mail: huoxm@zetyun.com
# Created Time:  2015-12-12 18时00分07秒
#############################################

if [ $# -lt 2 ] then
    echo 'please input username and password'
    exit

user=$1
pass=$2

echo "username:"$user
echo "password:"$pass

exit
# add user to sudoers
sudo -i<<EOF
$pass
EOF
chmod 640 /etc/sudoers
echo "$user ALL=(ALL)   NOPASSWD:   ALL" >> /etc/sudoers
cat /etc/default/grub | awk 'BEGIN{con="";}{gsub("quiet splash", "quiet splash text"); con=con""$0"\n";}END{print con;}' > /etc/default/grub1
mv /etc/default/grub1 /etc/default/grub
update-grub
su $user
cd

sudo apt-get update
sudo apt-get install -y openssh-server python-pip python-virtualenv vim git tmux sauce
sudo mv .profile ../
sudo rm -rf *
sudo rm -rf .*
sudo rm -rf .config
virtualenv pyvirt

wget 
scp 182.92.172.215:/home/xingming/.bashrc ./
scp 182.92.172.215:/home/xingming/.vimrc ./
scp 182.92.172.215:/home/xingming/.dircolors ./
scp 182.92.172.215:/home/xingming/.tmux.info ./
source .bashrc
ssh-keygen -t rsa -P ''<<EOF

EOF

echo 'init over!'

exit
