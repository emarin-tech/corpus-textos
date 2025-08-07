# publicaciones/models.py

from django.db import models
from usuarios.models import Usuario  # o el nombre correcto del modelo extendido

class GrupoEditorial(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    ciudad = models.CharField(max_length=255, blank=True, null=True)
    pais = models.CharField(max_length=255, blank=True, null=True)
    sitio_web = models.URLField(blank=True, null=True)
    logo = models.ImageField(upload_to='grupos_editoriales/logos/', null=True, blank=True)

    creado = models.DateTimeField(auto_now_add=True)
    creado_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, related_name='grupos_editoriales_creados', null=True, blank=True)
    modificado = models.DateTimeField(auto_now=True)
    modificado_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, related_name='grupos_editoriales_modificados', null=True, blank=True)

    propietario_usuario = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='grupo_editorial_propietario_usuario'
    )
    propietario_grupo = models.ForeignKey(
        'usuarios.Grupo',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='grupo_editorial_propietario_grupo'
    )

    notas = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "grupo editorial"
        verbose_name_plural = "grupos editoriales"

class Editorial(models.Model):
    nombre = models.CharField(max_length=255)
    grupo_editorial = models.ForeignKey(GrupoEditorial, on_delete=models.SET_NULL, related_name='editoriales', null=True, blank=True)
    logo = models.ImageField(upload_to='editoriales/logos/', null=True, blank=True)

    creado = models.DateTimeField(auto_now_add=True)
    creado_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, related_name='editoriales_creadas', null=True, blank=True)
    modificado = models.DateTimeField(auto_now=True)
    modificado_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, related_name='editoriales_modificadas', null=True, blank=True)

    notas = models.TextField(null=True, blank=True)

    propietario_usuario = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='editorial_propietario_usuario'
    )
    propietario_grupo = models.ForeignKey(
        'usuarios.Grupo',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='editorial_propietario_grupo'
    )

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "editoria "
        verbose_name_plural = "editoriales"

class Autor(models.Model):
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=150)
    foto = models.ImageField(upload_to='autores/fotos/', null=True, blank=True)

    creado = models.DateTimeField(auto_now_add=True)
    creado_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, related_name='autores_creados', null=True, blank=True)
    modificado = models.DateTimeField(auto_now=True)
    modificado_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, related_name='autores_modificados', null=True, blank=True)

    propietario_usuario = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='autor_propietario_usuario'
    )
    propietario_grupo = models.ForeignKey(
        'usuarios.Grupo',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='autor_propietario_grupo'
    )

    notas = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.apellidos}, {self.nombre}"

    class Meta:
        verbose_name = "autor"
        verbose_name_plural = "autores"

class Fuente(models.Model):
    TIPO_CHOICES = [
        ('libro', 'Libro'),
        ('articulo', 'Artículo'),
        # futuros tipos…
    ]

    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    titulo = models.CharField(max_length=500)
    subtitulo = models.CharField(max_length=512, null=True, blank=True)
    autores = models.ManyToManyField(Autor, related_name='fuentes')
    fecha_publicacion = models.DateField(blank=True, null=True)

    creado = models.DateTimeField(auto_now_add=True)
    creado_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, related_name='fuentes_creadas', null=True, blank=True)
    modificado = models.DateTimeField(auto_now=True)
    modificado_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, related_name='fuentes_modificadas', null=True, blank=True)

    propietario_usuario = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='fuente_propietario_usuario'
    )
    propietario_grupo = models.ForeignKey(
        'usuarios.Grupo',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='fuente_propietario_grupo'
    )

    notas = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Fuente"
        verbose_name_plural = "Fuentes"

    def __str__(self):
        return self.titulo

class Libro(Fuente):
    editorial = models.ForeignKey(Editorial, on_delete=models.SET_NULL, null=True, blank=True, related_name='libros')
    isbn10 = models.CharField(max_length=10, blank=True, null=True)
    isbn13 = models.CharField(max_length=13, blank=True, null=True)
    numero_paginas = models.PositiveIntegerField(blank=True, null=True)
    edicion = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = "Libro"
        verbose_name_plural = "Libros"

    def save(self, *args, **kwargs):
        self.tipo = 'libro'
        super().save(*args, **kwargs)


class Revista(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    issn = models.CharField(max_length=20, null=True, blank=True)
    editorial = models.ForeignKey(Editorial, on_delete=models.SET_NULL, null=True, blank=True)
    sitio_web = models.URLField(null=True, blank=True)

    creado = models.DateTimeField(auto_now_add=True)
    creado_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, related_name='revistas_creadas', null=True,
                                   blank=True)
    modificado = models.DateTimeField(auto_now=True)
    modificado_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, related_name='revistas_modificadas',
                                       null=True, blank=True)

    class Meta:
        verbose_name = "Revista"
        verbose_name_plural = "Revistas"

    def __str__(self):
        return self.nombre

class Articulo(Fuente):
    revista = models.ForeignKey(Revista, on_delete=models.PROTECT, related_name='articulos')

    volumen = models.CharField(max_length=50, null=True, blank=True)
    numero = models.CharField(max_length=50, null=True, blank=True)
    paginas = models.CharField(max_length=50, null=True, blank=True)

    doi = models.CharField(max_length=100, null=True, blank=True)
    url = models.URLField(null=True, blank=True)

    class Meta:
        verbose_name = "Artículo"
        verbose_name_plural = "Artículos"

    def save(self, *args, **kwargs):
        self.tipo = 'articulo'
        super().save(*args, **kwargs)
