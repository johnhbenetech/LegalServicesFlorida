#!/bin/bash

pip3 install -r /home/django/requirements.txt
python3 /home/django/manage.py migrate
echo yes | python3 /home/django/manage.py collectstatic
/usr/bin/supervisord -n