release: mkdir static && cd MoneyGMA && python manage.py migrate && python manage.py collectstatic --noinput;
web: cd MoneyGMA && waitress-serve --listen=*:$PORT MoneyGMA.wsgi:application