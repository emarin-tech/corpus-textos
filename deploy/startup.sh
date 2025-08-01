#!/bin/bash
set -ex

echo "Starting startup script..."
echo "🔥 startup.sh comenzando..." >&2

# Configuración
INSTANCE_CONNECTION_NAME="corpus-451314:europe-southwest1:corpus-2026"
DB_PORT=5432

# Logging con timestamp
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# Iniciar Cloud SQL Proxy solo si se necesita
log "🔌 Starting Cloud SQL Proxy..."
/usr/local/bin/cloud-sql-proxy $INSTANCE_CONNECTION_NAME --port $DB_PORT &
PROXY_PID=$!

# Asegurar que se detiene cuando el contenedor termine
trap "log 'Stopping Cloud SQL Proxy...'; kill $PROXY_PID" SIGTERM


# Esperar a que Cloud SQL Proxy esté listo
sleep 5

# Esperar a que esté listo
sleep 5

# Mostrar entorno
log "Environment:"
log "DJANGO_SETTINGS_MODULE = ${DJANGO_SETTINGS_MODULE:-<not set>}"
log "PORT = ${PORT:-8000}"
log "Working directory: $(pwd)"
log "Contents: $(ls -la)"

# Crear carpeta de estáticos
log "📁 Creating staticfiles directory..."
mkdir -p staticfiles

# Verificar conexión a la base de datos
log "Checking database connection..."
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
exec gunicorn Corpus2026.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 2 \
    --threads 4 \
    --timeout 0 \
    --access-logfile - \
    --error-logfile - \
    --capture-output \
    --enable-stdio-inheritance \
    --log-level debug