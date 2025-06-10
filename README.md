# Proyecto de Autenticación JWT

Este proyecto implementa un sistema de autenticación usando Django REST Framework y JWT (JSON Web Tokens).

## Características

- Autenticación mediante JWT
- API REST con Django REST Framework
- Frontend para demostración
- Endpoints protegidos de ejemplo

## Requisitos

- Python 3.13+
- Django 5.2+
- Django REST Framework
- SimpleJWT
- Node.js (para el frontend)

## Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/DonMichi26/proyecto.git
cd proyecto
```

2. Instalar dependencias de Python:
```bash
pip install -r requirements.txt
```

3. Ejecutar migraciones:
```bash
python manage.py migrate
```

4. Crear superusuario:
```bash
python manage.py createsuperuser
```

5. Iniciar el servidor:
```bash
python manage.py runserver
```

## Uso

- Frontend: http://localhost:8000/
- Admin: http://localhost:8000/admin/
- API endpoints:
  - Login: `/api/login/`
  - Refresh Token: `/api/token/refresh/`
  - Test Protected: `/api/test/`
