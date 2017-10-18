#!/bin/bash

pip3 install -r /home/django/requirements.txt
python3 /home/django/manage.py makemigrations
python3 /home/django/manage.py migrate
python3 /home/django/manage.py loaddata /home/django/fixtures/counties.json
python3 /home/django/manage.py loaddata /home/django/fixtures/languages.json
python3 /home/django/manage.py loaddata /home/django/fixtures/problemcodes.json
echo yes | python3 /home/django/manage.py collectstatic
echo "from django.contrib.auth.models import User; User.objects.create_superuser('username', 'email', 'password')" | python3 /home/django/manage.py  shell
/usr/bin/supervisord -n