from django.contrib import admin
from .models import GrupoEditorial, Editorial, Autor, Fuente, Libro, Revista, Articulo


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

@admin.register(GrupoEditorial)
class GrupoEditorialAdmin(AuditoriaAdmin):
    list_display = ('nombre', 'ciudad', 'pais', 'sitio_web', 'creado', 'creado_por')
    search_fields = ('nombre', 'ciudad', 'pais')
    list_filter = ('pais',)

@admin.register(Editorial)
class EditorialAdmin(AuditoriaAdmin):
    list_display = ('nombre', 'grupo_editorial', 'creado', 'creado_por')
    search_fields = ('nombre', 'grupo_editorial__nombre')
    list_filter = ('grupo_editorial',)

@admin.register(Autor)
class AutorAdmin(AuditoriaAdmin):
    list_display = ('nombre', 'apellidos', 'creado', 'creado_por', 'modificado', 'modificado_por')
    search_fields = ('nombre', 'apellidos')

@admin.register(Fuente)
class FuenteAdmin(AuditoriaAdmin):
    list_display = ('titulo', 'tipo', 'fecha_publicacion', 'creado_por')
    search_fields = ('titulo', 'subtitulo')
    list_filter = ('tipo',)


@admin.register(Libro)
class LibroAdmin(AuditoriaAdmin):
    list_display = ('titulo', 'editorial', 'isbn13', 'numero_paginas')
    search_fields = ('titulo', 'isbn10', 'isbn13')
    list_filter = ('editorial',)


@admin.register(Revista)
class RevistaAdmin(AuditoriaAdmin):
    list_display = ('nombre', 'issn', 'editorial', 'sitio_web', 'creado_por')
    search_fields = ('nombre', 'issn')


@admin.register(Articulo)
class ArticuloAdmin(AuditoriaAdmin):
    list_display = ('titulo', 'revista', 'volumen', 'numero', 'doi')
    search_fields = ('titulo', 'doi')
    list_filter = ('revista',)
