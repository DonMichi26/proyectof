# Backend Django con React

Este proyecto es un backend desarrollado con Django que proporciona una API REST para autenticación y gestión de usuarios, con un frontend en React.

## Estructura del Proyecto

```
backend/
├── backen/              # Directorio principal del proyecto Django
│   ├── autenticacion/   # Aplicación de autenticación
│   ├── mi_proyecto/     # Configuración del proyecto
│   └── manage.py        # Script de gestión de Django
├── frontend/           # Aplicación React
└── requirements.txt    # Dependencias de Python
```

## Requisitos

- Python 3.8+
- Node.js 14+
- MySQL 8.0+

## Instalación

1. Clonar el repositorio:
```bash
git clone <url-del-repositorio>
cd backend
```

2. Crear y activar entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar la base de datos:
- Crear una base de datos MySQL llamada 'backend'
- Configurar las credenciales en `mi_proyecto/settings.py`

5. Ejecutar migraciones:
```bash
python manage.py migrate
```

6. Crear superusuario:
```bash
python manage.py createsuperuser
```

## Ejecución

1. Iniciar el servidor Django:
```bash
python manage.py runserver
```

2. Iniciar el frontend React:
```bash
cd frontend
npm install
npm start
```

## Endpoints de la API

- `POST /api/v1/login/` - Login con JWT
- `POST /api/v1/refresh/` - Refrescar token JWT
- `POST /api/v1/login-json/` - Login personalizado
- `GET /api/v1/dashboard/` - Dashboard protegido

## Tecnologías Utilizadas

- Django 5.0.2
- Django REST Framework 3.14.0
- JWT Authentication
- React
- Material-UI
- MySQL



