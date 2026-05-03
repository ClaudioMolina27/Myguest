/* ============================================================
   QUERIES DE PRUEBA
   ============================================================ */

-- Cantidad de registros de docentes
SELECT COUNT(*) AS total_registros FROM regis_taller;

-- Cantidad de productos registrados
SELECT COUNT(*) AS total_det_registros FROM det_regis_taller;

-- Detalle de productos de un taller específico
SELECT
    p.nom_producto      AS producto,
    cp.nom_categ_producto AS categoria,
    ct.cantidad,
    um.nom_unidad_medida_abrev AS unidad,
    p.precio            AS precio_unit,
    ROUND(p.precio * ct.cantidad) AS sub_total,
    a.nom_agrupador     AS agrupador
FROM config_taller ct
JOIN producto        p  ON ct.id_producto        = p.id_producto
JOIN categ_producto  cp ON p.cod_categ_producto   = cp.cod_categ_producto
JOIN unidad_medida   um ON p.cod_unidad_medida    = um.cod_unidad_medida
JOIN agrupador       a  ON ct.cod_agrupador       = a.cod_agrupador
WHERE ct.id_taller = 151
ORDER BY a.nom_agrupador ASC, cp.nom_categ_producto ASC, p.nom_producto ASC;

-- Buscar talleres por asignatura
SELECT * FROM taller WHERE sigla = 'ABT3131' ORDER BY semana ASC;
