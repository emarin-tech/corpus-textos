from django.apps import AppConfig
from django.db.utils import ProgrammingError, OperationalError

class UsuariosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'usuarios'

    def ready(self):
        from django.contrib import admin
        from django.contrib.auth.admin import UserAdmin
        from django.db import connection
        from .models import Usuario

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT to_regclass('usuarios_usuario');")
                table_exists = cursor.fetchone()[0] is not None

            if table_exists:
                @admin.register(Usuario)
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

        except (ProgrammingError, OperationalError):
            pass
