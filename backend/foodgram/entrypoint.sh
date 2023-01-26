#!/usr/bin/env bash
python3 manage.py collectstatic --noinput
python3 manage.py migrate
gunicorn foodgram.wsgi:application --bind 0:8000
