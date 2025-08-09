from django.urls import path
from .views import login_view, registro, verificar_email
from . import views

app_name = "usuarios"

urlpatterns = [
    path("login/", login_view, name="login"),
    path("registro/", registro, name="registro"),
    path('verificar/<uidb64>/<token>/', verificar_email, name='verificar_email'),
    path('logout/', views.salir, name='logout'),
]
