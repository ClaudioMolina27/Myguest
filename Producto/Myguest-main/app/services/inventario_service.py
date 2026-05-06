from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import or_

from app.models.inventario_model import Producto, Inventario
from app.schemas.inventario_schema import ProductoCreate, ProductoUpdate, InventarioUpdate, AlertaStock


async def get_productos(db: AsyncSession):
    result = await db.execute(select(Producto).order_by(Producto.nom_producto))
    return result.scalars().all()


async def get_producto_by_id(db: AsyncSession, id_producto: int):
    result = await db.execute(select(Producto).where(Producto.id_producto == id_producto))
    return result.scalars().first()


async def get_productos_by_nombre(db: AsyncSession, nombre: str):
    result = await db.execute(
        select(Producto).where(Producto.nom_producto.ilike(f"%{nombre}%"))
        .order_by(Producto.nom_producto)
    )
    return result.scalars().all()


async def create_producto(db: AsyncSession, datos: ProductoCreate):
    nuevo = Producto(
        nom_producto=datos.nom_producto,
        precio=datos.precio,
        cod_unidad_medida=datos.cod_unidad_medida,
        cod_categ_producto=datos.cod_categ_producto,
        cod_familia=datos.cod_familia,
    )
    db.add(nuevo)
    await db.commit()
    await db.refresh(nuevo)

    inventario = Inventario(id_producto=nuevo.id_producto, stock_actual=0, stock_minimo=0)
    db.add(inventario)
    await db.commit()

    return nuevo


async def update_producto(db: AsyncSession, id_producto: int, datos: ProductoUpdate):
    producto = await get_producto_by_id(db, id_producto)
    if not producto:
        return None
    for campo, valor in datos.model_dump(exclude_unset=True).items():
        setattr(producto, campo, valor)
    await db.commit()
    await db.refresh(producto)
    return producto


async def delete_producto(db: AsyncSession, id_producto: int):
    producto = await get_producto_by_id(db, id_producto)
    if not producto:
        return False
    
    result = await db.execute(
        select(Inventario).where(Inventario.id_producto == id_producto)
    )
    inventario = result.scalars().first()
    if inventario:
        await db.delete(inventario)
        await db.flush()

    await db.delete(producto)
    await db.commit()
    return True


async def get_inventario(db: AsyncSession):
    result = await db.execute(
        select(Inventario, Producto.nom_producto)
        .join(Producto, Inventario.id_producto == Producto.id_producto)
        .order_by(Producto.nom_producto)
    )
    rows = result.all()
    return [
        AlertaStock(
            id_producto=inv.id_producto,
            nom_producto=nom,
            stock_actual=float(inv.stock_actual),
            stock_minimo=float(inv.stock_minimo),
            diferencia=float(inv.stock_actual) - float(inv.stock_minimo)
        )
        for inv, nom in rows
    ]


async def get_inventario_by_producto(db: AsyncSession, id_producto: int):
    result = await db.execute(
        select(Inventario, Producto.nom_producto)
        .join(Producto, Inventario.id_producto == Producto.id_producto)
        .where(Inventario.id_producto == id_producto)
    )
    row = result.first()
    if not row:
        return None
    inv, nom = row
    return AlertaStock(
        id_producto=inv.id_producto,
        nom_producto=nom,
        stock_actual=float(inv.stock_actual),
        stock_minimo=float(inv.stock_minimo),
        diferencia=float(inv.stock_actual) - float(inv.stock_minimo)
    )


async def get_alertas_stock(db: AsyncSession):
    result = await db.execute(
        select(Inventario, Producto.nom_producto)
        .join(Producto, Inventario.id_producto == Producto.id_producto)
        .where(Inventario.stock_actual <= Inventario.stock_minimo)
        .order_by(Producto.nom_producto)
    )
    rows = result.all()
    return [
        AlertaStock(
            id_producto=inv.id_producto,
            nom_producto=nom,
            stock_actual=float(inv.stock_actual),
            stock_minimo=float(inv.stock_minimo),
            diferencia=float(inv.stock_actual) - float(inv.stock_minimo)
        )
        for inv, nom in rows
    ]


async def update_stock_minimo(db: AsyncSession, id_producto: int, datos: InventarioUpdate):
    result = await db.execute(
        select(Inventario).where(Inventario.id_producto == id_producto)
    )
    inventario = result.scalars().first()
    if not inventario:
        return None
    inventario.stock_minimo = datos.stock_minimo
    await db.commit()
    await db.refresh(inventario)
    return inventario