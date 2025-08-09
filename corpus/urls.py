from django.urls import path
from . import views

app_name = "corpus"

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path("escritorio/", views.escritorio, name="escritorio"),
]
