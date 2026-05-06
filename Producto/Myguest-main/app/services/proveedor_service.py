from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.proveedor_model import Proveedor, FamiliaProducto
from app.schemas.proveedor_schema import ProveedorCreate, ProveedorUpdate, FamiliaCreate, FamiliaUpdate


# ── PROVEEDORES ──────────────────────────────────────────────────────────────

async def get_proveedores(db: AsyncSession, solo_activos: bool = True):
    query = select(Proveedor).order_by(Proveedor.nom_proveedor)
    if solo_activos:
        query = query.where(Proveedor.activo == True)
    result = await db.execute(query)
    return result.scalars().all()


async def get_proveedor_by_id(db: AsyncSession, id_proveedor: int):
    result = await db.execute(select(Proveedor).where(Proveedor.id_proveedor == id_proveedor))
    return result.scalars().first()


async def create_proveedor(db: AsyncSession, datos: ProveedorCreate):
    nuevo = Proveedor(
        nom_proveedor=datos.nom_proveedor,
        rut=datos.rut,
        contacto=datos.contacto,
        email=datos.email,
        telefono=datos.telefono,
        activo=True
    )
    db.add(nuevo)
    await db.commit()
    await db.refresh(nuevo)
    return nuevo


async def update_proveedor(db: AsyncSession, id_proveedor: int, datos: ProveedorUpdate):
    proveedor = await get_proveedor_by_id(db, id_proveedor)
    if not proveedor:
        return None
    for campo, valor in datos.model_dump(exclude_unset=True).items():
        setattr(proveedor, campo, valor)
    await db.commit()
    await db.refresh(proveedor)
    return proveedor


async def desactivar_proveedor(db: AsyncSession, id_proveedor: int):
    proveedor = await get_proveedor_by_id(db, id_proveedor)
    if not proveedor:
        return False
    proveedor.activo = False
    await db.commit()
    return True


# ── FAMILIAS ─────────────────────────────────────────────────────────────────

async def get_familias(db: AsyncSession):
    result = await db.execute(select(FamiliaProducto).order_by(FamiliaProducto.nom_familia))
    return result.scalars().all()


async def get_familia_by_id(db: AsyncSession, cod_familia: int):
    result = await db.execute(select(FamiliaProducto).where(FamiliaProducto.cod_familia == cod_familia))
    return result.scalars().first()


async def create_familia(db: AsyncSession, datos: FamiliaCreate):
    nueva = FamiliaProducto(
        cod_familia=datos.cod_familia,
        nom_familia=datos.nom_familia,
        id_proveedor=datos.id_proveedor
    )
    db.add(nueva)
    await db.commit()
    await db.refresh(nueva)
    return nueva


async def update_familia(db: AsyncSession, cod_familia: int, datos: FamiliaUpdate):
    familia = await get_familia_by_id(db, cod_familia)
    if not familia:
        return None
    for campo, valor in datos.model_dump(exclude_unset=True).items():
        setattr(familia, campo, valor)
    await db.commit()
    await db.refresh(familia)
    return familia


async def delete_familia(db: AsyncSession, cod_familia: int):
    familia = await get_familia_by_id(db, cod_familia)
    if not familia:
        return False
    await db.delete(familia)
    await db.commit()
    return True