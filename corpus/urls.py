from django.urls import path
from . import views
from .views import dashboard

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path("dashboard/", dashboard, name="dashboard"),
]
