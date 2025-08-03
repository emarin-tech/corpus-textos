from django.db import models
from django.conf import settings
from usuarios.models import Usuario

class PlanMembresia(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    precio_eur = models.DecimalField(max_digits=6, decimal_places=2)
    duracion_meses = models.PositiveIntegerField(default=13)
    tipo = models.CharField(max_length=20, choices=[('usuario', 'Usuario'), ('grupo', 'Grupo')])
    stripe_product_id = models.CharField(max_length=255, blank=True, null=True)
    stripe_price_id = models.CharField(max_length=255, blank=True, null=True)
    activo = models.BooleanField(default=True)

    creado = models.DateTimeField(auto_now_add=True)
    creado_por = models.ForeignKey(
        'usuarios.Usuario',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='planes_creados'
    )
    modificado = models.DateTimeField(auto_now=True)
    modificado_por = models.ForeignKey(
        'usuarios.Usuario',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='planes_modificados'
    )

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "plan de membresía"
        verbose_name_plural = "planes de membresía"

class Oferta(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    codigo = models.CharField(max_length=50, unique=True)
    porcentaje_descuento = models.DecimalField(max_digits=5, decimal_places=2)  # hasta 100.00%
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    plan = models.ForeignKey(PlanMembresia, on_delete=models.CASCADE, related_name='ofertas')
    limite_usos = models.PositiveIntegerField(blank=True, null=True)
    usos_realizados = models.PositiveIntegerField(default=0)
    activa = models.BooleanField(default=True)

    creado = models.DateTimeField(auto_now_add=True)
    creado_por = models.ForeignKey(
        'usuarios.Usuario',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='ofertas_creadas'
    )
    modificado = models.DateTimeField(auto_now=True)
    modificado_por = models.ForeignKey(
        'usuarios.Usuario',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='ofertas_modificadas'
    )

    def __str__(self):
        return f'{self.nombre} ({self.porcentaje_descuento}%)'

    class Meta:
        verbose_name = "oferta"
        verbose_name_plural = "ofertas"

class MembresiaUsuario(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='membresias_usuario')
    membresia = models.ForeignKey(PlanMembresia, on_delete=models.CASCADE, related_name='usuarios_membresia')

    frecuencia = models.CharField(max_length=20, choices=[('mensual', 'Mensual'), ('anual', 'Anual')])
    inicio = models.DateField()
    fin = models.DateField()
    cancelada_en = models.DateField(blank=True, null=True)
    auto_renovar = models.BooleanField(default=True)

    creado = models.DateTimeField(auto_now_add=True)
    creado_por = models.ForeignKey(
        'usuarios.Usuario',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='membresias_usuario_creadas'
    )
    modificado = models.DateTimeField(auto_now=True)
    modificado_por = models.ForeignKey(
        'usuarios.Usuario',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='membresias_usuario_modificadas'
    )

    class Meta:
        verbose_name = 'membresía de usuario'
        verbose_name_plural = 'membresías de usuario'
        unique_together = ('usuario', 'membresia', 'inicio')

    def __str__(self):
        return f"{self.usuario} - {self.membresia} ({self.inicio} a {self.fin})"
