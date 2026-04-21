from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import get_settings
from app.database import engine, Base

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: crear tablas si no existen (solo dev)
    if settings.app_env == "development":
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown: cerrar conexiones
    await engine.dispose()


app = FastAPI(
    title=settings.app_name,
    description="API REST para gestión de inventario y talleres de gastronomía",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS — ajustar origins en produccion
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.app_env == "development" else ["https://tu-dominio.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers (se van agregando a medida que se crean) ──────────────────────────
# from app.routers import auth, carrera, perfil, producto, taller, inventario
# app.include_router(auth.router,      prefix="/auth",       tags=["Auth"])
# app.include_router(carrera.router,   prefix="/carreras",   tags=["Carreras"])
# app.include_router(perfil.router,    prefix="/perfiles",   tags=["Perfiles"])
# app.include_router(producto.router,  prefix="/productos",  tags=["Productos"])
# app.include_router(taller.router,    prefix="/talleres",   tags=["Talleres"])
# app.include_router(inventario.router,prefix="/inventario", tags=["Inventario"])


@app.get("/", tags=["Health"])
async def root():
    return {"status": "ok", "app": settings.app_name, "env": settings.app_env}


@app.get("/health", tags=["Health"])
async def health():
    return {"status": "ok"}
