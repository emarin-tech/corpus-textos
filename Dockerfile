FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8080

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    wget \
    dos2unix \
    && rm -rf /var/lib/apt/lists/* \
    && wget https://dl.google.com/cloudsql/cloud_sql_proxy.linux.amd64 -O /usr/local/bin/cloud_sql_proxy \
    && chmod +x /usr/local/bin/cloud_sql_proxy

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x /app/deploy/startup.sh && dos2unix /app/deploy/startup.sh

EXPOSE 8080

CMD ["/app/deploy/startup.sh"]
