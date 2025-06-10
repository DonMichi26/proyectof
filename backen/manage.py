#!/usr/bin/env python
"""
Archivo de utilidad para administrar tareas del proyecto Django.
Este archivo permite ejecutar comandos como iniciar el servidor, aplicar migraciones, crear usuarios, etc.
"""

# Importación de módulos necesarios
import os  # Para interactuar con variables de entorno y sistema operativo
import sys  # Para acceder a argumentos de línea de comandos

def main():
    """
    Punto de entrada principal para ejecutar comandos de Django.
    Esta función configura el entorno y ejecuta los comandos de Django.
    """
    # Configura el módulo de configuración de Django para este proyecto
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mi_proyecto.settings')
    
    try:
        # Importa la función que ejecutará los comandos de Django
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Manejo de error si Django no está instalado correctamente
        raise ImportError(
            "No se pudo importar Django. ¿Está instalado y disponible en tu entorno virtual?"
        ) from exc
    
    # Ejecuta el comando de Django con los argumentos proporcionados
    execute_from_command_line(sys.argv)

# Verifica si este archivo se está ejecutando directamente (no importado)
if __name__ == '__main__':
    main()
