from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    """
    Usuario básico como AUTH_USER_MODEL.
    Solo añade 'nombre' y 'correo_electronico' como ejemplo.
    """
    nombre = models.CharField(max_length=150, blank=True)
    correo_electronico = models.EmailField(unique=True)

    USERNAME_FIELD = 'correo_electronico'
    REQUIRED_FIELDS = ['username']  # mantiene username para compatibilidad

    def __str__(self):
        return self.correo_electronico
