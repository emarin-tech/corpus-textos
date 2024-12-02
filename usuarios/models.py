# usuarios/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    TIPO_USUARIO = [
        ('normal', 'Usuario Normal'),
        ('premium', 'Usuario Premium'),
        ('grupo', 'Usuario de Grupo'),
    ]

    email = models.EmailField('email address', unique=True)  # Hacemos email único y requerido
    tipo_usuario = models.CharField(max_length=10, choices=TIPO_USUARIO, default='normal')
    institucion = models.CharField(max_length=255, blank=True)
    proposito_uso = models.TextField(blank=True)
    datos_pago = models.JSONField(null=True, blank=True)

    # Campos para OAuth
    google_id = models.CharField(max_length=255, blank=True, null=True)
    is_email_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'  # Usamos email como campo principal de autenticación
    REQUIRED_FIELDS = ['username']  # username sigue siendo requerido por AbstractUser

    def __str__(self):
        return self.email


class Grupo(models.Model):
    nombre = models.CharField(max_length=255)
    usuario_jefe = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name='grupos_administrados')
    miembros = models.ManyToManyField(Usuario, through='MembresiaGrupo', related_name='grupos')
    ciudad = models.CharField(max_length=255)
    pais = models.CharField(max_length=255)
    proposito_uso = models.TextField(blank=True)
    institucion = models.CharField(max_length=255, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)


class MembresiaGrupo(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    fecha_union = models.DateTimeField(auto_now_add=True)
    invitacion_token = models.CharField(max_length=100, unique=True, null=True, blank=True)
    estado = models.CharField(max_length=20, choices=[
        ('pendiente', 'Pendiente'),
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo')
    ])