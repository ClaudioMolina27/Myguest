/* ============================================================
   SCRIPT 10 - CARGA DE DETALLE DE REGISTROS DE TALLERES (DML)
   Genera el detalle automáticamente desde regis_taller + config_taller
   ============================================================ */

BEGIN;

INSERT INTO det_regis_taller (
    fecha, ano_academ, cod_periodo_academ, sigla, seccion,
    id_taller, id_producto, cod_agrupador, precio, cantidad
)
SELECT
    rt.fecha,
    rt.ano_academ,
    rt.cod_periodo_academ,
    rt.sigla,
    rt.seccion,
    rt.id_taller,
    ct.id_producto,
    ct.cod_agrupador,
    p.precio,
    ct.cantidad
FROM regis_taller rt
JOIN config_taller ct ON ct.id_taller = rt.id_taller
JOIN producto p       ON ct.id_producto = p.id_producto;

COMMIT;
