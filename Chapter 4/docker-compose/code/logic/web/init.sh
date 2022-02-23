#!/bin/bash

python manage.py init_db

exec "$@"