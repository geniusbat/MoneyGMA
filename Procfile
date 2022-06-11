release: cd MoneyGMA && python manage.py migrate && mkdir static && python manage.py collectstatic --noinput;
web: cd MoneyGMA && waitress-serve --listen=*:$PORT MoneyGMA.wsgi:application