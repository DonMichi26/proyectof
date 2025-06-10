"""
Configuración de URLs para la aplicación de autenticación.
"""
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import LoginView, TestProtectedView, HomeView

urlpatterns = [
    # Frontend
    path('', HomeView.as_view(), name='home'),
    
    # API
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('test/', TestProtectedView.as_view(), name='test-protected'),
]
