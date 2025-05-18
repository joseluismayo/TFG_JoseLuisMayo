from django.contrib import admin
from django.urls import path, include  # Importa 'include' para incluir las URLs de la app

urlpatterns = [
    path('', include('appdjango.urls')),  # Esto incluye las URLs de tu app
]
