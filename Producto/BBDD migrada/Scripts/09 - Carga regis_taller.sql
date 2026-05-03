/* ============================================================
   SCRIPT 09 - CARGA DE REGISTROS DE TALLERES (DML)
   ============================================================ */

BEGIN;

INSERT INTO regis_taller (fecha, ano_academ, cod_periodo_academ, sigla, seccion, id_taller, id_usuario, obs) VALUES
('2023-03-06', 2023, 1, 'ABT3131', 3, 82, 3, 'Menta llegó en malas condiciones'),
('2023-03-14', 2023, 1, 'ABT3131', 3, 83, 3, 'Sin observaciones'),
('2023-03-23', 2023, 1, 'ABT3131', 3, 84, 5, 'Preferentemente limones deben ser pica que es lo más común'),
('2023-04-06', 2023, 1, 'ABT3131', 3, 86, 3, 'Vodka insuficiente'),
('2023-04-14', 2023, 1, 'ABT3131', 3, 87, 7, 'Sin observaciones'),
('2023-04-17', 2023, 1, 'ABT3131', 3, 88, 3, 'Sin observaciones');

COMMIT;
