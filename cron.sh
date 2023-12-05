#!/bin/bash

/usr/local/src/Python-3.7.6/python /root/ipban/ban_bulk.py reset
/usr/local/src/Python-3.7.6/python /root/ipban/ban_bulk.py

#export VISUAL=nano; crontab -e
###Synchronize AbuseIP every 30 minutes
#*/30 * * * * /bin/sh ~/ipban/cron.sh