from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.database import get_db
from app.dependencies import get_current_user
from app.schemas.compras_schema import (
    OrdenCompraCreate, OrdenCompraUpdate, OrdenCompraResponse
)
from app.services import compras_service

router = APIRouter()


@router.get("/ordenes-compra/", response_model=List[OrdenCompraResponse])
async def listar_ordenes(
    id_proveedor: Optional[int] = Query(None, description="Filtrar por proveedor"),
    estado: Optional[str] = Query(None, description="borrador | enviada | recibida | anulada"),
    db: AsyncSession = Depends(get_db),
    usuario=Depends(get_current_user)
):
    return await compras_service.get_ordenes_compra(db, id_proveedor, estado)


@router.get("/ordenes-compra/{id_orden_compra}", response_model=OrdenCompraResponse)
async def obtener_orden(
    id_orden_compra: int,
    db: AsyncSession = Depends(get_db),
    usuario=Depends(get_current_user)
):
    orden = await compras_service.get_orden_compra_by_id(db, id_orden_compra)
    if not orden:
        raise HTTPException(status_code=404, detail="Orden de compra no encontrada")
    return orden


@router.post("/ordenes-compra/", response_model=OrdenCompraResponse, status_code=status.HTTP_201_CREATED)
async def crear_orden(
    datos: OrdenCompraCreate,
    db: AsyncSession = Depends(get_db),
    usuario=Depends(get_current_user)
):
    return await compras_service.create_orden_compra(db, datos)


@router.put("/ordenes-compra/{id_orden_compra}", response_model=OrdenCompraResponse)
async def actualizar_orden(
    id_orden_compra: int,
    datos: OrdenCompraUpdate,
    db: AsyncSession = Depends(get_db),
    usuario=Depends(get_current_user)
):
    orden = await compras_service.update_orden_compra(db, id_orden_compra, datos)
    if not orden:
        raise HTTPException(status_code=404, detail="Orden de compra no encontrada")
    return orden


@router.delete("/ordenes-compra/{id_orden_compra}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_orden(
    id_orden_compra: int,
    db: AsyncSession = Depends(get_db),
    usuario=Depends(get_current_user)
):
    eliminado = await compras_service.delete_orden_compra(db, id_orden_compra)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Orden de compra no encontrada")