#!/bin/sh


echo "Migratsiyalar bajarilmoqda..."
python manage.py migrate --noinput

echo "Statik fayllar yig'ilmoqda..."
python manage.py collectstatic --noinput

echo "Gunicorn ishga tushirilmoqda..."
# 8000 portda tinglaydi
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3