# Sistema de Gestión de Gastronomía

API REST con FastAPI + Supabase (PostgreSQL) para gestión de inventario y talleres.

## Requisitos
- Python 3.11+
- Cuenta en Supabase (supabase.com)

## Instalación

```bash
# 1. Clonar el repositorio
git clone <repo>
cd gastronomia_app

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales de Supabase

# 5. Correr el servidor
uvicorn app.main:app --reload
```

## Documentación
- Swagger UI: http://localhost:8000/docs
- Redoc:       http://localhost:8000/redoc

## Estructura
```
app/
├── main.py          # Entrada FastAPI, CORS, routers
├── config.py        # Variables de entorno (Pydantic Settings)
├── database.py      # Engine async, sesión SQLAlchemy, Base
├── dependencies.py  # JWT auth, inyección de dependencias
├── models/          # Modelos SQLAlchemy (tablas)
├── schemas/         # Schemas Pydantic (validación)
├── routers/         # Endpoints por entidad
├── services/        # Lógica de negocio
└── ia/              # Módulo Gemma 4 (fase posterior)
```
