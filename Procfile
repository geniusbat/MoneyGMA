release: cd MoneyGMA && python manage.py migrate
web: cd MoneyGMA && waitress-serve --listen=*:$PORT MoneyGMA.wsgi:application