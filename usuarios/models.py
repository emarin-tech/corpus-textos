from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class Usuario(AbstractUser):
    # Datos personales
    nombre = models.CharField(max_length=150)
    apellidos = models.CharField(max_length=150)
    titulo = models.CharField(max_length=50, blank=True, null=True)

    # Contacto
    correo_electronico = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    foto = models.ImageField(upload_to='autores/fotos/', null=True, blank=True)

    # Autenticación externa
    google_id = models.CharField(max_length=255, unique=True, blank=True, null=True)
    USERNAME_FIELD = 'correo_electronico'
    REQUIRED_FIELDS = ['username']

    # Dirección
    calle = models.CharField(max_length=255, blank=True, null=True)
    ciudad = models.CharField(max_length=100, blank=True, null=True)
    provincia = models.CharField(max_length=100, blank=True, null=True)
    codigo_postal = models.CharField(max_length=20, blank=True, null=True)
    pais = models.CharField(max_length=100, blank=True, null=True)

    # Privacidad y comunicaciones
    acepta_politica_datos = models.BooleanField(default=False)
    acepta_correo_electronico = models.BooleanField(default=False)
    acepta_correo_postal = models.BooleanField(default=False)
    acepta_boletin = models.BooleanField(default=False)
    acepta_publicacion_contenido = models.BooleanField(default=False)
    acepta_condiciones_servicio = models.BooleanField(default=False)


    # Tiempos
    creado = models.DateTimeField(auto_now_add=True)
    modificado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.nombre} {self.apellidos}'

    class Meta:
        verbose_name = "usuario"
        verbose_name_plural = "usuarios"
