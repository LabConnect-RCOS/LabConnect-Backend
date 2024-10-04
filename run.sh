#! /bin/sh
set -e  # Fail on any error

# Migrate DB
flask db upgrade || exit 1

# Run the app
gunicorn app:app -w 6 --preload --max-requests-jitter 300 --bind 0.0.0.0:9000 || exit 1