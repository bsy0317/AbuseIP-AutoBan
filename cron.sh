#!/bin/bash

python3 ~/ipban/ban_bulk.py reset
python3 ~/ipban/ban_bulk.py

#export VISUAL=nano; crontab -e
###Synchronize AbuseIP every 30 minutes
#*/30 * * * * /bin/sh ~/ipban/cron.sh