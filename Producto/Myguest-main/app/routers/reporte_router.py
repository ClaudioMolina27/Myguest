from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.database import get_db
from app.dependencies import get_current_user
from app.schemas.reporte_schema import ReporteCompleto
from app.services import reporte_service

router = APIRouter()


@router.get("/reportes/", response_model=ReporteCompleto)
async def generar_reporte(
    ano_academ: Optional[int] = Query(None, description="Año académico ej: 2026"),
    cod_periodo_academ: Optional[int] = Query(None, description="Período: 1=primer semestre, 2=segundo semestre"),
    sigla: Optional[str] = Query(None, description="Filtrar por sigla de asignatura ej: ABT3131"),
    db: AsyncSession = Depends(get_db),
    usuario=Depends(get_current_user)
):
    return await reporte_service.get_reporte_completo(db, ano_academ, cod_periodo_academ, sigla)