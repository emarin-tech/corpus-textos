from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    model = Usuario
    list_display = ('correo_electronico', 'username', 'is_staff', 'is_active')
    search_fields = ('correo_electronico', 'username')
    ordering = ('correo_electronico',)

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('nombre',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('correo_electronico', 'nombre', 'password1', 'password2')}),
    )
