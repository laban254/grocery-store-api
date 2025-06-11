#!/bin/bash

# Run migrations
python src/manage.py migrate

# Collect static files
python src/manage.py collectstatic --noinput
