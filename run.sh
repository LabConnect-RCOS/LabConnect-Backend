#! /bin/bash

# Eventually add alembic migrations here

gunicorn run:app -w 6 --preload --max-requests-jitter 300 --bind 0.0.0.0:9000