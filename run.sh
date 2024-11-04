#!/bin/bash

source inti.sh

gunicorn smart_flowerpot.wsgi:application \
    --workers $GUNICORN_WORKERS \
    --bind $GUNICORN_BIND \
    --timeout $GUNICORN_TIMEOUT \
    --log-level=info \
    --access-logfile - \
    --error-logfile -