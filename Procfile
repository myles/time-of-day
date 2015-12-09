manage: python manage.py assets build -q
web: gunicorn -w 4 -b 0.0.0.0:$PORT -k gevent timeofday:app
