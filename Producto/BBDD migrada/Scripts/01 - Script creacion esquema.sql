/* ============================================================
   SCRIPT 01 - CREACIÓN DE ESQUEMA (DDL)
   Base de datos: Sistema de Gestión de Talleres
   Motor: PostgreSQL
   ============================================================ */

/* ---- DROP en orden inverso a las FK ---- */
DROP TABLE IF EXISTS config_perfil      CASCADE;
DROP TABLE IF EXISTS det_regis_taller   CASCADE;
DROP TABLE IF EXISTS regis_taller       CASCADE;
DROP TABLE IF EXISTS prog_taller        CASCADE;
DROP TABLE IF EXISTS prog_asign         CASCADE;
DROP TABLE IF EXISTS config_taller      CASCADE;
DROP TABLE IF EXISTS producto           CASCADE;
DROP TABLE IF EXISTS taller             CASCADE;
DROP TABLE IF EXISTS usuario            CASCADE;
DROP TABLE IF EXISTS asign              CASCADE;
DROP TABLE IF EXISTS carrera            CASCADE;
DROP TABLE IF EXISTS categ_producto     CASCADE;
DROP TABLE IF EXISTS unidad_medida      CASCADE;
DROP TABLE IF EXISTS item_menu          CASCADE;
DROP TABLE IF EXISTS perfil             CASCADE;
DROP TABLE IF EXISTS periodo_academ     CASCADE;
DROP TABLE IF EXISTS agrupador          CASCADE;
DROP TABLE IF EXISTS param              CASCADE;

/* ---- TABLAS ---- */

CREATE TABLE param (
    cod_param   smallint     NOT NULL,
    nom_param   varchar(50)  NOT NULL,
    valor       varchar(50),
    PRIMARY KEY (cod_param)
);
COMMENT ON TABLE  param           IS 'Parámetros del sistema';
COMMENT ON COLUMN param.cod_param IS 'Código del parámetro del sistema';
COMMENT ON COLUMN param.nom_param IS 'Nombre del parámetro del sistema';
COMMENT ON COLUMN param.valor     IS 'Valor del parámetro';

CREATE TABLE item_menu (
    cod_item_menu        varchar(4)   NOT NULL,
    nom_item_menu        varchar(50)  NOT NULL,
    descripcion          varchar(500),
    url                  varchar(100),
    cod_item_menu_padre  varchar(4),
    PRIMARY KEY (cod_item_menu)
);
COMMENT ON TABLE item_menu IS 'Opciones de menú del sistema';

CREATE TABLE perfil (
    cod_perfil   smallint     NOT NULL,
    nom_perfil   varchar(30)  NOT NULL,
    descripcion  varchar(500) NOT NULL,
    PRIMARY KEY (cod_perfil)
);
COMMENT ON TABLE perfil IS 'Perfiles de acceso del sistema';

CREATE TABLE config_perfil (
    cod_perfil     smallint    NOT NULL,
    cod_item_menu  varchar(4)  NOT NULL,
    PRIMARY KEY (cod_perfil, cod_item_menu)
);
COMMENT ON TABLE config_perfil IS 'Configuración de acceso a menú por perfil';

CREATE TABLE agrupador (
    cod_agrupador  smallint     NOT NULL,
    nom_agrupador  varchar(100) NOT NULL,
    PRIMARY KEY (cod_agrupador)
);
COMMENT ON TABLE agrupador IS 'Agrupadores de productos en la especificación de un taller';

CREATE TABLE carrera (
    cod_carrera        smallint    NOT NULL,
    nom_carrera        varchar(30) NOT NULL,
    nom_carrera_abrev  varchar(10),
    PRIMARY KEY (cod_carrera)
);

CREATE TABLE asign (
    sigla            varchar(15) NOT NULL,
    nom_asign        varchar(50) NOT NULL,
    nom_asign_abrev  varchar(30) NOT NULL,
    cod_carrera      smallint    NOT NULL,
    PRIMARY KEY (sigla)
);

CREATE TABLE categ_producto (
    cod_categ_producto  smallint    NOT NULL,
    nom_categ_producto  varchar(30) NOT NULL,
    PRIMARY KEY (cod_categ_producto)
);

CREATE TABLE unidad_medida (
    cod_unidad_medida        smallint     NOT NULL,
    nom_unidad_medida        varchar(20)  NOT NULL,
    nom_unidad_medida_abrev  varchar(12)  NOT NULL,
    cod_unidad_medida_base   smallint,
    factor                   numeric(6,2),
    PRIMARY KEY (cod_unidad_medida)
);

CREATE TABLE producto (
    id_producto         SERIAL,
    nom_producto        varchar(100) NOT NULL,
    precio              int          NOT NULL,
    cod_unidad_medida   smallint     NOT NULL,
    cod_categ_producto  smallint     NOT NULL,
    PRIMARY KEY (id_producto)
);

CREATE TABLE taller (
    id_taller            SERIAL,
    titulo_preparacion   varchar(100),
    detalle_preparacion  varchar(2000),
    semana               smallint    NOT NULL,
    sigla                varchar(15) NOT NULL,
    PRIMARY KEY (id_taller)
);

CREATE TABLE config_taller (
    id_producto    int      NOT NULL,
    id_taller      int      NOT NULL,
    cod_agrupador  smallint NOT NULL,
    cantidad       numeric(12,6),
    PRIMARY KEY (id_producto, id_taller, cod_agrupador)
);

CREATE TABLE periodo_academ (
    cod_periodo_academ        smallint    NOT NULL,
    nom_periodo_academ        varchar(30) NOT NULL,
    nom_periodo_academ_abrev  varchar(12) NOT NULL,
    PRIMARY KEY (cod_periodo_academ)
);

CREATE TABLE usuario (
    id_usuario        SERIAL,
    login             varchar(40)  NOT NULL,
    hash_password     varchar(256) NOT NULL,
    primer_apellido   varchar(20)  NOT NULL,
    segundo_apellido  varchar(20),
    nom               varchar(20)  NOT NULL,
    nom_preferido     varchar(20),
    cod_perfil        smallint     NOT NULL,
    cod_carrera       smallint     NOT NULL,
    PRIMARY KEY (id_usuario)
);

CREATE TABLE prog_asign (
    ano_academ          smallint    NOT NULL,
    cod_periodo_academ  smallint    NOT NULL,
    sigla               varchar(15) NOT NULL,
    seccion             smallint    NOT NULL,
    PRIMARY KEY (ano_academ, cod_periodo_academ, sigla, seccion)
);

CREATE TABLE prog_taller (
    fecha               date        NOT NULL,
    ano_academ          smallint    NOT NULL,
    cod_periodo_academ  smallint    NOT NULL,
    sigla               varchar(15) NOT NULL,
    seccion             smallint    NOT NULL,
    id_taller           int         NOT NULL,
    id_usuario          int         NOT NULL,
    PRIMARY KEY (fecha, ano_academ, cod_periodo_academ, sigla, seccion, id_taller)
);

CREATE TABLE regis_taller (
    fecha               date        NOT NULL,
    ano_academ          smallint    NOT NULL,
    cod_periodo_academ  smallint    NOT NULL,
    sigla               varchar(15) NOT NULL,
    seccion             smallint    NOT NULL,
    id_taller           int         NOT NULL,
    id_usuario          int         NOT NULL,
    obs                 varchar(500) NOT NULL DEFAULT 'Sin observaciones',
    PRIMARY KEY (fecha, ano_academ, cod_periodo_academ, sigla, seccion, id_taller)
);

CREATE TABLE det_regis_taller (
    fecha               date        NOT NULL,
    ano_academ          smallint    NOT NULL,
    cod_periodo_academ  smallint    NOT NULL,
    sigla               varchar(15) NOT NULL,
    seccion             smallint    NOT NULL,
    id_producto         int         NOT NULL,
    id_taller           int         NOT NULL,
    cod_agrupador       smallint    NOT NULL,
    precio              int         NOT NULL,
    cantidad            numeric(12,6) NOT NULL,
    PRIMARY KEY (fecha, ano_academ, cod_periodo_academ, sigla, seccion, id_producto, id_taller, precio, cod_agrupador)
);

/* ---- FOREIGN KEYS (22 restricciones) ---- */
ALTER TABLE item_menu       ADD CONSTRAINT item_menu_item_menu_fk             FOREIGN KEY (cod_item_menu_padre)                                           REFERENCES item_menu   (cod_item_menu);
ALTER TABLE config_perfil   ADD CONSTRAINT config_perfil_item_menu_fk         FOREIGN KEY (cod_item_menu)                                                 REFERENCES item_menu   (cod_item_menu);
ALTER TABLE config_perfil   ADD CONSTRAINT config_perfil_perfil_fk            FOREIGN KEY (cod_perfil)                                                    REFERENCES perfil      (cod_perfil);
ALTER TABLE unidad_medida   ADD CONSTRAINT unidadmedida_unidadmedida_fk       FOREIGN KEY (cod_unidad_medida_base)                                        REFERENCES unidad_medida (cod_unidad_medida);
ALTER TABLE asign           ADD CONSTRAINT asign_carrera_fk                   FOREIGN KEY (cod_carrera)                                                   REFERENCES carrera     (cod_carrera);
ALTER TABLE producto        ADD CONSTRAINT producto_categproducto_fk          FOREIGN KEY (cod_categ_producto)                                            REFERENCES categ_producto (cod_categ_producto);
ALTER TABLE producto        ADD CONSTRAINT producto_unidadmedida_fk           FOREIGN KEY (cod_unidad_medida)                                             REFERENCES unidad_medida (cod_unidad_medida);
ALTER TABLE taller          ADD CONSTRAINT taller_asign_fk                    FOREIGN KEY (sigla)                                                         REFERENCES asign       (sigla);
ALTER TABLE config_taller   ADD CONSTRAINT configtaller_agrupador_fk          FOREIGN KEY (cod_agrupador)                                                 REFERENCES agrupador   (cod_agrupador);
ALTER TABLE config_taller   ADD CONSTRAINT configtaller_producto_fk           FOREIGN KEY (id_producto)                                                   REFERENCES producto    (id_producto);
ALTER TABLE config_taller   ADD CONSTRAINT configtaller_taller_fk             FOREIGN KEY (id_taller)                                                     REFERENCES taller      (id_taller);
ALTER TABLE usuario         ADD CONSTRAINT usuario_carrera_fk                 FOREIGN KEY (cod_carrera)                                                   REFERENCES carrera     (cod_carrera);
ALTER TABLE usuario         ADD CONSTRAINT usuario_perfil_fk                  FOREIGN KEY (cod_perfil)                                                    REFERENCES perfil      (cod_perfil);
ALTER TABLE prog_asign      ADD CONSTRAINT progasign_asign_fk                 FOREIGN KEY (sigla)                                                         REFERENCES asign       (sigla);
ALTER TABLE prog_asign      ADD CONSTRAINT progasign_periodo_academ_fk        FOREIGN KEY (cod_periodo_academ)                                            REFERENCES periodo_academ (cod_periodo_academ);
ALTER TABLE prog_taller     ADD CONSTRAINT progtaller_progasign_fk            FOREIGN KEY (ano_academ, cod_periodo_academ, sigla, seccion)                REFERENCES prog_asign  (ano_academ, cod_periodo_academ, sigla, seccion);
ALTER TABLE prog_taller     ADD CONSTRAINT progtaller_usuario_fk              FOREIGN KEY (id_usuario)                                                    REFERENCES usuario     (id_usuario);
ALTER TABLE prog_taller     ADD CONSTRAINT progtaller_taller_fk               FOREIGN KEY (id_taller)                                                     REFERENCES taller      (id_taller);
ALTER TABLE regis_taller    ADD CONSTRAINT registaller_progtaller_fk          FOREIGN KEY (fecha, ano_academ, cod_periodo_academ, sigla, seccion, id_taller) REFERENCES prog_taller (fecha, ano_academ, cod_periodo_academ, sigla, seccion, id_taller);
ALTER TABLE regis_taller    ADD CONSTRAINT registaller_usuario_fk             FOREIGN KEY (id_usuario)                                                    REFERENCES usuario     (id_usuario);
ALTER TABLE det_regis_taller ADD CONSTRAINT detregistaller_producto_fk        FOREIGN KEY (id_producto)                                                   REFERENCES producto    (id_producto);
ALTER TABLE det_regis_taller ADD CONSTRAINT detregistaller_registaller_fk     FOREIGN KEY (fecha, ano_academ, cod_periodo_academ, sigla, seccion, id_taller) REFERENCES regis_taller (fecha, ano_academ, cod_periodo_academ, sigla, seccion, id_taller);
