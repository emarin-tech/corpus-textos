from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario
# from .models import Grupo, UsuarioGrupo
from django.db import connection
from django.db import OperationalError, ProgrammingError


class UsuarioAdmin(UserAdmin):
    model = Usuario
    list_display = ('correo_electronico', 'nombre', 'apellidos', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'acepta_boletin')
    fieldsets = UserAdmin.fieldsets + (
        ('Información adicional', {
            'fields': (
                'nombre', 'apellidos', 'titulo',
                'telefono', 'foto', 'google_id',
                'calle', 'ciudad', 'provincia', 'codigo_postal', 'pais',
                'acepta_politica_datos', 'acepta_correo_electronico',
                'acepta_correo_postal', 'acepta_boletin', 'acepta_publicacion_contenido',
                'acepta_condiciones_servicio'
            )
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('nombre', 'apellidos', 'correo_electronico')}),
    )
    ordering = ('correo_electronico',)
    search_fields = ('correo_electronico', 'nombre', 'apellidos')

    admin.site.register(Usuario)

