from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.database import get_db
from app.dependencies import get_current_user
from app.schemas.proveedor_schema import (
    ProveedorCreate, ProveedorUpdate, ProveedorResponse,
    FamiliaCreate, FamiliaUpdate, FamiliaResponse
)
from app.services import proveedor_service

router = APIRouter()


# ── PROVEEDORES ──────────────────────────────────────────────────────────────

@router.get("/proveedores/", response_model=List[ProveedorResponse])
async def listar_proveedores(
    todos: bool = Query(False, description="Incluir proveedores desactivados"),
    db: AsyncSession = Depends(get_db),
    usuario=Depends(get_current_user)
):
    return await proveedor_service.get_proveedores(db, solo_activos=not todos)


@router.get("/proveedores/{id_proveedor}", response_model=ProveedorResponse)
async def obtener_proveedor(
    id_proveedor: int,
    db: AsyncSession = Depends(get_db),
    usuario=Depends(get_current_user)
):
    proveedor = await proveedor_service.get_proveedor_by_id(db, id_proveedor)
    if not proveedor:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    return proveedor


@router.post("/proveedores/", response_model=ProveedorResponse, status_code=status.HTTP_201_CREATED)
async def crear_proveedor(
    datos: ProveedorCreate,
    db: AsyncSession = Depends(get_db),
    usuario=Depends(get_current_user)
):
    return await proveedor_service.create_proveedor(db, datos)


@router.put("/proveedores/{id_proveedor}", response_model=ProveedorResponse)
async def actualizar_proveedor(
    id_proveedor: int,
    datos: ProveedorUpdate,
    db: AsyncSession = Depends(get_db),
    usuario=Depends(get_current_user)
):
    proveedor = await proveedor_service.update_proveedor(db, id_proveedor, datos)
    if not proveedor:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    return proveedor


@router.delete("/proveedores/{id_proveedor}", status_code=status.HTTP_204_NO_CONTENT)
async def desactivar_proveedor(
    id_proveedor: int,
    db: AsyncSession = Depends(get_db),
    usuario=Depends(get_current_user)
):
    desactivado = await proveedor_service.desactivar_proveedor(db, id_proveedor)
    if not desactivado:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")


# ── FAMILIAS ─────────────────────────────────────────────────────────────────

@router.get("/familias/", response_model=List[FamiliaResponse])
async def listar_familias(
    db: AsyncSession = Depends(get_db),
    usuario=Depends(get_current_user)
):
    return await proveedor_service.get_familias(db)


@router.get("/familias/{cod_familia}", response_model=FamiliaResponse)
async def obtener_familia(
    cod_familia: int,
    db: AsyncSession = Depends(get_db),
    usuario=Depends(get_current_user)
):
    familia = await proveedor_service.get_familia_by_id(db, cod_familia)
    if not familia:
        raise HTTPException(status_code=404, detail="Familia no encontrada")
    return familia


@router.post("/familias/", response_model=FamiliaResponse, status_code=status.HTTP_201_CREATED)
async def crear_familia(
    datos: FamiliaCreate,
    db: AsyncSession = Depends(get_db),
    usuario=Depends(get_current_user)
):
    return await proveedor_service.create_familia(db, datos)


@router.put("/familias/{cod_familia}", response_model=FamiliaResponse)
async def actualizar_familia(
    cod_familia: int,
    datos: FamiliaUpdate,
    db: AsyncSession = Depends(get_db),
    usuario=Depends(get_current_user)
):
    familia = await proveedor_service.update_familia(db, cod_familia, datos)
    if not familia:
        raise HTTPException(status_code=404, detail="Familia no encontrada")
    return familia


@router.delete("/familias/{cod_familia}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_familia(
    cod_familia: int,
    db: AsyncSession = Depends(get_db),
    usuario=Depends(get_current_user)
):
    eliminado = await proveedor_service.delete_familia(db, cod_familia)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Familia no encontrada")
    