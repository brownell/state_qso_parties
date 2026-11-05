#!/bin/sh
set -eu

exec gunicorn \
    --bind 0.0.0.0:8080 \
    --workers 1 \
    --threads 4 \
    app:app