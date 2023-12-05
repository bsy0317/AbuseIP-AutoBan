#!/bin/bash

echo "===INSTALLING IPBAN Dependencies==="

mkdir /tmp/ipban

yum install -y gcc libffi-devel bzip2-devel ncurses-devel gdbm-devel xz-devel sqlite-devel readline-devel zlib-devel libuuid-devel xz git
cd /usr/local/src
curl -LO 'https://www.openssl.org/source/openssl-1.1.1f.tar.gz'
tar -xvf openssl-1.1.1f.tar.gz
cd openssl-1.1.1f
./config shared --prefix=/usr/local/openssl --openssldir=/usr/local/openssl
make
echo "===OPENSSL MAKE COMPLETE==="
make install
echo "===OPENSSL INSTALLED==="

echo "/usr/local/lib" >> /etc/ld.so.conf
echo "/usr/local/openssl/lib" >> /etc/ld.so.conf
ldconfig

cd /usr/local/src
curl -LO 'https://www.python.org/ftp/python/3.7.6/Python-3.7.6.tar.xz'
tar -xf Python-3.7.6.tar.xz
cd Python-3.7.6
./configure --prefix=/usr/local --enable-shared --with-openssl=/usr/local/openssl --with-system-ffi
make
echo "===PYTHON MAKE COMPLETE==="
make install
echo "===PYTHON INSTALLED==="

ldconfig
echo "===LD CONFIG COMPLETE==="
echo "===INSTALLING Python3 Dependencies==="
pip3 install rich

echo "===INSTALL COMPLETE==="

echo "===Backup Current iptables Config==="
mkdir ~/ipban > /dev/null 2>&1
curl -LO 'https://raw.githubusercontent.com/bsy0317/AbuseIP-AutoBan/main/ban_bulk.py' -o ~/ipban/ban_bulk.py
curl -LO 'https://raw.githubusercontent.com/bsy0317/AbuseIP-AutoBan/main/cron.sh' -o ~/ipban/cron.sh
python3 ~/ipban/ban_bulk.py backup

echo "===INSTALL Complete IPBAN==="

# echo "===INSTALLING CRON JOB==="
# echo "===Synchronize AbuseIP every 15 minutes==="
# echo "###Synchronize AbuseIP every 15 minutes" >> /var/spool/cron/root
# echo "*/15 * * * * /bin/sh /root/ipban/cron.sh > /root/ipban/cron.sh.log 2>&1" >> /var/spool/cron/root
# crontab -l
# service crond restart
# echo "===CRON JOB INSTALLED==="