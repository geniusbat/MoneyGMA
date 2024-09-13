#!/bin/bash
cd ..
python3 MoneyGMA/manage.py makemigrations
python3 MoneyGMA/manage.py migrate
python3 MoneyGMA/manage.py migrate --run-syncdb
gunicorn gunicorn --bind 127.0.0.1:8122 --error-logfile gunicorn-access.log MoneyGMA.wsgi:application --daemon