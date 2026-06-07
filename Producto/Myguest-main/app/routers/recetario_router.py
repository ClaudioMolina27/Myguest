from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.database import get_db
from app.dependencies import get_current_user
from app.schemas.recetario_schema import (
    RecetaResumen, RecetaDetalle, RecetaDisponibilidad, RecetaEscalada
)
from app.services import recetario_service

router = APIRouter()


@router.get("/recetario/", response_model=List[RecetaResumen])
async def listar_recetas(
    sigla: Optional[str] = Query(None, description="Filtrar por sigla de asignatura"),
    db: AsyncSession = Depends(get_db),
    usuario=Depends(get_current_user)
):
    return await recetario_service.get_recetas(db, sigla)


@router.get("/recetario/{id_taller}", response_model=RecetaDetalle)
async def obtener_receta(
    id_taller: int,
    db: AsyncSession = Depends(get_db),
    usuario=Depends(get_current_user)
):
    receta = await recetario_service.get_receta_detalle(db, id_taller)
    if not receta:
        raise HTTPException(status_code=404, detail="Receta no encontrada")
    return receta


@router.get("/recetario/{id_taller}/disponibilidad", response_model=RecetaDisponibilidad)
async def verificar_disponibilidad(
    id_taller: int,
    alumnos: int = Query(1, description="Número de alumnos para calcular cantidades necesarias"),
    db: AsyncSession = Depends(get_db),
    usuario=Depends(get_current_user)
):
    resultado = await recetario_service.get_disponibilidad(db, id_taller, alumnos)
    if not resultado:
        raise HTTPException(status_code=404, detail="Receta no encontrada")
    return resultado


@router.get("/recetario/{id_taller}/escalado", response_model=RecetaEscalada)
async def escalar_receta(
    id_taller: int,
    alumnos: int = Query(..., description="Número de alumnos para escalar la receta"),
    db: AsyncSession = Depends(get_db),
    usuario=Depends(get_current_user)
):
    resultado = await recetario_service.get_receta_escalada(db, id_taller, alumnos)
    if not resultado:
        raise HTTPException(status_code=404, detail="Receta no encontrada")
    return resultado