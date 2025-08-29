import datetime
import secrets
from django.db import models
from django.conf import settings
from django.utils import timezone
from .managers import UsuarioManager
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

class Usuario(AbstractBaseUser, PermissionsMixin):
    # Datos personales
    nombre = models.CharField(max_length=150, blank=True, null=True)
    apellidos = models.CharField(max_length=150, blank=True, null=True)
    titulo = models.CharField(max_length=50, blank=True, null=True)

    # Contacto
    correo_electronico = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    foto = models.ImageField(upload_to='autores/fotos/', null=True, blank=True)

    # Autenticación externa
    google_id = models.CharField(max_length=255, unique=True, blank=True, null=True)
    objects = UsuarioManager()
    USERNAME_FIELD = 'correo_electronico'
    REQUIRED_FIELDS = []

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
    email_verificado = models.BooleanField(default=False)
    email_verificado_en = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    # (is_superuser lo aporta PermissionsMixin, pero en tu tabla puede ser columna booleana, OK)

    # Tiempos
    creado = models.DateTimeField(auto_now_add=True)
    modificado = models.DateTimeField(auto_now=True)

    def __str__(self):
        # usa el identificador como respaldo
        identificador = getattr(self, 'correo_electronico', None) or getattr(self, 'email', '')
        nombre = getattr(self, 'nombre', '') or ''
        apellidos = getattr(self, 'apellidos', '') or ''
        texto = (nombre + ' ' + apellidos).strip()
        return texto or identificador or f'Usuario {self.pk}'

    class Meta:
        verbose_name = "usuario"
        verbose_name_plural = "usuarios"

class EmailVerificacion(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token = models.CharField(max_length=64, unique=True)
    creado = models.DateTimeField(auto_now_add=True)
    expira = models.DateTimeField()

    @classmethod
    def crear(cls, usuario, horas=24):
        cls.objects.filter(usuario=usuario).delete()
        return cls.objects.create(
            usuario=usuario,
            token=secrets.token_urlsafe(32),
            expira=timezone.now() + datetime.timedelta(hours=horas),
        )

    def valido(self):
        return timezone.now() <= self.expira

class Grupo(models.Model):
    nombre = models.CharField(max_length=150)
    organizacion = models.CharField(max_length=255, blank=True, null=True)
    responsable = models.ForeignKey(
        'usuarios.Usuario',
        on_delete=models.CASCADE,
        related_name='grupos_creados'
    )

    tipo_membresia = models.CharField(max_length=50, blank=True, null=True)
    inicio_membresia = models.DateField(blank=True, null=True)
    fin_membresia = models.DateField(blank=True, null=True)
    membresia_cancelada_en = models.DateField(blank=True, null=True)
    logo = models.ImageField(upload_to='autores/fotos/', null=True, blank=True)

    creado = models.DateTimeField(auto_now_add=True)
    modificado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "grupo"
        verbose_name_plural = "grupos"

class UsuarioGrupo(models.Model):
    usuario = models.ForeignKey(
        'usuarios.Usuario',
        on_delete=models.CASCADE,
        related_name='membresias_grupo'
    )
    grupo = models.ForeignKey(
        Grupo,
        on_delete=models.CASCADE,
        related_name='miembros'
    )
    fecha_union = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)
    rol = models.CharField(max_length=50, default='miembro')  # 'miembro', 'editor', etc.

    class Meta:
        unique_together = ('usuario', 'grupo')
        verbose_name = "membresía de grupo"
        verbose_name_plural = "membresías de grupo"

    def __str__(self):
        return f'{self.usuario} en {self.grupo}'

