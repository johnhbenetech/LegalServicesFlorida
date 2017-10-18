python manage.py makemigrations
python manage.py migrate
python manage.py loaddata ./fixtures/counties.json

python manage.py loaddata ./fixtures/languages.json

python manage.py loaddata ./fixtures/problemcodes.json



@echo on
echo yes|python manage.py collectstatic

