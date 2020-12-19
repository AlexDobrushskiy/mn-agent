#!/usr/bin/env bash
# start-server.sh
python manage.py migrate
python manage.py collectstatic
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
    (python manage.py createsuperuser --no-input)
fi
chown www-data:www-data /opt/app/server/db.sqlite3
gunicorn server.wsgi --daemon --user www-data --bind 0.0.0.0:8010 --workers 3
nginx -g "daemon off;"
