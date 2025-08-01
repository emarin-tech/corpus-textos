from .base import *
import os
from google.cloud import secretmanager

# Inicializa el cliente de Secret Manager
client = secretmanager.SecretManagerServiceClient()

# Tu ID del proyecto en GCP
GCP_PROJECT_ID = os.getenv('corpus-451314')

def get_secret(secret_id, version="latest"):
    secret_name = f"projects/{GCP_PROJECT_ID}/secrets/{secret_id}/versions/{version}"
    response = client.access_secret_version(request={"name": secret_name})
    return response.payload.data.decode("UTF-8")

# Configuración de base de datos
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': get_secret('DB_NAME'),
        'USER': get_secret('DB_USER'),
        'PASSWORD': get_secret('DB_PASSWORD'),
        'HOST': get_secret('DB_HOST'),
        'PORT': get_secret('DB_PORT'),
    }
}

# Stripe
STRIPE_SECRET_KEY = get_secret('STRIPE_SECRET_KEY')
STRIPE_PUBLISHABLE_KEY = get_secret('STRIPE_PUBLISHABLE_KEY')

# Archivos estáticos y media
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATICFILES_DIRS = [BASE_DIR.parent / 'static']