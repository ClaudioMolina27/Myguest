from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import Optional

from app.models.compras_model import OrdenCompra, DetOrdenCompra
from app.schemas.compras_schema import OrdenCompraCreate, OrdenCompraUpdate


async def get_ordenes_compra(db: AsyncSession, id_proveedor: int = None, estado: str = None):
    query = select(OrdenCompra).options(selectinload(OrdenCompra.detalles)).order_by(OrdenCompra.fecha_emision.desc())
    if id_proveedor:
        query = query.where(OrdenCompra.id_proveedor == id_proveedor)
    if estado:
        query = query.where(OrdenCompra.estado == estado)
    result = await db.execute(query)
    return result.scalars().all()


async def get_orden_compra_by_id(db: AsyncSession, id_orden_compra: int):
    result = await db.execute(
        select(OrdenCompra)
        .options(selectinload(OrdenCompra.detalles))
        .where(OrdenCompra.id_orden_compra == id_orden_compra)
    )
    return result.scalars().first()


async def create_orden_compra(db: AsyncSession, datos: OrdenCompraCreate):
    orden = OrdenCompra(
        fecha_emision=datos.fecha_emision,
        fecha_entrega_est=datos.fecha_entrega_est,
        id_proveedor=datos.id_proveedor,
        id_usuario=datos.id_usuario,
        estado="borrador",
        obs=datos.obs
    )
    db.add(orden)
    await db.flush()

    for det in datos.detalles:
        detalle = DetOrdenCompra(
            id_orden_compra=orden.id_orden_compra,
            id_producto=det.id_producto,
            cantidad=det.cantidad,
            precio_unitario=det.precio_unitario
        )
        db.add(detalle)

    await db.commit()

    result = await db.execute(
        select(OrdenCompra)
        .options(selectinload(OrdenCompra.detalles))
        .where(OrdenCompra.id_orden_compra == orden.id_orden_compra)
    )
    return result.scalars().first()


async def update_orden_compra(db: AsyncSession, id_orden_compra: int, datos: OrdenCompraUpdate):
    orden = await get_orden_compra_by_id(db, id_orden_compra)
    if not orden:
        return None
    for campo, valor in datos.model_dump(exclude_unset=True).items():
        setattr(orden, campo, valor)
    await db.commit()
    await db.refresh(orden)
    return orden


async def delete_orden_compra(db: AsyncSession, id_orden_compra: int):
    orden = await get_orden_compra_by_id(db, id_orden_compra)
    if not orden:
        return False
    await db.delete(orden)
    await db.commit()
    return True