from django.contrib import admin
from .models import PlanMembresia, Oferta, MembresiaUsuario

class AuditoriaAdmin(admin.ModelAdmin):
    readonly_fields = ('creado', 'modificado', 'creado_por', 'modificado_por')

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.creado_por = request.user
        obj.modificado_por = request.user
        super().save_model(request, obj, form, change)

@admin.register(PlanMembresia)
class PlanMembresiaAdmin(AuditoriaAdmin):
    list_display = ('nombre', 'tipo', 'precio_eur', 'duracion_meses', 'activo')
    list_filter = ('tipo', 'activo')
    search_fields = ('nombre', 'descripcion')

    fieldsets = (
        ('Información general', {
            'fields': ('nombre', 'descripcion', 'tipo', 'precio_eur', 'duracion_meses', 'activo')
        }),
        ('Integración con Stripe', {
            'fields': ('stripe_product_id', 'stripe_price_id')
        }),
    )

@admin.register(Oferta)
class OfertaAdmin(AuditoriaAdmin):
    list_display = ('nombre', 'codigo', 'porcentaje_descuento', 'plan', 'fecha_inicio', 'fecha_fin', 'activa')
    list_filter = ('activa', 'plan')
    search_fields = ('nombre', 'codigo')

    fieldsets = (
        ('Detalles de la oferta', {
            'fields': ('nombre', 'codigo', 'porcentaje_descuento', 'plan', 'activa')
        }),
        ('Fechas y límites', {
            'fields': ('fecha_inicio', 'fecha_fin', 'limite_usos', 'usos_realizados')
        }),
    )

@admin.register(MembresiaUsuario)
class MembresiaUsuarioAdmin(AuditoriaAdmin):
    list_display = ('usuario', 'membresia', 'frecuencia', 'inicio', 'fin', 'auto_renovar', 'cancelada_en')
    list_filter = ('frecuencia', 'auto_renovar', 'cancelada_en')
    search_fields = ('usuario__email', 'usuario__nombre', 'usuario__apellidos', 'membresia__nombre')
