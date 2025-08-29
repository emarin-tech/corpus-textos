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
SECRET_KEY = get_secret('DJANGO_SECRET_KEY')
DJANGO_SECRET_KEY = get_secret('DJANGO_SECRET_KEY')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATIC_URL = '/static/'
STATIC_ROOT = '/app/staticfiles'

MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
SOCIAL_AUTH_REDIRECT_IS_HTTPS = True  # en Cloud Run detrás de HTTPS

EMAIL_HOST = get_secret('EMAIL_HOST')           # Ej: smtp.gmail.com
EMAIL_HOST_USER = get_secret('EMAIL_HOST_USER') # Ej: info@emarintech.com
EMAIL_HOST_PASSWORD = get_secret('EMAIL_HOST_PASSWORD')
EMAIL_PORT = get_secret('EMAIL_PORT')
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
DEFAULT_FROM_EMAIL = f'Corpus <{EMAIL_HOST_USER}>'
SERVER_EMAIL = DEFAULT_FROM_EMAIL

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = get_secret('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = get_secret('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# MUY IMPORTANTE: orígenes de confianza (con esquema)
CSRF_TRUSTED_ORIGINS = [
    "https://corpus2026-132887978036.europe-west1.run.app",
    # "https://tu-dominio.com"
]

import os

USE_GCS = os.environ.get("USE_GCS") == "1"
if USE_GCS:
    INSTALLED_APPS += ["storages"]
    DEFAULT_FILE_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
    GS_BUCKET_IMAGENES_NOMBRE = os.environ.get("GS_BUCKET_IMAGENES_NOMBRE", "corpus-imagenes")
    GS_DEFAULT_ACL = None  # acceso uniforme en el bucket
    GS_OBJECT_PARAMETERS = {"cache_control": "public, max-age=86400"}
    MEDIA_URL = f"https://storage.googleapis.com/{GS_BUCKET_IMAGENES_NOMBRE}/"
else:
    MEDIA_URL = "/media/"
    MEDIA_ROOT = BASE_DIR / "media"
