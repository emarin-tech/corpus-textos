from .base import *
import os

# a ver
# Inicializa el cliente de Secret Manager
ALLOWED_HOSTS = ['*']
# Tu ID del proyecto en GCP
GCP_PROJECT_ID = os.getenv('GOOGLE_CLOUD_PROJECT', 'corpus-451314')  # valor por defecto opcional
DEBUG = False
import os

def get_secret(name):
    use_secret_manager = os.getenv("USE_SECRET_MANAGER", "false").lower() == "true"

    if use_secret_manager:
        try:
            from google.cloud import secretmanager
            client = secretmanager.SecretManagerServiceClient()
            project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
            if not project_id:
                raise RuntimeError("GOOGLE_CLOUD_PROJECT is not set.")
            secret_name = f"projects/{project_id}/secrets/{name}/versions/latest"
            response = client.access_secret_version(request={"name": secret_name})
            return response.payload.data.decode("UTF-8")
        except Exception as e:
            raise RuntimeError(f"Error accessing secret {name}: {e}")
    else:
        val = os.getenv(name)
        if val is None:
            raise RuntimeError(f"Secret {name} not found in environment variables.")
        return val


# Configuración de base de datos
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': get_secret('DB_NAME'),
        'USER': get_secret('DB_USER'),
        'PASSWORD': get_secret('DB_PASSWORD'),
        'HOST': get_secret('DB_HOST'),
        'PORT': get_secret('DB_PORT'),
    },

}

# Stripe
STRIPE_SECRET_KEY = get_secret('STRIPE_SECRET_KEY')
STRIPE_PUBLISHABLE_KEY = get_secret('STRIPE_PUBLISHABLE_KEY')

# Archivos estáticos y media
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')