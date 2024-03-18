#!/bin/sh

set -e

python3 manage.py migrate --noinput

daphne -b 0.0.0.0 wini_chat.asgi:application
