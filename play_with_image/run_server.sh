#!/usr/bin/env bash

python manage.py migrate --noinput
python manage.py collectstatic --noinput --clear

/usr/local/bin/gunicorn \
  --config python:gunicorn_config \
  play_with_image.wsgi