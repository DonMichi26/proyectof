"""
Modelos para la aplicación de autenticación.
"""
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class UserLogin(models.Model):
    """
    Modelo para registrar los inicios de sesión de usuarios.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuario')
    login_time = models.DateTimeField(default=timezone.now, verbose_name='Hora de inicio de sesión')
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name='Dirección IP')
    user_agent = models.TextField(null=True, blank=True, verbose_name='Navegador/Dispositivo')

    class Meta:
        verbose_name = 'Inicio de sesión'
        verbose_name_plural = 'Inicios de sesión'
        ordering = ['-login_time']

    def __str__(self):
        return f"{self.user.username} - {self.login_time.strftime('%d/%m/%Y %H:%M:%S')}" 