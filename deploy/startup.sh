#!/bin/bash
set -e

echo "Starting startup script..."

# Iniciar Cloud SQL Proxy en segundo plano
/usr/local/cloud_sql_proxy corpus-451314:europe-west1:corpus-2026-instance --port 5432 &
PROXY_PID=$!

# Esperar a que Cloud SQL Proxy esté listo
sleep 5

# Función para logging
log_message() {
    echo "[$(date)] $1"
}

# Capturar errores
trap 'catch $? $LINENO' ERR
catch() {
    log_message "Error $1 occurred on line $2"
}

# Verificar el entorno
log_message "Checking environment..."
log_message "DJANGO_SETTINGS_MODULE = $DJANGO_SETTINGS_MODULE"
log_message "PORT = $PORT"
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

# Ejecutar migraciones con más detalle
log_message "Running migrations with verbose output..."
python manage.py showmigrations
python manage.py migrate --verbosity 3

# Recolectar archivos estáticos
log_message "Collecting static files..."
python manage.py collectstatic --noinput

# Iniciar Gunicorn
log_message "Starting Gunicorn..."
exec gunicorn Corpus2026.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --threads 4 --timeout 0 --access-logfile - --error-logfile - --capture-output --enable-stdio-inheritance --log-level debug

# Asegurarse de que Cloud SQL Proxy se detenga cuando el contenedor se detenga
trap "kill $PROXY_PID" SIGTERM
