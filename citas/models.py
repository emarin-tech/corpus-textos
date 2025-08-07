# citas/models.py

from django.db import models
from usuarios.models import Usuario, Grupo
from publicaciones.models import Fuente

class Etiqueta(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    imagen = models.ImageField(upload_to='etiquetas/', null=True, blank=True)
    texto = models.TextField(null=True, blank=True)

    etiqueta_padre = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subetiquetas'
    )

    propietario_usuario = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='etiquetas_propias'
    )
    propietario_grupo = models.ForeignKey(
        Grupo,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='etiquetas_grupo'
    )

    creado = models.DateTimeField(auto_now_add=True)
    creado_por = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='etiquetas_creadas'
    )
    modificado = models.DateTimeField(auto_now=True)
    modificado_por = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='etiquetas_modificadas'
    )

    class Meta:
        verbose_name = "etiqueta"
        verbose_name_plural = "etiquetas"

    def __str__(self):
        return self.nombre


class Cita(models.Model):
    fuente = models.ForeignKey(Fuente, on_delete=models.CASCADE, related_name='citas')
    pagina = models.CharField(max_length=50, null=True, blank=True)
    imagen = models.ImageField(upload_to='citas/', null=True, blank=True)
    texto = models.TextField()

    etiquetas = models.ManyToManyField(Etiqueta, related_name='citas', blank=True)

    propietario_usuario = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='citas_propias'
    )
    propietario_grupo = models.ForeignKey(
        Grupo,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='citas_grupo'
    )

    creado = models.DateTimeField(auto_now_add=True)
    creado_por = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='citas_creadas'
    )
    modificado = models.DateTimeField(auto_now=True)
    modificado_por = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='citas_modificadas'
    )

    class Meta:
        verbose_name = "cita"
        verbose_name_plural = "citas"

    def __str__(self):
        return f"{self.fuente} - pág. {self.pagina or 'N/A'}"
