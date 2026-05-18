from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from datetime import datetime, timezone
from typing import Optional

from app.models.facturacion_model import Factura, DetFactura
from app.schemas.facturacion_schema import FacturaCreate, FacturaUpdate


async def get_facturas(db: AsyncSession, id_proveedor: int = None, estado: str = None):
    query = select(Factura).options(selectinload(Factura.detalles)).order_by(Factura.fecha_ingreso.desc())
    if id_proveedor:
        query = query.where(Factura.id_proveedor == id_proveedor)
    if estado:
        query = query.where(Factura.estado_conciliacion == estado)
    result = await db.execute(query)
    return result.scalars().all()


async def get_factura_by_id(db: AsyncSession, id_factura: int):
    result = await db.execute(
        select(Factura)
        .options(selectinload(Factura.detalles))
        .where(Factura.id_factura == id_factura)
    )
    return result.scalars().first()


async def create_factura(db: AsyncSession, datos: FacturaCreate):
    factura = Factura(
        num_documento=datos.num_documento,
        fecha_emision=datos.fecha_emision,
        fecha_ingreso=datetime.now(timezone.utc),
        id_proveedor=datos.id_proveedor,
        id_orden_compra=datos.id_orden_compra,
        id_usuario=datos.id_usuario,
        estado_conciliacion="pendiente",
        obs=datos.obs
    )
    db.add(factura)
    await db.flush()

    for det in datos.detalles:
        detalle = DetFactura(
            id_factura=factura.id_factura,
            id_producto=det.id_producto,
            cantidad=det.cantidad,
            precio_unitario=det.precio_unitario,
            fecha_vencimiento=det.fecha_vencimiento
        )
        db.add(detalle)

    await db.commit()
    await db.refresh(factura)

    result = await db.execute(
        select(Factura)
        .options(selectinload(Factura.detalles))
        .where(Factura.id_factura == factura.id_factura)
    )
    return result.scalars().first()


async def update_factura(db: AsyncSession, id_factura: int, datos: FacturaUpdate):
    factura = await get_factura_by_id(db, id_factura)
    if not factura:
        return None
    for campo, valor in datos.model_dump(exclude_unset=True).items():
        setattr(factura, campo, valor)
    await db.commit()
    await db.refresh(factura)
    return factura


async def delete_factura(db: AsyncSession, id_factura: int):
    factura = await get_factura_by_id(db, id_factura)
    if not factura:
        return False
    await db.delete(factura)
    await db.commit()
    return True