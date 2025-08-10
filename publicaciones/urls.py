from django.urls import path
from . import views

app_name = "publicaciones"

urlpatterns = [
    path("autores/", views.autores_inicio, name="autores_inicio"),
    path('autores/nuevo/', views.crear_autor, name='crear_autor'),
    path('autores/ajax/', views.autores_ajax, name='autores_ajax'),
    path('autores/<int:pk>/editar/', views.editar_autor, name='editar_autor'),  # <-- ESTA ES CLAVE
]
