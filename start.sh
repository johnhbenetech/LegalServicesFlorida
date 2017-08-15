#!/bin/bash

pip3 install -r /home/django/requirements.txt
python3 /home/django/manage.py migrate
python3 /home/django/manage.py loaddata /home/django/fixtures/counties.json
python3 /home/django/manage.py loaddata /home/django/fixtures/languages.json
python3 /home/django/manage.py installtasks
echo yes | python3 /home/django/manage.py collectstatic
/usr/bin/supervisord -n