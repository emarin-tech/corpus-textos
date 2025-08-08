from .base import *
import os
from decouple import config

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
    }
}

STRIPE_SECRET_KEY = config('STRIPE_SECRET_KEY')
STRIPE_PUBLISHABLE_KEY = config('STRIPE_PUBLISHABLE_KEY')
DJANGO_SECRET_KEY = config('DJANGO_SECRET_KEY')
SECRET_KEY = config('DJANGO_SECRET_KEY')

EMAIL_HOST = config("EMAIL_HOST")           # Ej: smtp.gmail.com
EMAIL_HOST_USER = config("EMAIL_HOST_USER") # Ej: info@emarintech.com
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
EMAIL_PORT = config("EMAIL_PORT")
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
