#!/bin/bash
python3 MoneyGMA/manage.py makemigrations
python3 MoneyGMA/manage.py migrate
python3 MoneyGMA/manage.py migrate --run-syncdb
python3 MoneyGMA/manage.py collectstatic
gunicorn --bind 127.0.0.1:8122 --chdir MoneyGMA/ MoneyGMA.wsgi:application