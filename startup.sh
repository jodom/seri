#!/bin/bash

# Start Gunicorn process
echo Starting Gunicorn.
exec gunicorn core.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3
