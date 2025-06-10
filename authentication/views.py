from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework import status
from django.views.generic import TemplateView
import logging

logger = logging.getLogger(__name__)

class LoginView(APIView):
    """
    Vista para autenticar usuarios y generar tokens JWT.
    
    Métodos:
        POST: Autentica al usuario y devuelve tokens JWT
        
    Parámetros:
        - username: Nombre de usuario
        - password: Contraseña del usuario
        
    Respuestas:
        - 200: Autenticación exitosa con tokens
        - 400: Datos inválidos
        - 401: Credenciales inválidas
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        try:
            username = request.data.get('username')
            password = request.data.get('password')
            
            if not username or not password:
                return Response(
                    {'error': 'Se requieren username y password'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            user = authenticate(username=username, password=password)
            
            if not user:
                logger.warning(f'Intento de inicio de sesión fallido: {username}')
                return Response(
                    {'error': 'Credenciales inválidas'}, 
                    status=status.HTTP_401_UNAUTHORIZED
                )
                
            if not user.is_active:
                return Response(
                    {'error': 'Usuario inactivo'}, 
                    status=status.HTTP_401_UNAUTHORIZED
                )
                
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email
                }
            })
                
        except Exception as e:
            logger.error(f'Error en LoginView: {str(e)}')
            return Response(
                {'error': 'Error interno del servidor'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class TestProtectedView(APIView):
    """
    Vista de ejemplo protegida que requiere autenticación.
    
    Métodos:
        GET: Devuelve información del usuario autenticado
        
    Respuestas:
        - 200: Información del usuario
        - 401: No autenticado
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            return Response({
                'message': 'Autenticación exitosa',
                'user': {
                    'id': request.user.id,
                    'username': request.user.username,
                    'email': request.user.email
                }
            })
        except Exception as e:
            logger.error(f'Error en TestProtectedView: {str(e)}')
            return Response(
                {'error': 'Error interno del servidor'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class HomeView(TemplateView):
    """
    Vista para mostrar la página principal.
    
    Atributos:
        template_name: Ruta al template HTML
    """
    template_name = 'authentication/home.html'
