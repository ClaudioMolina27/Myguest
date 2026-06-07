from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from typing import Optional

from app.models.academico_model import Taller
from app.models.inventario_model import Producto, Inventario
from app.schemas.recetario_schema import (
    RecetaResumen, RecetaDetalle, IngredienteReceta,
    RecetaDisponibilidad, IngredienteDisponibilidad,
    RecetaEscalada, IngredienteEscalado
)

# Importamos los modelos de config_taller y agrupador
from sqlalchemy import Table, Column, Integer, SmallInteger, Numeric, MetaData
from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from app.models.academico_model import Taller


class ConfigTaller(Base):
    __tablename__ = "config_taller"
    __table_args__ = {"extend_existing": True}

    id_producto: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_taller: Mapped[int] = mapped_column(Integer, primary_key=True)
    cod_agrupador: Mapped[int] = mapped_column(SmallInteger, primary_key=True)
    cantidad: Mapped[float] = mapped_column(Numeric(12, 6))


class Agrupador(Base):
    __tablename__ = "agrupador"
    __table_args__ = {"extend_existing": True}

    cod_agrupador: Mapped[int] = mapped_column(SmallInteger, primary_key=True)
    nom_agrupador: Mapped[str] = mapped_column()


async def get_recetas(db: AsyncSession, sigla: str = None):
    query = select(Taller).order_by(Taller.sigla, Taller.semana)
    if sigla:
        query = query.where(Taller.sigla == sigla)
    result = await db.execute(query)
    talleres = result.scalars().all()

    recetas = []
    for taller in talleres:
        ingredientes = await _get_ingredientes(db, taller.id_taller)
        costo = sum(i.costo_ingrediente for i in ingredientes)
        recetas.append(RecetaResumen(
            id_taller=taller.id_taller,
            titulo_preparacion=taller.titulo_preparacion,
            detalle_preparacion=taller.detalle_preparacion,
            semana=taller.semana,
            sigla=taller.sigla,
            jornada=taller.jornada,
            num_ingredientes=len(ingredientes),
            costo_estimado=costo
        ))
    return recetas


async def get_receta_detalle(db: AsyncSession, id_taller: int):
    result = await db.execute(select(Taller).where(Taller.id_taller == id_taller))
    taller = result.scalars().first()
    if not taller:
        return None

    ingredientes = await _get_ingredientes(db, id_taller)
    costo_total = sum(i.costo_ingrediente for i in ingredientes)
    porciones = max(1, len(ingredientes))

    return RecetaDetalle(
        id_taller=taller.id_taller,
        titulo_preparacion=taller.titulo_preparacion,
        detalle_preparacion=taller.detalle_preparacion,
        semana=taller.semana,
        sigla=taller.sigla,
        jornada=taller.jornada,
        ingredientes=ingredientes,
        costo_estimado=costo_total,
        costo_por_alumno=round(costo_total / porciones, 2)
    )


async def get_disponibilidad(db: AsyncSession, id_taller: int, alumnos: int = 1):
    result = await db.execute(select(Taller).where(Taller.id_taller == id_taller))
    taller = result.scalars().first()
    if not taller:
        return None

    ingredientes = await _get_ingredientes(db, id_taller)
    items = []
    ejecutable = True

    for ing in ingredientes:
        cantidad_necesaria = ing.cantidad * alumnos
        inv_result = await db.execute(
            select(Inventario).where(Inventario.id_producto == ing.id_producto)
        )
        inv = inv_result.scalars().first()
        stock_actual = float(inv.stock_actual) if inv else 0.0
        disponible = stock_actual >= cantidad_necesaria
        if not disponible:
            ejecutable = False

        items.append(IngredienteDisponibilidad(
            id_producto=ing.id_producto,
            nom_producto=ing.nom_producto,
            cantidad_necesaria=cantidad_necesaria,
            stock_actual=stock_actual,
            disponible=disponible,
            faltante=max(0, cantidad_necesaria - stock_actual)
        ))

    return RecetaDisponibilidad(
        id_taller=id_taller,
        titulo_preparacion=taller.titulo_preparacion,
        ejecutable=ejecutable,
        ingredientes=items
    )


async def get_receta_escalada(db: AsyncSession, id_taller: int, alumnos: int):
    result = await db.execute(select(Taller).where(Taller.id_taller == id_taller))
    taller = result.scalars().first()
    if not taller:
        return None

    ingredientes = await _get_ingredientes(db, id_taller)
    porciones_base = max(1, len(ingredientes))
    factor = alumnos / porciones_base

    items_escalados = []
    costo_total = 0.0

    for ing in ingredientes:
        cantidad_escalada = round(ing.cantidad * factor, 6)
        costo = round(cantidad_escalada * ing.precio_unitario, 2)
        costo_total += costo
        items_escalados.append(IngredienteEscalado(
            id_producto=ing.id_producto,
            nom_producto=ing.nom_producto,
            nom_agrupador=ing.nom_agrupador,
            cantidad_base=ing.cantidad,
            cantidad_escalada=cantidad_escalada,
            nom_unidad_medida=ing.nom_unidad_medida,
            costo_ingrediente=costo
        ))

    return RecetaEscalada(
        id_taller=id_taller,
        titulo_preparacion=taller.titulo_preparacion,
        alumnos=alumnos,
        porciones_base=porciones_base,
        ingredientes=items_escalados,
        costo_total=round(costo_total, 2),
        costo_por_alumno=round(costo_total / alumnos, 2) if alumnos > 0 else 0.0
    )


async def _get_ingredientes(db: AsyncSession, id_taller: int):
    from sqlalchemy import text
    query = text("""
        SELECT
            ct.id_producto,
            p.nom_producto,
            ct.cod_agrupador,
            a.nom_agrupador,
            CAST(ct.cantidad AS FLOAT) as cantidad,
            um.nom_unidad_medida_abrev as nom_unidad_medida,
            p.precio as precio_unitario,
            CAST(ct.cantidad AS FLOAT) * p.precio as costo_ingrediente
        FROM config_taller ct
        JOIN producto p ON ct.id_producto = p.id_producto
        JOIN agrupador a ON ct.cod_agrupador = a.cod_agrupador
        JOIN unidad_medida um ON p.cod_unidad_medida = um.cod_unidad_medida
        WHERE ct.id_taller = :id_taller
        ORDER BY a.nom_agrupador, p.nom_producto
    """)
    result = await db.execute(query, {"id_taller": id_taller})
    rows = result.fetchall()
    return [
        IngredienteReceta(
            id_producto=row.id_producto,
            nom_producto=row.nom_producto,
            cod_agrupador=row.cod_agrupador,
            nom_agrupador=row.nom_agrupador,
            cantidad=row.cantidad,
            nom_unidad_medida=row.nom_unidad_medida,
            precio_unitario=row.precio_unitario,
            costo_ingrediente=row.costo_ingrediente
        )
        for row in rows
    ]