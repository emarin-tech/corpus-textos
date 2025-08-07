# citas/admin.py

from django.contrib import admin
from .models import Cita, Etiqueta

class AuditoriaAdmin(admin.ModelAdmin):
    readonly_fields = ('creado', 'modificado', 'creado_por', 'modificado_por')

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.creado_por = request.user
            # Si no hay grupo ni usuario asignado como propietario, asumimos que es privado del creador
            if not obj.propietario_usuario and not obj.propietario_grupo:
                obj.propietario_usuario = request.user
        obj.modificado_por = request.user
        super().save_model(request, obj, form, change)

@admin.register(Cita)
class CitaAdmin(AuditoriaAdmin):
    list_display = ('id', 'fuente', 'pagina', 'propietario_usuario', 'propietario_grupo')
    search_fields = ('fuente__titulo', 'texto')
    list_filter = ('propietario_usuario', 'propietario_grupo')
    autocomplete_fields = ('fuente', 'etiquetas')
    fieldsets = (
        ('Datos de la cita', {
            'fields': ('fuente', 'pagina', 'texto', 'imagen', 'etiquetas')
        }),
        ('Propiedad', {
            'fields': ('propietario_usuario', 'propietario_grupo')
        }),
        ('Auditoría', {
            'fields': ('creado', 'creado_por', 'modificado', 'modificado_por')
        }),
    )

@admin.register(Etiqueta)
class EtiquetaAdmin(AuditoriaAdmin):
    list_display = ('nombre', 'slug', 'etiqueta_padre', 'propietario_usuario', 'propietario_grupo')
    search_fields = ('nombre', 'slug')
    list_filter = ('etiqueta_padre',)
    prepopulated_fields = {"slug": ("nombre",)}
    fieldsets = (
        ('Información general', {
            'fields': ('nombre', 'slug', 'etiqueta_padre', 'texto', 'imagen')
        }),
        ('Propiedad', {
            'fields': ('propietario_usuario', 'propietario_grupo')
        }),
        ('Auditoría', {
            'fields': ('creado', 'creado_por', 'modificado', 'modificado_por')
        }),
    )
