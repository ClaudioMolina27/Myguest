/* Reporte 1: Valorización por taller */
SELECT 
    c.nom_carrera,
    a.sigla,
    a.nom_asign,
    t.semana,
    t.titulo_preparacion,
    ROUND(SUM(p.precio * ct.cantidad), 0) AS total_taller
FROM asign a
JOIN taller t ON t.sigla = a.sigla
JOIN config_taller ct ON t.id_taller = ct.id_taller
JOIN producto p ON ct.id_producto = p.id_producto
JOIN carrera c ON a.cod_carrera = c.cod_carrera
WHERE c.cod_carrera = 1
GROUP BY c.nom_carrera, a.sigla, a.nom_asign, t.semana, t.titulo_preparacion
ORDER BY c.nom_carrera ASC, a.sigla ASC, t.semana ASC;

/* Reporte 5: Detalle de productos por taller y por rango de fechas */
SELECT 
    c.nom_carrera,
    cp.nom_categ_producto,
    p.nom_producto,
    ct.cantidad,
    um.nom_unidad_medida,
    p.precio,
    (ct.cantidad * p.precio) AS precio_total,
    pt.fecha,
    pa.nom_periodo_academ,
    pt.sigla,
    a.nom_asign,
    pt.seccion,
    t.semana,
    t.titulo_preparacion
FROM prog_taller pt
JOIN asign a ON pt.sigla = a.sigla
JOIN config_taller ct ON pt.id_taller = ct.id_taller
JOIN taller t ON pt.id_taller = t.id_taller
JOIN producto p ON ct.id_producto = p.id_producto
JOIN unidad_medida um ON p.cod_unidad_medida = um.cod_unidad_medida
JOIN categ_producto cp ON p.cod_categ_producto = cp.cod_categ_producto
JOIN carrera c ON a.cod_carrera = c.cod_carrera
JOIN periodo_academ pa ON pt.cod_periodo_academ = pa.cod_periodo_academ
ORDER BY c.nom_carrera ASC, cp.nom_categ_producto ASC, p.nom_producto ASC;