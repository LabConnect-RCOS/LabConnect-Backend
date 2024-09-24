#! /bin/sh

# Eventually add alembic migrations here
flask db upgrade
gunicorn app:app -w 6 --preload --max-requests-jitter 300 --bind 0.0.0.0:9000
