/* ============================================================
   SCRIPT 02 - CARGA DE TABLAS DE PARÁMETROS (DML)
   ============================================================ */

BEGIN;

-- param
INSERT INTO param (cod_param, nom_param, valor) VALUES (1, 'Año académico vigente', '2024');

-- agrupador
INSERT INTO agrupador (cod_agrupador, nom_agrupador) VALUES (1, 'Taller');
INSERT INTO agrupador (cod_agrupador, nom_agrupador) VALUES (2, 'Almuerzo personal de servicio');

-- periodo_academ
INSERT INTO periodo_academ (cod_periodo_academ, nom_periodo_academ, nom_periodo_academ_abrev) VALUES (1, 'Primer semestre', '1SEM');
INSERT INTO periodo_academ (cod_periodo_academ, nom_periodo_academ, nom_periodo_academ_abrev) VALUES (2, 'Segundo semestre', '2SEM');
INSERT INTO periodo_academ (cod_periodo_academ, nom_periodo_academ, nom_periodo_academ_abrev) VALUES (3, 'Temporada académica de verano', 'TAV');

-- carrera
INSERT INTO carrera (cod_carrera, nom_carrera, nom_carrera_abrev) VALUES (0, '(Sin carrera)', '(SIN-CARR)');
INSERT INTO carrera (cod_carrera, nom_carrera, nom_carrera_abrev) VALUES (1, 'Gastronomía', 'GASTRO');
INSERT INTO carrera (cod_carrera, nom_carrera, nom_carrera_abrev) VALUES (2, 'Administración Hotelera', 'HOTEL');

-- categ_producto
INSERT INTO categ_producto (cod_categ_producto, nom_categ_producto) VALUES (0, '(Sin categoría)');
INSERT INTO categ_producto (cod_categ_producto, nom_categ_producto) VALUES (1, 'Frutas y verduras');
INSERT INTO categ_producto (cod_categ_producto, nom_categ_producto) VALUES (2, 'Carnes, cecinas y embutidos');
INSERT INTO categ_producto (cod_categ_producto, nom_categ_producto) VALUES (3, 'Mariscos y pescados');
INSERT INTO categ_producto (cod_categ_producto, nom_categ_producto) VALUES (4, 'Congelados');
INSERT INTO categ_producto (cod_categ_producto, nom_categ_producto) VALUES (5, 'Ovo lácteos');
INSERT INTO categ_producto (cod_categ_producto, nom_categ_producto) VALUES (6, 'Abarrotes');
INSERT INTO categ_producto (cod_categ_producto, nom_categ_producto) VALUES (7, 'Vinos, licores y bebidas');
INSERT INTO categ_producto (cod_categ_producto, nom_categ_producto) VALUES (8, 'No alimenticios');
INSERT INTO categ_producto (cod_categ_producto, nom_categ_producto) VALUES (9, 'Artículos de aseo');
INSERT INTO categ_producto (cod_categ_producto, nom_categ_producto) VALUES (10, 'Equipos y otros');

-- unidad_medida (bases primero, luego derivadas)
INSERT INTO unidad_medida (cod_unidad_medida, nom_unidad_medida, nom_unidad_medida_abrev, cod_unidad_medida_base, factor) VALUES (1, 'kilogramos', 'Kg.', NULL, NULL);
INSERT INTO unidad_medida (cod_unidad_medida, nom_unidad_medida, nom_unidad_medida_abrev, cod_unidad_medida_base, factor) VALUES (3, 'litros', 'lt.', NULL, NULL);
INSERT INTO unidad_medida (cod_unidad_medida, nom_unidad_medida, nom_unidad_medida_abrev, cod_unidad_medida_base, factor) VALUES (5, 'unidades', 'unid', NULL, NULL);
INSERT INTO unidad_medida (cod_unidad_medida, nom_unidad_medida, nom_unidad_medida_abrev, cod_unidad_medida_base, factor) VALUES (6, 'metros', 'mt.', NULL, NULL);
INSERT INTO unidad_medida (cod_unidad_medida, nom_unidad_medida, nom_unidad_medida_abrev, cod_unidad_medida_base, factor) VALUES (2, 'gramos', 'gr.', 2, 1000);
INSERT INTO unidad_medida (cod_unidad_medida, nom_unidad_medida, nom_unidad_medida_abrev, cod_unidad_medida_base, factor) VALUES (4, 'mililitros', 'ml.', 3, 1000);

-- perfil
INSERT INTO perfil (cod_perfil, nom_perfil, descripcion) VALUES (0, 'Administrador TI', 'Administrador desde el punto de vista TI del sistema. En resumen, tiene acceso a todo.');
INSERT INTO perfil (cod_perfil, nom_perfil, descripcion) VALUES (1, 'Administrador de carrera', 'Administrador de entidades del sistema, usuarios y perfiles. También accede a reportes de gestión.');
INSERT INTO perfil (cod_perfil, nom_perfil, descripcion) VALUES (2, 'Docente', 'Docentes de la carrera responsables de la ejecución del taller.');

-- asign
INSERT INTO asign (sigla, nom_asign, nom_asign_abrev, cod_carrera) VALUES ('ABT3111', 'Salón básico hotelería', 'Básico', 2);
INSERT INTO asign (sigla, nom_asign, nom_asign_abrev, cod_carrera) VALUES ('ABT3121', 'Taller de bar', 'Bar', 2);
INSERT INTO asign (sigla, nom_asign, nom_asign_abrev, cod_carrera) VALUES ('ABT3142', 'Taller de gastronomía de hotelería', 'Gastronomía de hotelería', 2);
INSERT INTO asign (sigla, nom_asign, nom_asign_abrev, cod_carrera) VALUES ('RHT2121', 'Taller de pisos', 'Pisos', 2);
INSERT INTO asign (sigla, nom_asign, nom_asign_abrev, cod_carrera) VALUES ('TCC3301', 'Taller de gastronomía optativo', 'Gastronomía optativo', 2);
INSERT INTO asign (sigla, nom_asign, nom_asign_abrev, cod_carrera) VALUES ('ABT2131', 'Cata de vinos', 'Cata', 1);
INSERT INTO asign (sigla, nom_asign, nom_asign_abrev, cod_carrera) VALUES ('ABT3131', 'Bar y coctelería', 'Bar', 1);
INSERT INTO asign (sigla, nom_asign, nom_asign_abrev, cod_carrera) VALUES ('ABT3141', 'Salón comedor básico', 'Comedor básico', 1);
INSERT INTO asign (sigla, nom_asign, nom_asign_abrev, cod_carrera) VALUES ('ABT4151', 'Salón comedor avanzado', 'Comedor avanzado', 1);
INSERT INTO asign (sigla, nom_asign, nom_asign_abrev, cod_carrera) VALUES ('CIT1111', 'Taller de cocina básica', 'Cocina básica', 1);
INSERT INTO asign (sigla, nom_asign, nom_asign_abrev, cod_carrera) VALUES ('CIT2111', 'Taller de cocina institucional', 'Cocina institucional', 1);
INSERT INTO asign (sigla, nom_asign, nom_asign_abrev, cod_carrera) VALUES ('CRT3111', 'Taller de cocina internacional', 'Cocina internacional', 1);
INSERT INTO asign (sigla, nom_asign, nom_asign_abrev, cod_carrera) VALUES ('CRT4111', 'Taller de cocina chilena', 'Cocina chilena', 1);
INSERT INTO asign (sigla, nom_asign, nom_asign_abrev, cod_carrera) VALUES ('PRT1131', 'Taller de panadería', 'Panadería', 1);
INSERT INTO asign (sigla, nom_asign, nom_asign_abrev, cod_carrera) VALUES ('PRT2121', 'Taller de pastelería', 'Pastelería', 1);
INSERT INTO asign (sigla, nom_asign, nom_asign_abrev, cod_carrera) VALUES ('PTT6697', 'Portafolio de título', 'Portafolio', 1);

-- item_menu (nodos raíz primero)
INSERT INTO item_menu (cod_item_menu, nom_item_menu, descripcion, url, cod_item_menu_padre) VALUES ('01', 'Administración', 'Administración de distintas configuraciones del sistema', NULL, NULL);
INSERT INTO item_menu (cod_item_menu, nom_item_menu, descripcion, url, cod_item_menu_padre) VALUES ('02', 'Consultas', 'Consultas del sistema', NULL, NULL);
INSERT INTO item_menu (cod_item_menu, nom_item_menu, descripcion, url, cod_item_menu_padre) VALUES ('03', 'Reportes', 'Reportes del sistema', NULL, NULL);
INSERT INTO item_menu (cod_item_menu, nom_item_menu, descripcion, url, cod_item_menu_padre) VALUES ('101', 'Usuarios', 'Administración de usuarios', 'usuarios/', '01');
INSERT INTO item_menu (cod_item_menu, nom_item_menu, descripcion, url, cod_item_menu_padre) VALUES ('102', '-', 'Separador', NULL, '01');
INSERT INTO item_menu (cod_item_menu, nom_item_menu, descripcion, url, cod_item_menu_padre) VALUES ('103', 'Talleres', 'Administración de talleres', 'asignaturas/lista/', '01');
INSERT INTO item_menu (cod_item_menu, nom_item_menu, descripcion, url, cod_item_menu_padre) VALUES ('104', 'Programación', 'Administración de programación', 'programacion/lista/', '01');
INSERT INTO item_menu (cod_item_menu, nom_item_menu, descripcion, url, cod_item_menu_padre) VALUES ('105', '-', 'Separador', NULL, '01');
INSERT INTO item_menu (cod_item_menu, nom_item_menu, descripcion, url, cod_item_menu_padre) VALUES ('106', 'Productos', 'Administración de programación', '/productos/lista/', '01');
INSERT INTO item_menu (cod_item_menu, nom_item_menu, descripcion, url, cod_item_menu_padre) VALUES ('107', '-', 'Separador', NULL, '01');
INSERT INTO item_menu (cod_item_menu, nom_item_menu, descripcion, url, cod_item_menu_padre) VALUES ('108', 'Registro', 'Registro de ejecución de talleres', 'registro/lista', '01');
INSERT INTO item_menu (cod_item_menu, nom_item_menu, descripcion, url, cod_item_menu_padre) VALUES ('201', 'Consulta 01', 'Consulta 01', 'consultas/1/', '02');
INSERT INTO item_menu (cod_item_menu, nom_item_menu, descripcion, url, cod_item_menu_padre) VALUES ('202', 'Consulta 02', 'Consulta 02', 'consultas/2/', '02');
INSERT INTO item_menu (cod_item_menu, nom_item_menu, descripcion, url, cod_item_menu_padre) VALUES ('203', 'Consulta 03', 'Consulta 03', 'consultas/3/', '02');
INSERT INTO item_menu (cod_item_menu, nom_item_menu, descripcion, url, cod_item_menu_padre) VALUES ('204', 'Consulta 04', 'Consulta 04', 'consultas/4/', '02');
INSERT INTO item_menu (cod_item_menu, nom_item_menu, descripcion, url, cod_item_menu_padre) VALUES ('205', 'Consulta 05', 'Consulta 05', 'consultas/5/', '02');
INSERT INTO item_menu (cod_item_menu, nom_item_menu, descripcion, url, cod_item_menu_padre) VALUES ('301', 'Reporte 01', 'Reporte 01', 'reportes/1/', '03');
INSERT INTO item_menu (cod_item_menu, nom_item_menu, descripcion, url, cod_item_menu_padre) VALUES ('302', 'Reporte 02', 'Reporte 02', 'reportes/2/', '03');
INSERT INTO item_menu (cod_item_menu, nom_item_menu, descripcion, url, cod_item_menu_padre) VALUES ('303', 'Reporte 03', 'Reporte 03', 'reportes/3/', '03');
INSERT INTO item_menu (cod_item_menu, nom_item_menu, descripcion, url, cod_item_menu_padre) VALUES ('304', 'Reporte 04', 'Reporte 04', 'reportes/4/', '03');
INSERT INTO item_menu (cod_item_menu, nom_item_menu, descripcion, url, cod_item_menu_padre) VALUES ('305', 'Reporte 05', 'Reporte 05', 'reportes/5/', '03');

-- config_perfil
INSERT INTO config_perfil (cod_perfil, cod_item_menu) VALUES (0, '01');
INSERT INTO config_perfil (cod_perfil, cod_item_menu) VALUES (0, '101');
INSERT INTO config_perfil (cod_perfil, cod_item_menu) VALUES (0, '102');
INSERT INTO config_perfil (cod_perfil, cod_item_menu) VALUES (0, '103');
INSERT INTO config_perfil (cod_perfil, cod_item_menu) VALUES (0, '104');
INSERT INTO config_perfil (cod_perfil, cod_item_menu) VALUES (0, '105');
INSERT INTO config_perfil (cod_perfil, cod_item_menu) VALUES (0, '106');
INSERT INTO config_perfil (cod_perfil, cod_item_menu) VALUES (0, '107');
INSERT INTO config_perfil (cod_perfil, cod_item_menu) VALUES (0, '108');
INSERT INTO config_perfil (cod_perfil, cod_item_menu) VALUES (0, '02');
INSERT INTO config_perfil (cod_perfil, cod_item_menu) VALUES (0, '201');
INSERT INTO config_perfil (cod_perfil, cod_item_menu) VALUES (0, '202');
INSERT INTO config_perfil (cod_perfil, cod_item_menu) VALUES (0, '203');
INSERT INTO config_perfil (cod_perfil, cod_item_menu) VALUES (0, '204');
INSERT INTO config_perfil (cod_perfil, cod_item_menu) VALUES (0, '205');
INSERT INTO config_perfil (cod_perfil, cod_item_menu) VALUES (0, '03');
INSERT INTO config_perfil (cod_perfil, cod_item_menu) VALUES (0, '301');
INSERT INTO config_perfil (cod_perfil, cod_item_menu) VALUES (0, '302');
INSERT INTO config_perfil (cod_perfil, cod_item_menu) VALUES (0, '303');
INSERT INTO config_perfil (cod_perfil, cod_item_menu) VALUES (0, '304');
INSERT INTO config_perfil (cod_perfil, cod_item_menu) VALUES (0, '305');
INSERT INTO config_perfil (cod_perfil, cod_item_menu) VALUES (1, '01');
INSERT INTO config_perfil (cod_perfil, cod_item_menu) VALUES (1, '101');
INSERT INTO config_perfil (cod_perfil, cod_item_menu) VALUES (1, '102');
INSERT INTO config_perfil (cod_perfil, cod_item_menu) VALUES (1, '103');
INSERT INTO config_perfil (cod_perfil, cod_item_menu) VALUES (1, '104');
INSERT INTO config_perfil (cod_perfil, cod_item_menu) VALUES (1, '105');
INSERT INTO config_perfil (cod_perfil, cod_item_menu) VALUES (1, '106');
INSERT INTO config_perfil (cod_perfil, cod_item_menu) VALUES (1, '02');
INSERT INTO config_perfil (cod_perfil, cod_item_menu) VALUES (1, '201');
INSERT INTO config_perfil (cod_perfil, cod_item_menu) VALUES (1, '202');
INSERT INTO config_perfil (cod_perfil, cod_item_menu) VALUES (1, '203');
INSERT INTO config_perfil (cod_perfil, cod_item_menu) VALUES (1, '204');
INSERT INTO config_perfil (cod_perfil, cod_item_menu) VALUES (1, '205');
INSERT INTO config_perfil (cod_perfil, cod_item_menu) VALUES (1, '03');
INSERT INTO config_perfil (cod_perfil, cod_item_menu) VALUES (1, '301');
INSERT INTO config_perfil (cod_perfil, cod_item_menu) VALUES (1, '302');
INSERT INTO config_perfil (cod_perfil, cod_item_menu) VALUES (1, '303');
INSERT INTO config_perfil (cod_perfil, cod_item_menu) VALUES (1, '304');
INSERT INTO config_perfil (cod_perfil, cod_item_menu) VALUES (1, '305');
INSERT INTO config_perfil (cod_perfil, cod_item_menu) VALUES (2, '01');
INSERT INTO config_perfil (cod_perfil, cod_item_menu) VALUES (2, '108');
INSERT INTO config_perfil (cod_perfil, cod_item_menu) VALUES (2, '02');
INSERT INTO config_perfil (cod_perfil, cod_item_menu) VALUES (2, '201');

COMMIT;