from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.database import get_db
from app.dependencies import get_current_user
from app.schemas.inventario_schema import (
    ProductoCreate, ProductoUpdate, ProductoResponse,
    InventarioUpdate, InventarioResponse, AlertaStock
)
from app.services import inventario_service

router = APIRouter()


# ── PRODUCTOS ────────────────────────────────────────────────────────────────

@router.get("/productos/", response_model=List[ProductoResponse])
async def listar_productos(
    nombre: Optional[str] = Query(None, description="Filtrar por nombre"),
    db: AsyncSession = Depends(get_db),
    usuario=Depends(get_current_user)
):
    if nombre:
        return await inventario_service.get_productos_by_nombre(db, nombre)
    return await inventario_service.get_productos(db)


@router.get("/productos/{id_producto}", response_model=ProductoResponse)
async def obtener_producto(
    id_producto: int,
    db: AsyncSession = Depends(get_db),
    usuario=Depends(get_current_user)
):
    producto = await inventario_service.get_producto_by_id(db, id_producto)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto


@router.post("/productos/", response_model=ProductoResponse, status_code=status.HTTP_201_CREATED)
async def crear_producto(
    datos: ProductoCreate,
    db: AsyncSession = Depends(get_db),
    usuario=Depends(get_current_user)
):
    return await inventario_service.create_producto(db, datos)


@router.put("/productos/{id_producto}", response_model=ProductoResponse)
async def actualizar_producto(
    id_producto: int,
    datos: ProductoUpdate,
    db: AsyncSession = Depends(get_db),
    usuario=Depends(get_current_user)
):
    producto = await inventario_service.update_producto(db, id_producto, datos)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto


@router.delete("/productos/{id_producto}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_producto(
    id_producto: int,
    db: AsyncSession = Depends(get_db),
    usuario=Depends(get_current_user)
):
    eliminado = await inventario_service.delete_producto(db, id_producto)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Producto no encontrado")


# ── INVENTARIO ───────────────────────────────────────────────────────────────

@router.get("/inventario/alertas", response_model=List[AlertaStock])
async def alertas_stock(
    db: AsyncSession = Depends(get_db),
    usuario=Depends(get_current_user)
):
    return await inventario_service.get_alertas_stock(db)


@router.get("/inventario/", response_model=List[AlertaStock])
async def listar_inventario(
    db: AsyncSession = Depends(get_db),
    usuario=Depends(get_current_user)
):
    return await inventario_service.get_inventario(db)


@router.get("/inventario/{id_producto}", response_model=AlertaStock)
async def obtener_stock(
    id_producto: int,
    db: AsyncSession = Depends(get_db),
    usuario=Depends(get_current_user)
):
    inv = await inventario_service.get_inventario_by_producto(db, id_producto)
    if not inv:
        raise HTTPException(status_code=404, detail="Producto no encontrado en inventario")
    return inv


@router.put("/inventario/{id_producto}", response_model=AlertaStock)
async def actualizar_stock_minimo(
    id_producto: int,
    datos: InventarioUpdate,
    db: AsyncSession = Depends(get_db),
    usuario=Depends(get_current_user)
):
    inv = await inventario_service.update_stock_minimo(db, id_producto, datos)
    if not inv:
        raise HTTPException(status_code=404, detail="Producto no encontrado en inventario")
    return await inventario_service.get_inventario_by_producto(db, id_producto)