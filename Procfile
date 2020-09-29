web: python3 manage.py collectstatic --noinput
web: python3 manage.py 0.0.0.0:$PORT --noreload
web: gunicorn wiki.wsgi