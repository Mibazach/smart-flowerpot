#!/bin/bash

export DJANGO_SECRET_KEY="-kgxn9%xxgz=t=5y7-264g-0#l6ndhu+ztf1f3qz$ubzsawqbo"
export DJANGO_DEBUG="False"
export DJANGO_ALLOWED_HOSTS="localhost,127.0.0.1"
export DB_ENGINE="django.db.backends.sqlite3"


GUNICORN_WORKERS=3 
GUNICORN_BIND="0.0.0.0:8000"
GUNICORN_TIMEOUT=120   

gunicorn smart_flowerpot.wsgi:application \
    --workers $GUNICORN_WORKERS \
    --bind $GUNICORN_BIND \
    --timeout $GUNICORN_TIMEOUT \
    --log-level=info \
    --access-logfile - \
    --error-logfile -