from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from typing import Optional

from app.schemas.reporte_schema import (
    ReporteCompleto, ReporteStockItem, ReporteConsumoItem,
    ReporteFacturaItem, ReporteMermaDevolucionItem, ReporteCostoAsignaturaItem
)


async def get_reporte_completo(
    db: AsyncSession,
    ano_academ: Optional[int] = None,
    cod_periodo_academ: Optional[int] = None,
    sigla: Optional[str] = None
):
    stock = await _get_stock(db)
    consumo = await _get_consumo(db, ano_academ, cod_periodo_academ, sigla)
    facturas = await _get_facturas(db, ano_academ)
    mermas_devoluciones = await _get_mermas_devoluciones(db, ano_academ)
    costos = await _get_costos_asignatura(db, ano_academ, cod_periodo_academ)

    return ReporteCompleto(
        ano_academ=ano_academ,
        cod_periodo_academ=cod_periodo_academ,
        sigla=sigla,
        stock=stock,
        consumo=consumo,
        facturas=facturas,
        mermas_devoluciones=mermas_devoluciones,
        costos_asignatura=costos
    )


async def _get_stock(db: AsyncSession):
    query = text("""
        SELECT
            p.id_producto,
            p.nom_producto,
            cp.nom_categ_producto,
            um.nom_unidad_medida_abrev as nom_unidad_medida,
            CAST(i.stock_actual AS FLOAT) as stock_actual,
            CAST(i.stock_minimo AS FLOAT) as stock_minimo,
            CAST(i.stock_actual - i.stock_minimo AS FLOAT) as diferencia,
            CASE
                WHEN i.stock_actual <= 0 THEN 'Sin stock'
                WHEN i.stock_actual <= i.stock_minimo THEN 'Stock crítico'
                WHEN i.stock_actual <= i.stock_minimo * 1.2 THEN 'Stock bajo'
                ELSE 'Normal'
            END as estado
        FROM inventario i
        JOIN producto p ON i.id_producto = p.id_producto
        JOIN categ_producto cp ON p.cod_categ_producto = cp.cod_categ_producto
        JOIN unidad_medida um ON p.cod_unidad_medida = um.cod_unidad_medida
        ORDER BY estado, p.nom_producto
    """)
    result = await db.execute(query)
    rows = result.fetchall()
    return [ReporteStockItem(**dict(row._mapping)) for row in rows]


async def _get_consumo(db: AsyncSession, ano_academ=None, cod_periodo_academ=None, sigla=None):
    filtros = []
    params = {}
    if ano_academ:
        filtros.append("drt.ano_academ = :ano_academ")
        params["ano_academ"] = ano_academ
    if cod_periodo_academ:
        filtros.append("drt.cod_periodo_academ = :cod_periodo_academ")
        params["cod_periodo_academ"] = cod_periodo_academ
    if sigla:
        filtros.append("drt.sigla = :sigla")
        params["sigla"] = sigla

    where = "WHERE " + " AND ".join(filtros) if filtros else ""

    query = text(f"""
        SELECT
            drt.sigla,
            a.nom_asign,
            drt.id_taller,
            t.titulo_preparacion,
            drt.fecha,
            p.nom_producto,
            CAST(drt.cantidad AS FLOAT) as cantidad,
            drt.precio as precio_unitario,
            CAST(drt.cantidad * drt.precio AS FLOAT) as costo_total
        FROM det_regis_taller drt
        JOIN asign a ON drt.sigla = a.sigla
        JOIN taller t ON drt.id_taller = t.id_taller
        JOIN producto p ON drt.id_producto = p.id_producto
        {where}
        ORDER BY drt.fecha DESC, drt.sigla
    """)
    result = await db.execute(query, params)
    rows = result.fetchall()
    return [ReporteConsumoItem(**dict(row._mapping)) for row in rows]


async def _get_facturas(db: AsyncSession, ano_academ=None):
    where = "WHERE EXTRACT(YEAR FROM f.fecha_emision) = :ano" if ano_academ else ""
    params = {"ano": ano_academ} if ano_academ else {}

    query = text(f"""
        SELECT
            f.id_factura,
            f.num_documento,
            f.fecha_emision,
            pr.nom_proveedor,
            f.estado_conciliacion,
            COUNT(df.id_producto) as total_productos,
            CAST(COALESCE(SUM(df.cantidad * df.precio_unitario), 0) AS FLOAT) as monto_total
        FROM factura f
        JOIN proveedor pr ON f.id_proveedor = pr.id_proveedor
        LEFT JOIN det_factura df ON f.id_factura = df.id_factura
        {where}
        GROUP BY f.id_factura, f.num_documento, f.fecha_emision, pr.nom_proveedor, f.estado_conciliacion
        ORDER BY f.fecha_emision DESC
    """)
    result = await db.execute(query, params)
    rows = result.fetchall()
    return [ReporteFacturaItem(**dict(row._mapping)) for row in rows]


async def _get_mermas_devoluciones(db: AsyncSession, ano_academ=None):
    ano_filter_m = "WHERE EXTRACT(YEAR FROM m.fecha) = :ano" if ano_academ else ""
    ano_filter_d = "WHERE EXTRACT(YEAR FROM d.fecha) = :ano" if ano_academ else ""
    params = {"ano": ano_academ} if ano_academ else {}

    query = text(f"""
        SELECT
            'Merma' as tipo,
            m.fecha,
            p.nom_producto,
            CAST(m.cantidad AS FLOAT) as cantidad,
            mm.nom_motivo_merma as motivo,
            u.nom || ' ' || u.primer_apellido as nom_usuario
        FROM merma m
        JOIN producto p ON m.id_producto = p.id_producto
        JOIN motivo_merma mm ON m.cod_motivo_merma = mm.cod_motivo_merma
        JOIN usuario u ON m.id_usuario = u.id_usuario
        {ano_filter_m}
        UNION ALL
        SELECT
            'Devolucion' as tipo,
            d.fecha,
            p.nom_producto,
            CAST(dd.cantidad AS FLOAT) as cantidad,
            d.motivo_sobrante as motivo,
            u.nom || ' ' || u.primer_apellido as nom_usuario
        FROM devolucion d
        JOIN det_devolucion dd ON d.id_devolucion = dd.id_devolucion
        JOIN producto p ON dd.id_producto = p.id_producto
        JOIN usuario u ON d.id_usuario = u.id_usuario
        {ano_filter_d}
        ORDER BY fecha DESC
    """)
    result = await db.execute(query, params)
    rows = result.fetchall()
    return [ReporteMermaDevolucionItem(**dict(row._mapping)) for row in rows]


async def _get_costos_asignatura(db: AsyncSession, ano_academ=None, cod_periodo_academ=None):
    filtros = []
    params = {}
    if ano_academ:
        filtros.append("drt.ano_academ = :ano_academ")
        params["ano_academ"] = ano_academ
    if cod_periodo_academ:
        filtros.append("drt.cod_periodo_academ = :cod_periodo_academ")
        params["cod_periodo_academ"] = cod_periodo_academ

    where = "WHERE " + " AND ".join(filtros) if filtros else ""

    query = text(f"""
        SELECT
            drt.sigla,
            a.nom_asign,
            COUNT(DISTINCT drt.id_taller) as num_talleres,
            CAST(SUM(drt.cantidad * drt.precio) AS FLOAT) as costo_total,
            CAST(SUM(drt.cantidad * drt.precio) / NULLIF(COUNT(DISTINCT drt.id_taller), 0) AS FLOAT) as costo_promedio_taller
        FROM det_regis_taller drt
        JOIN asign a ON drt.sigla = a.sigla
        {where}
        GROUP BY drt.sigla, a.nom_asign
        ORDER BY costo_total DESC
    """)
    result = await db.execute(query, params)
    rows = result.fetchall()
    return [ReporteCostoAsignaturaItem(**dict(row._mapping)) for row in rows]