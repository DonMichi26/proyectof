from django.db import models

# Create your models here.

class Usuario(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField()
    password_hash = models.CharField(max_length=128)
    created_at = models.DateTimeField()

    class Meta:
        db_table = 'users'  # El nombre correcto de la tabla en MySQL
        managed = False  # Django no gestionará esta tabla
