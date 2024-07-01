#!/bin/sh

# wait for PSQL server to start
sleep 10

su  -c "python manage.py makemigrations "
su -c "python manage.py migrate"
su -c "python manage.py runserver 0.0.0.0:8000"