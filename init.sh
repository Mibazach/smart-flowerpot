#!/bin/bash

export DJANGO_SECRET_KEY="your-secure-secret-key"
export DJANGO_DEBUG="True"
export DJANGO_ALLOWED_HOSTS="localhost,127.0.0.1"
export DB_ENGINE="django.db.backends.sqlite3"
export DB_NAME="your_database_name"
export DB_USER="your_database_user"
export DB_PASSWORD="your_database_password"
export DB_HOST="your_database_host"
export DB_PORT="your_database_port"


export DJANGO_SETTINGS_MODULE="smart_flowerpot.settings"
export GUNICORN_WORKERS=3 
export GUNICORN_BIND="0.0.0.0:8000"
export GUNICORN_TIMEOUT=120   