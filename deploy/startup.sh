#!/bin/bash
set -e
echo "Iniciando contenedor..."

# Comprobamos que Django pueda arrancar
python manage.py migrate --noinput
python manage.py collectstatic --noinput

# Arrancamos gunicorn (Cloud Run escucha en $PORT)
exec gunicorn Corpus2026.wsgi:application --bind 0.0.0.0:${PORT}
