"""
Archivo de configuración de URLs principal para el proyecto Django 'mi_proyecto'.
Define las rutas principales del proyecto y enlaza las URLs de las aplicaciones.
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # Ruta para acceder al panel de administración de Django
    path('admin/', admin.site.urls),

    # Ruta base para la API, incluye las URLs definidas en la app 'autenticacion'
    path('api/v1/', include('autenticacion.urls')),
]

#CORS_ALLOWED_ORIGINS = [
#    "https://tudominio.com",
#    "https://www.otrodominio.com",
#]
