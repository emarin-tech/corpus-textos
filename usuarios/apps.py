from django.apps import AppConfig
from django.db.utils import ProgrammingError, OperationalError

class UsuariosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'usuarios'