"""
Vistas para el sistema de autenticación.
Este módulo contiene todas las vistas necesarias para manejar la autenticación
y los endpoints protegidos de la API.
"""

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import json
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import status
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.settings import api_settings
from django.contrib.auth.models import User
from django.db import connection
from .models import Usuario

# Configuración del archivo de usuarios
USUARIOS_JSON = os.path.join(os.path.dirname(__file__), 'usuarios.json')

def leer_usuarios():
    """
    Lee los usuarios almacenados en el archivo JSON.
    Si el archivo no existe, retorna una lista vacía.
    """
    if not os.path.exists(USUARIOS_JSON):
        return []
    with open(USUARIOS_JSON, 'r', encoding='utf-8') as f:
        return json.load(f)

def escribir_usuarios(usuarios):
    """
    Guarda la lista de usuarios en el archivo JSON.
    """
    with open(USUARIOS_JSON, 'w', encoding='utf-8') as f:
        json.dump(usuarios, f, indent=2)

# Create your views here.

class CookieJWTAuthentication(JWTAuthentication):
    """
    Autenticación personalizada que permite obtener el token JWT desde las cookies.
    Útil para aplicaciones web donde el frontend y backend están en dominios diferentes.
    """
    def get_header(self, request):
        header = super().get_header(request)
        if header is None:
            # Si no hay token en el header Authorization, buscar en las cookies
            access_token = request.COOKIES.get('access_token')
            if access_token:
                # Formatear como un header Authorization estándar
                return f"{api_settings.AUTH_HEADER_TYPES[0]} {access_token}".encode('utf-8')
        return header

    def get_raw_token(self, header):
        # Sobreescribir para manejar el token que viene de la cookie sin el prefijo 'Bearer '
        parts = header.split()
        if parts[0] == api_settings.AUTH_HEADER_TYPES[0].encode():
            return parts[1]
        return super().get_raw_token(header)

# Vista protegida que solo permite el acceso a usuarios autenticados con un token válido
class PruebaProtegida(APIView):
    """
    Endpoint protegido que requiere autenticación.
    Ejemplo de uso: GET /protegido/
    Requiere: Token JWT válido en las cookies
    Retorna: Mensaje de bienvenida con el nombre del usuario
    """
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    # Método GET que retorna un mensaje si el usuario tiene un token válido
    def get(self, request):
        """
        Maneja las peticiones GET a la ruta protegida.
        Verifica el token de autenticación en el header.
        """
        return Response({"mensaje": f"¡Acceso concedido al usuario {request.user.username} con token válido!"})

@method_decorator(csrf_exempt, name='dispatch')
class LoginJSON(APIView):
    """
    Endpoint para autenticación de usuarios.
    Ejemplo de uso: POST /login-json/
    Requiere: username y password en el body
    Retorna: Token JWT y redirección al dashboard si las credenciales son válidas
    """
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        data = request.data
        username = data.get('username')
        password = data.get('password')
        
        print(f"Intentando login con usuario: {username}")  # Debug log
        
        try:
            # Buscar usuario en la tabla personalizada
            usuario = Usuario.objects.get(username=username, password_hash=password)
            print(f"Usuario encontrado: {usuario.username}")  # Debug log
            
            # Crear o obtener usuario de Django
            user, created = User.objects.get_or_create(
                username=usuario.username,
                defaults={
                    'email': usuario.email,
                    'is_active': True
                }
            )
            
            # Generar tokens JWT
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            
            response = Response({
                'mensaje': 'Login exitoso',
                'access_token': access_token,
                'refresh_token': refresh_token,
                'redirect_url': '/api/v1/dashboard/',
                'user': {
                    'username': usuario.username,
                    'email': usuario.email
                }
            }, status=status.HTTP_200_OK)
            
            # Configurar cookies con tokens
            response.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                samesite='Lax',
                secure=not settings.DEBUG,
                max_age=600  # 10 minutos en segundos
            )
            
            response.set_cookie(
                key='refresh_token',
                value=refresh_token,
                httponly=True,
                samesite='Lax',
                secure=not settings.DEBUG,
                max_age=604800  # 7 días en segundos
            )
            
            return response
            
        except Usuario.DoesNotExist:
            print(f"Usuario no encontrado: {username}")  # Debug log
            return Response({
                'mensaje': 'Credenciales incorrectas',
                'detalles': 'Usuario o contraseña inválidos'
            }, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            print(f"Error durante el login: {str(e)}")  # Debug log
            return Response({
                'mensaje': 'Error en el servidor',
                'detalles': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@method_decorator(csrf_exempt, name='dispatch')
class RegistroJSON(APIView):
    """
    Endpoint para registro de nuevos usuarios.
    Ejemplo de uso: POST /registro-json/
    Requiere: username y password en el body
    Retorna: Mensaje de éxito o error
    """
    def post(self, request):
        """
        Maneja las peticiones POST para el registro.
        Crea un nuevo usuario si no existe.
        """
        data = request.data
        username = data.get('username')
        password = data.get('password')
        if not username or not password:
            return Response({'mensaje': 'Usuario y contraseña requeridos'}, status=status.HTTP_400_BAD_REQUEST)
        usuarios = leer_usuarios()
        if any(user['username'] == username for user in usuarios):
            return Response({'mensaje': 'El usuario ya existe'}, status=status.HTTP_400_BAD_REQUEST)
        usuarios.append({'username': username, 'password': password})
        escribir_usuarios(usuarios)
        return Response({'mensaje': 'Usuario registrado correctamente'}, status=status.HTTP_201_CREATED)

@method_decorator(csrf_exempt, name='dispatch')
class VerificarDB(APIView):
    """
    Endpoint para verificar la conexión a la base de datos.
    Ejemplo de uso: GET /verificar-db/
    Retorna: Información sobre la conexión y usuarios en la base de datos
    """
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        try:
            # Verificar la conexión a la base de datos
            with connection.cursor() as cursor:
                cursor.execute("SELECT VERSION()")
                db_version = cursor.fetchone()[0]

            # Obtener información de usuarios
            usuarios = User.objects.all()
            usuarios_info = []
            
            for user in usuarios:
                # Intentar autenticar al usuario para verificar su contraseña
                auth_result = authenticate(username=user.username, password='nekolu26')
                usuarios_info.append({
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'is_active': user.is_active,
                    'date_joined': user.date_joined.strftime('%Y-%m-%d %H:%M:%S'),
                    'password_hash': user.password[:50] + '...',  # Mostrar parte del hash
                    'auth_test': 'OK' if auth_result else 'FAIL'
                })

            return Response({
                'mensaje': 'Conexión exitosa a la base de datos',
                'db_version': db_version,
                'db_name': settings.DATABASES['default']['NAME'],
                'db_host': settings.DATABASES['default']['HOST'],
                'usuarios': usuarios_info,
                'total_usuarios': len(usuarios_info)
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'mensaje': 'Error al conectar con la base de datos',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@method_decorator(csrf_exempt, name='dispatch')
class Dashboard(APIView):
    """
    Endpoint para el dashboard del usuario.
    Ejemplo de uso: GET /dashboard/
    Requiere: Token JWT válido
    Retorna: Información del dashboard
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'mensaje': 'Bienvenido al dashboard',
            'usuario': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'is_staff': user.is_staff,
                'is_superuser': user.is_superuser,
                'last_login': user.last_login.strftime('%Y-%m-%d %H:%M:%S') if user.last_login else None,
                'date_joined': user.date_joined.strftime('%Y-%m-%d %H:%M:%S')
            },
            'estadisticas': {
                'total_usuarios': User.objects.count(),
                'usuarios_activos': User.objects.filter(is_active=True).count(),
                'usuarios_staff': User.objects.filter(is_staff=True).count()
            }
        }, status=status.HTTP_200_OK)
