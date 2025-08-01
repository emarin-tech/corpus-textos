from django.urls import path
from .views import CustomLoginView
from . import views

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('registro/', views.RegistroView.as_view(), name='registro'),
]