#!/usr/bin/bash

#Add @reboot  /home/user/startup.sh to cron to run it

cd <project_dir>
gunicorn --bind 127.0.0.1:8122 --error-logfile /var/logs/OverwatchGMA/moneygma-gunicorn-access.log MoneyGMA/MoneyGMA.wsgi:application --daemon