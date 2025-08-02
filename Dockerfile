FROM python:3.12-slim

# Variables de entorno para Python
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8080

# Instalar dependencias del sistema y Cloud SQL Proxy
RUN apt-get update && apt-get install -y \
    libpq-dev \
    build-essential \
    pkg-config \
    dos2unix \
    wget \
    && rm -rf /var/lib/apt/lists/* \
    && wget https://storage.googleapis.com/cloud-sql-connectors/cloud-sql-proxy/v2.8.0/cloud-sql-proxy.linux.amd64 -O /usr/local/bin/cloud-sql-proxy \
    && chmod +x /usr/local/bin/cloud-sql-proxy


# Establecer directorio de trabajo
WORKDIR /app

RUN pip list

# Copiar requirements.txt primero
COPY requirements.txt .
RUN pip install --verbose --no-cache-dir -r requirements.txt 2>&1 | tee pip_install.log
RUN pip install --verbose django-widget-tweaks==1.5.0


# Crear directorio para archivos estáticos
RUN mkdir -p staticfiles

# Copiar el resto del código
COPY . .

# Asegurarse que el script tiene permisos de ejecución
RUN chmod +x /app/deploy/startup.sh \
    && dos2unix /app/deploy/startup.sh

# Puerto que escuchará el contenedor
EXPOSE 8080

# Comando para iniciar la aplicación
CMD ["/app/deploy/startup.sh"]