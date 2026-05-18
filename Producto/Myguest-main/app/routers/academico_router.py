from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.database import get_db
from app.dependencies import get_current_user
from app.schemas.academico_schema import (
    CarreraResponse, AsignaturaResponse, TallerResponse, PeriodoAcademResponse,
    ProgAsignCreate, ProgAsignResponse,
    ProgTallerCreate, ProgTallerResponse,
    RegisTallerCreate, RegisTallerResponse
)
from app.services import academico_service

router = APIRouter()


# ── CONSULTAS MAESTRAS ───────────────────────────────────────────────────────

@router.get("/carreras/", response_model=List[CarreraResponse])
async def listar_carreras(
    db: AsyncSession = Depends(get_db),
    usuario=Depends(get_current_user)
):
    return await academico_service.get_carreras(db)


@router.get("/asignaturas/", response_model=List[AsignaturaResponse])
async def listar_asignaturas(
    cod_carrera: Optional[int] = Query(None, description="Filtrar por carrera"),
    db: AsyncSession = Depends(get_db),
    usuario=Depends(get_current_user)
):
    return await academico_service.get_asignaturas(db, cod_carrera)


@router.get("/talleres/", response_model=List[TallerResponse])
async def listar_talleres_por_asignatura(
    sigla: str = Query(..., description="Sigla de la asignatura"),
    db: AsyncSession = Depends(get_db),
    usuario=Depends(get_current_user)
):
    return await academico_service.get_talleres_by_sigla(db, sigla)


@router.get("/periodos/", response_model=List[PeriodoAcademResponse])
async def listar_periodos(
    db: AsyncSession = Depends(get_db),
    usuario=Depends(get_current_user)
):
    return await academico_service.get_periodos(db)


# ── PROGRAMACIÓN DE ASIGNATURAS ──────────────────────────────────────────────

@router.get("/prog-asign/", response_model=List[ProgAsignResponse])
async def listar_prog_asign(
    ano_academ: Optional[int] = Query(None),
    cod_periodo_academ: Optional[int] = Query(None),
    db: AsyncSession = Depends(get_db),
    usuario=Depends(get_current_user)
):
    return await academico_service.get_prog_asign(db, ano_academ, cod_periodo_academ)


@router.post("/prog-asign/", response_model=ProgAsignResponse, status_code=status.HTTP_201_CREATED)
async def crear_prog_asign(
    datos: ProgAsignCreate,
    db: AsyncSession = Depends(get_db),
    usuario=Depends(get_current_user)
):
    return await academico_service.create_prog_asign(db, datos)


# ── PROGRAMACIÓN DE TALLERES ─────────────────────────────────────────────────

@router.get("/prog-taller/", response_model=List[ProgTallerResponse])
async def listar_prog_taller(
    ano_academ: Optional[int] = Query(None),
    cod_periodo_academ: Optional[int] = Query(None),
    sigla: Optional[str] = Query(None),
    seccion: Optional[int] = Query(None),
    db: AsyncSession = Depends(get_db),
    usuario=Depends(get_current_user)
):
    return await academico_service.get_prog_taller(db, ano_academ, cod_periodo_academ, sigla, seccion)


@router.post("/prog-taller/", response_model=ProgTallerResponse, status_code=status.HTTP_201_CREATED)
async def crear_prog_taller(
    datos: ProgTallerCreate,
    db: AsyncSession = Depends(get_db),
    usuario=Depends(get_current_user)
):
    return await academico_service.create_prog_taller(db, datos)


# ── REGISTRO DE EJECUCIÓN ────────────────────────────────────────────────────

@router.get("/regis-taller/", response_model=List[RegisTallerResponse])
async def listar_regis_taller(
    ano_academ: Optional[int] = Query(None),
    cod_periodo_academ: Optional[int] = Query(None),
    sigla: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
    usuario=Depends(get_current_user)
):
    return await academico_service.get_regis_taller(db, ano_academ, cod_periodo_academ, sigla)


@router.post("/regis-taller/", response_model=RegisTallerResponse, status_code=status.HTTP_201_CREATED)
async def registrar_ejecucion_taller(
    datos: RegisTallerCreate,
    db: AsyncSession = Depends(get_db),
    usuario=Depends(get_current_user)
):
    return await academico_service.create_regis_taller(db, datos)