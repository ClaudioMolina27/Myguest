from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.database import get_db
from app.dependencies import get_current_user
from app.schemas.facturacion_schema import (
    FacturaCreate, FacturaUpdate, FacturaResponse
)
from app.services import facturacion_service

router = APIRouter()


@router.get("/facturas/", response_model=List[FacturaResponse])
async def listar_facturas(
    id_proveedor: Optional[int] = Query(None, description="Filtrar por proveedor"),
    estado: Optional[str] = Query(None, description="pendiente | conciliada | con_diferencia"),
    db: AsyncSession = Depends(get_db),
    usuario=Depends(get_current_user)
):
    return await facturacion_service.get_facturas(db, id_proveedor, estado)


@router.get("/facturas/{id_factura}", response_model=FacturaResponse)
async def obtener_factura(
    id_factura: int,
    db: AsyncSession = Depends(get_db),
    usuario=Depends(get_current_user)
):
    factura = await facturacion_service.get_factura_by_id(db, id_factura)
    if not factura:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    return factura


@router.post("/facturas/", response_model=FacturaResponse, status_code=status.HTTP_201_CREATED)
async def crear_factura(
    datos: FacturaCreate,
    db: AsyncSession = Depends(get_db),
    usuario=Depends(get_current_user)
):
    return await facturacion_service.create_factura(db, datos)


@router.put("/facturas/{id_factura}", response_model=FacturaResponse)
async def actualizar_factura(
    id_factura: int,
    datos: FacturaUpdate,
    db: AsyncSession = Depends(get_db),
    usuario=Depends(get_current_user)
):
    factura = await facturacion_service.update_factura(db, id_factura, datos)
    if not factura:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    return factura


@router.delete("/facturas/{id_factura}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_factura(
    id_factura: int,
    db: AsyncSession = Depends(get_db),
    usuario=Depends(get_current_user)
):
    eliminado = await facturacion_service.delete_factura(db, id_factura)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Factura no encontrada")