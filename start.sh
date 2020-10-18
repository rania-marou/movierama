#!/usr/bin/env bash

# Run migrations
pipenv run python manage.py migrate

# Load fixtures
pipenv run python manage.py loaddata users movies votes

# Start service
pipenv run python manage.py runserver 0.0.0.0:8000