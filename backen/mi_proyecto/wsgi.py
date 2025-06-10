"""
Archivo de configuración WSGI para el proyecto Django 'mi_proyecto'.

Este archivo expone la aplicación WSGI como una variable llamada 'application'.
Es utilizado por servidores compatibles con WSGI (como Gunicorn o uWSGI) para servir tu proyecto en producción.
"""

import os
from django.core.wsgi import get_wsgi_application

# Establece la configuración por defecto de Django para el entorno WSGI
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mi_proyecto.settings')

# Crea la aplicación WSGI que será utilizada por el servidor web
application = get_wsgi_application()
