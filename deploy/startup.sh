#!/bin/bash
set -e

log_message() {
    echo "[$(date -u)] $1"
}
export DJANGO_SETTINGS_MODULE=Corpus2026.settings.produccion

log_message "DJANGO_SETTINGS_MODULE = $DJANGO_SETTINGS_MODULE"


echo "Starting startup script..."

# Esperar a que Cloud SQL Proxy esté listo
sleep 5

# Capturar errores
trap 'catch $? $LINENO' ERR
catch() {
    log_message "Error $1 occurred on line $2"
}

# Verificar el entorno
log_message "Checking environment..."
export DB_NAME=${DB_NAME}
export DB_USER=${DB_USER}
export DB_PASSWORD=${DB_PASSWORD}
export DB_PORT=${DB_PORT}
export DB_HOST=${DB_HOST}
export STRIPE_SECRET_KEY=${STRIPE_SECRET_KEY}
export STRIPE_PUBLISHABLE_KEY=${STRIPE_PUBLISHABLE_KEY}
export DJANGO_SECRET_KEY=${DJANGO_SECRET_KEY}
export PORT="${PORT:-8080}"  # fallback sano

log_message "DJANGO_SETTINGS_MODULE = $DJANGO_SETTINGS_MODULE"
log_message "PORT = $PORT"
# Dump filtrado para ver si Cloud Run ha inyectado los EMAIL_* (sin valores sensibles)
[ -n "${EMAIL_HOST:-}" ] && log_message "EMAIL_HOST present" || log_message "EMAIL_HOST MISSING"
[ -n "${EMAIL_HOST_USER:-}" ] && log_message "EMAIL_HOST_USER present" || log_message "EMAIL_HOST_USER MISSING"
[ -n "${EMAIL_HOST_PASSWORD:-}" ] && log_message "EMAIL_HOST_PASSWORD present" || log_message "EMAIL_HOST_PASSWORD MISSING"
[ -n "${EMAIL_PORT:-}" ] && log_message "EMAIL_PORT present" || log_message "EMAIL_PORT MISSING"

log_message "Current directory: $(pwd)"
log_message "Directory contents: $(ls -la)"

# Crear directorio para archivos estáticos
log_message "Creating static directory..."
mkdir -p staticfiles

# Verificar la conexión a la base de datos
log_message "Checking database connection..."
python -c "
import django
django.setup()
from django.db import connections
connections['default'].ensure_connection()
"


echo "[INFO] Ejecutando migraciones..."
python manage.py migrate --noinput --settings=Corpus2026.settings.produccion

echo "Recolectando archivos estáticos..."
python manage.py collectstatic --noinput --settings=Corpus2026.settings.produccion

# Iniciar Gunicorn
log_message "Starting Gunicorn..."
exec gunicorn Corpus2026.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --threads 4 --timeout 0 --access-logfile - --error-logfile - --capture-output --enable-stdio-inheritance --log-level info
