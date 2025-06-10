"""
Configuración de URLs para el proyecto core.
"""

from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

def redirect_to_home(request):
    return redirect('home')

urlpatterns = [
    path('', redirect_to_home),  # Redirige la raíz a la página principal
    path('admin/', admin.site.urls),
    path('api/', include('authentication.urls')),  # Incluye las URLs de autenticación
    # Aquí se agregarán las URLs de las aplicaciones
] 