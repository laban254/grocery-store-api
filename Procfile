web: gunicorn --chdir src grocery_api.wsgi:application --bind 0.0.0.0:$PORT
worker: celery -A grocery_api worker -l INFO
