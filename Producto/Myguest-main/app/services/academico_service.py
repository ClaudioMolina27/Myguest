from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import date

from app.models.academico_model import (
    Carrera, Asignatura, Taller, PeriodoAcadem,
    ProgAsign, ProgTaller, RegisTaller, DetRegisTaller
)
from app.schemas.academico_schema import (
    ProgAsignCreate, ProgTallerCreate, RegisTallerCreate
)


# ── CONSULTAS MAESTRAS ───────────────────────────────────────────────────────

async def get_carreras(db: AsyncSession):
    result = await db.execute(select(Carrera).order_by(Carrera.nom_carrera))
    return result.scalars().all()


async def get_asignaturas(db: AsyncSession, cod_carrera: int = None):
    query = select(Asignatura).order_by(Asignatura.nom_asign)
    if cod_carrera:
        query = query.where(Asignatura.cod_carrera == cod_carrera)
    result = await db.execute(query)
    return result.scalars().all()


async def get_talleres_by_sigla(db: AsyncSession, sigla: str):
    result = await db.execute(
        select(Taller).where(Taller.sigla == sigla).order_by(Taller.semana)
    )
    return result.scalars().all()


async def get_periodos(db: AsyncSession):
    result = await db.execute(select(PeriodoAcadem).order_by(PeriodoAcadem.cod_periodo_academ))
    return result.scalars().all()


# ── PROGRAMACIÓN DE ASIGNATURAS ───────────────────────────────────────────────

async def get_prog_asign(db: AsyncSession, ano_academ: int = None, cod_periodo: int = None):
    query = select(ProgAsign)
    if ano_academ:
        query = query.where(ProgAsign.ano_academ == ano_academ)
    if cod_periodo:
        query = query.where(ProgAsign.cod_periodo_academ == cod_periodo)
    result = await db.execute(query)
    return result.scalars().all()


async def create_prog_asign(db: AsyncSession, datos: ProgAsignCreate):
    nueva = ProgAsign(
        ano_academ=datos.ano_academ,
        cod_periodo_academ=datos.cod_periodo_academ,
        sigla=datos.sigla,
        seccion=datos.seccion
    )
    db.add(nueva)
    await db.commit()
    await db.refresh(nueva)
    return nueva


# ── PROGRAMACIÓN DE TALLERES ─────────────────────────────────────────────────

async def get_prog_taller(db: AsyncSession, ano_academ: int = None,
                          cod_periodo: int = None, sigla: str = None,
                          seccion: int = None):
    query = select(ProgTaller)
    if ano_academ:
        query = query.where(ProgTaller.ano_academ == ano_academ)
    if cod_periodo:
        query = query.where(ProgTaller.cod_periodo_academ == cod_periodo)
    if sigla:
        query = query.where(ProgTaller.sigla == sigla)
    if seccion:
        query = query.where(ProgTaller.seccion == seccion)
    result = await db.execute(query)
    return result.scalars().all()


async def create_prog_taller(db: AsyncSession, datos: ProgTallerCreate):
    nuevo = ProgTaller(
        fecha=datos.fecha,
        ano_academ=datos.ano_academ,
        cod_periodo_academ=datos.cod_periodo_academ,
        sigla=datos.sigla,
        seccion=datos.seccion,
        id_taller=datos.id_taller,
        id_usuario=datos.id_usuario
    )
    db.add(nuevo)
    await db.commit()
    await db.refresh(nuevo)
    return nuevo


# ── REGISTRO DE EJECUCIÓN ────────────────────────────────────────────────────

async def get_regis_taller(db: AsyncSession, ano_academ: int = None,
                           cod_periodo: int = None, sigla: str = None):
    query = select(RegisTaller)
    if ano_academ:
        query = query.where(RegisTaller.ano_academ == ano_academ)
    if cod_periodo:
        query = query.where(RegisTaller.cod_periodo_academ == cod_periodo)
    if sigla:
        query = query.where(RegisTaller.sigla == sigla)
    result = await db.execute(query)
    return result.scalars().all()


async def create_regis_taller(db: AsyncSession, datos: RegisTallerCreate):
    # Crear el registro principal
    regis = RegisTaller(
        fecha=datos.fecha,
        ano_academ=datos.ano_academ,
        cod_periodo_academ=datos.cod_periodo_academ,
        sigla=datos.sigla,
        seccion=datos.seccion,
        id_taller=datos.id_taller,
        id_usuario=datos.id_usuario,
        obs=datos.obs
    )
    db.add(regis)
    await db.flush()

    # Crear el detalle — al insertar aquí el trigger de PG descuenta el stock
    for det in datos.detalles:
        detalle = DetRegisTaller(
            fecha=datos.fecha,
            ano_academ=datos.ano_academ,
            cod_periodo_academ=datos.cod_periodo_academ,
            sigla=datos.sigla,
            seccion=datos.seccion,
            id_producto=det.id_producto,
            id_taller=datos.id_taller,
            cod_agrupador=det.cod_agrupador,
            precio=det.precio,
            cantidad=det.cantidad
        )
        db.add(detalle)

    await db.commit()
    await db.refresh(regis)
    return regis