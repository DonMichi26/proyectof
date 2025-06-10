# Importamos las clases necesarias de Django
from django.core.management.base import BaseCommand  # Clase base para comandos personalizados
from django.db import connection  # Para manejar la conexión a la base de datos

class Command(BaseCommand):
    # Descripción del comando que aparecerá en la ayuda
    help = 'Prueba la conexión a la base de datos'

    def handle(self, *args, **options):
        try:
            # Creamos un cursor para ejecutar consultas SQL
            with connection.cursor() as cursor:
                # Consultamos la versión de MySQL
                cursor.execute("SELECT VERSION()")
                version = cursor.fetchone()  # Obtenemos el resultado
                # Mostramos mensaje de éxito con la versión
                self.stdout.write(self.style.SUCCESS(f'Conexión exitosa a MySQL. Versión: {version[0]}'))
                
                # Consultamos todas las tablas existentes en la base de datos
                cursor.execute("SHOW TABLES")
                tables = cursor.fetchall()  # Obtenemos todas las tablas
                self.stdout.write("\nTablas en la base de datos:")
                # Iteramos sobre cada tabla y la mostramos
                for table in tables:
                    self.stdout.write(f"- {table[0]}")
                    
        except Exception as e:
            # Si ocurre algún error, mostramos el mensaje de error
            self.stdout.write(self.style.ERROR(f'Error al conectar con la base de datos: {str(e)}'))