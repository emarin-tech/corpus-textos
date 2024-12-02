# publicaciones/models.py
from django.db import models


class Editorial(models.Model):
    nombre = models.CharField(max_length=255)
    direccion = models.TextField(blank=True)
    ciudad = models.CharField(max_length=255)
    region = models.CharField(max_length=255, blank=True)
    pais = models.CharField(max_length=255)
    pagina_web = models.URLField(blank=True)

    class Meta:
        verbose_name_plural = "Editoriales"


class SelloEditorial(models.Model):
    nombre = models.CharField(max_length=255)
    editorial_madre = models.ForeignKey(Editorial, on_delete=models.CASCADE, related_name='sellos')

    class Meta:
        verbose_name_plural = "Sellos Editoriales"


class Autor(models.Model):
    nombre = models.CharField(max_length=255)
    apellidos = models.CharField(max_length=255)
    web = models.URLField(blank=True)
    correo_electronico = models.EmailField(blank=True)
    biografia = models.TextField(blank=True)
    foto = models.ImageField(upload_to='autores/', blank=True)

    class Meta:
        verbose_name_plural = "Autores"


class Publicacion(models.Model):
    TIPOS_PUBLICACION = [
        ('articulo', 'Artículo'),
        ('libro', 'Libro'),
        # Añadir más tipos según necesidad
    ]

    # Campos base
    tipo = models.CharField(max_length=20, choices=TIPOS_PUBLICACION)
    titulo = models.CharField(max_length=255)
    subtitulo = models.CharField(max_length=255, blank=True)
    fecha_edicion = models.DateField()
    sello_editorial = models.ForeignKey(SelloEditorial, on_delete=models.PROTECT)

    # ISBN (podemos tener ambos)
    isbn_10 = models.CharField(max_length=10, blank=True)
    isbn_13 = models.CharField(max_length=13, blank=True)

    # Campos específicos para revistas/artículos
    numero_edicion = models.PositiveIntegerField(null=True, blank=True)
    titulo_revista = models.CharField(max_length=255, blank=True)
    issue = models.CharField(max_length=50, blank=True)
    volumen = models.CharField(max_length=50, blank=True)
    fecha_publicacion = models.DateField(null=True, blank=True)
    url = models.URLField(blank=True)

    # Relación con autores
    autores = models.ManyToManyField(Autor, through='AutorPublicacion')

    # Control de acceso
    propietario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='publicaciones')
    grupo = models.ForeignKey(Grupo, on_delete=models.SET_NULL, null=True, blank=True, related_name='publicaciones')

    class Meta:
        verbose_name_plural = "Publicaciones"


class AutorPublicacion(models.Model):
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE)
    publicacion = models.ForeignKey(Publicacion, on_delete=models.CASCADE)
    orden = models.PositiveIntegerField()  # Para mantener el orden de los autores

    class Meta:
        ordering = ['orden']