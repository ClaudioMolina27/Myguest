/* ============================================================
   SCRIPT 11 - NUEVAS TABLAS PARA MÓDULOS MYGUEST v2.0
   Motor: PostgreSQL
   
   Tablas nuevas:
     - inventario         (stock en tiempo real)
     - proveedor          (módulo compras)
     - familia_producto   (agrupación de productos por familia)
     - orden_compra       (módulo compras)
     - det_orden_compra   (detalle de orden de compra)
     - factura            (módulo facturación)
     - det_factura        (detalle de factura)
     - homologacion       (IA: mapeo nombre proveedor → producto interno)
     - devolucion         (módulo devoluciones)
     - det_devolucion     (detalle de devolución)
     - merma              (módulo mermas)
     - motivo_merma       (catálogo de motivos de merma)
   
   Modificaciones a tablas existentes:
     - taller             (agrega columna jornada)
     - producto           (agrega columna stock_minimo)
   ============================================================ */

BEGIN;

/* ──────────────────────────────────────────────────────────────
   DROPS en orden inverso a las FK (solo si existen)
────────────────────────────────────────────────────────────── */
DROP TABLE IF EXISTS merma              CASCADE;
DROP TABLE IF EXISTS motivo_merma       CASCADE;
DROP TABLE IF EXISTS det_devolucion     CASCADE;
DROP TABLE IF EXISTS devolucion         CASCADE;
DROP TABLE IF EXISTS homologacion       CASCADE;
DROP TABLE IF EXISTS det_factura        CASCADE;
DROP TABLE IF EXISTS factura            CASCADE;
DROP TABLE IF EXISTS det_orden_compra   CASCADE;
DROP TABLE IF EXISTS orden_compra       CASCADE;
DROP TABLE IF EXISTS familia_producto   CASCADE;
DROP TABLE IF EXISTS proveedor          CASCADE;
DROP TABLE IF EXISTS inventario         CASCADE;

/* ──────────────────────────────────────────────────────────────
   1. INVENTARIO
   Stock en tiempo real por producto.
   Se actualiza mediante triggers al registrar facturas,
   ejecución de talleres y devoluciones.
────────────────────────────────────────────────────────────── */
CREATE TABLE inventario (
    id_producto         int             NOT NULL,
    stock_actual        numeric(12,6)   NOT NULL DEFAULT 0,
    stock_minimo        numeric(12,6)   NOT NULL DEFAULT 0,
    fecha_actualizacion timestamptz     NOT NULL DEFAULT now(),
    PRIMARY KEY (id_producto)
);

COMMENT ON TABLE  inventario                   IS 'Stock en tiempo real por producto';
COMMENT ON COLUMN inventario.id_producto       IS 'FK a producto';
COMMENT ON COLUMN inventario.stock_actual      IS 'Cantidad disponible actualmente en bodega';
COMMENT ON COLUMN inventario.stock_minimo      IS 'Cantidad mínima antes de generar alerta de reposición';
COMMENT ON COLUMN inventario.fecha_actualizacion IS 'Fecha y hora de la última modificación del stock';

ALTER TABLE inventario
    ADD CONSTRAINT inventario_producto_fk
    FOREIGN KEY (id_producto) REFERENCES producto (id_producto);


/* ──────────────────────────────────────────────────────────────
   2. PROVEEDOR
   Empresas que abastecen los insumos.
────────────────────────────────────────────────────────────── */
CREATE TABLE proveedor (
    id_proveedor    SERIAL,
    nom_proveedor   varchar(100)    NOT NULL,
    rut             varchar(12),
    contacto        varchar(60),
    email           varchar(80),
    telefono        varchar(20),
    activo          boolean         NOT NULL DEFAULT true,
    PRIMARY KEY (id_proveedor)
);

COMMENT ON TABLE  proveedor              IS 'Proveedores de insumos';
COMMENT ON COLUMN proveedor.rut          IS 'RUT del proveedor (formato: 12345678-9)';
COMMENT ON COLUMN proveedor.activo       IS 'false = proveedor deshabilitado, no aparece en nuevas OC';


/* ──────────────────────────────────────────────────────────────
   3. FAMILIA_PRODUCTO
   Agrupación de productos por familia (abarrotes, lácteos, etc.)
   para exportar planillas ordenadas a proveedores específicos.
────────────────────────────────────────────────────────────── */
CREATE TABLE familia_producto (
    cod_familia     smallint        NOT NULL,
    nom_familia     varchar(50)     NOT NULL,
    id_proveedor    int,
    PRIMARY KEY (cod_familia)
);

COMMENT ON TABLE  familia_producto             IS 'Familias de productos para agrupación en órdenes de compra';
COMMENT ON COLUMN familia_producto.id_proveedor IS 'Proveedor habitual de esta familia (opcional)';

ALTER TABLE familia_producto
    ADD CONSTRAINT familia_proveedor_fk
    FOREIGN KEY (id_proveedor) REFERENCES proveedor (id_proveedor);

-- Agregar familia a producto
ALTER TABLE producto
    ADD COLUMN IF NOT EXISTS cod_familia smallint;

ALTER TABLE producto
    ADD CONSTRAINT producto_familia_fk
    FOREIGN KEY (cod_familia) REFERENCES familia_producto (cod_familia);


/* ──────────────────────────────────────────────────────────────
   4. ORDEN_COMPRA
   Planificación de compras con anticipación de 30 días.
────────────────────────────────────────────────────────────── */
CREATE TABLE orden_compra (
    id_orden_compra     SERIAL,
    fecha_emision       date            NOT NULL DEFAULT current_date,
    fecha_entrega_est   date            NOT NULL,
    id_proveedor        int             NOT NULL,
    id_usuario          int             NOT NULL,
    estado              varchar(20)     NOT NULL DEFAULT 'borrador',
    obs                 varchar(500),
    PRIMARY KEY (id_orden_compra),
    CONSTRAINT oc_estado_ck CHECK (estado IN ('borrador','enviada','recibida','anulada'))
);

COMMENT ON TABLE  orden_compra                    IS 'Órdenes de compra a proveedores';
COMMENT ON COLUMN orden_compra.fecha_entrega_est  IS 'Fecha estimada de entrega del pedido';
COMMENT ON COLUMN orden_compra.estado             IS 'borrador | enviada | recibida | anulada';
COMMENT ON COLUMN orden_compra.id_usuario         IS 'Usuario que generó la orden';

ALTER TABLE orden_compra ADD CONSTRAINT oc_proveedor_fk FOREIGN KEY (id_proveedor) REFERENCES proveedor     (id_proveedor);
ALTER TABLE orden_compra ADD CONSTRAINT oc_usuario_fk   FOREIGN KEY (id_usuario)   REFERENCES usuario       (id_usuario);


/* ──────────────────────────────────────────────────────────────
   5. DET_ORDEN_COMPRA
   Detalle de productos por orden de compra.
────────────────────────────────────────────────────────────── */
CREATE TABLE det_orden_compra (
    id_orden_compra     int             NOT NULL,
    id_producto         int             NOT NULL,
    cantidad            numeric(12,6)   NOT NULL,
    precio_unitario     int             NOT NULL,
    PRIMARY KEY (id_orden_compra, id_producto)
);

COMMENT ON TABLE det_orden_compra IS 'Detalle de productos incluidos en una orden de compra';

ALTER TABLE det_orden_compra ADD CONSTRAINT detoc_oc_fk      FOREIGN KEY (id_orden_compra) REFERENCES orden_compra (id_orden_compra);
ALTER TABLE det_orden_compra ADD CONSTRAINT detoc_producto_fk FOREIGN KEY (id_producto)    REFERENCES producto     (id_producto);


/* ──────────────────────────────────────────────────────────────
   6. FACTURA
   Documento tributario de ingreso de mercadería.
   Se asocia a una orden de compra para la conciliación.
────────────────────────────────────────────────────────────── */
CREATE TABLE factura (
    id_factura          SERIAL,
    num_documento       varchar(20)     NOT NULL,
    fecha_emision       date            NOT NULL,
    fecha_ingreso       timestamptz     NOT NULL DEFAULT now(),
    id_proveedor        int             NOT NULL,
    id_orden_compra     int,
    id_usuario          int             NOT NULL,
    estado_conciliacion varchar(20)     NOT NULL DEFAULT 'pendiente',
    obs                 varchar(500),
    PRIMARY KEY (id_factura),
    CONSTRAINT factura_estado_ck CHECK (estado_conciliacion IN ('pendiente','conciliada','con_diferencia'))
);

COMMENT ON TABLE  factura                          IS 'Facturas de proveedores ingresadas al sistema';
COMMENT ON COLUMN factura.num_documento            IS 'Número de folio del documento tributario';
COMMENT ON COLUMN factura.id_orden_compra          IS 'OC asociada para conciliación (puede ser NULL si no hay OC previa)';
COMMENT ON COLUMN factura.estado_conciliacion      IS 'pendiente | conciliada | con_diferencia';

ALTER TABLE factura ADD CONSTRAINT factura_proveedor_fk  FOREIGN KEY (id_proveedor)    REFERENCES proveedor    (id_proveedor);
ALTER TABLE factura ADD CONSTRAINT factura_oc_fk         FOREIGN KEY (id_orden_compra) REFERENCES orden_compra (id_orden_compra);
ALTER TABLE factura ADD CONSTRAINT factura_usuario_fk    FOREIGN KEY (id_usuario)      REFERENCES usuario      (id_usuario);


/* ──────────────────────────────────────────────────────────────
   7. DET_FACTURA
   Detalle de productos ingresados por factura.
   Al confirmar, un trigger suma el stock en inventario.
────────────────────────────────────────────────────────────── */
CREATE TABLE det_factura (
    id_factura          int             NOT NULL,
    id_producto         int             NOT NULL,
    cantidad            numeric(12,6)   NOT NULL,
    precio_unitario     int             NOT NULL,
    fecha_vencimiento   date,
    PRIMARY KEY (id_factura, id_producto)
);

COMMENT ON TABLE  det_factura                      IS 'Detalle de productos de una factura';
COMMENT ON COLUMN det_factura.fecha_vencimiento    IS 'Fecha de caducidad del lote ingresado (ingreso manual por bodeguero)';

ALTER TABLE det_factura ADD CONSTRAINT detfac_factura_fk  FOREIGN KEY (id_factura)  REFERENCES factura  (id_factura);
ALTER TABLE det_factura ADD CONSTRAINT detfac_producto_fk FOREIGN KEY (id_producto) REFERENCES producto (id_producto);


/* ──────────────────────────────────────────────────────────────
   8. HOMOLOGACION
   Tabla de aprendizaje de la IA:
   mapea el nombre que usa el proveedor en su factura
   al producto interno del sistema.
────────────────────────────────────────────────────────────── */
CREATE TABLE homologacion (
    id_homologacion     SERIAL,
    nom_externo         varchar(200)    NOT NULL,
    id_proveedor        int             NOT NULL,
    id_producto         int             NOT NULL,
    confirmado          boolean         NOT NULL DEFAULT false,
    fecha_confirmacion  timestamptz,
    id_usuario          int,
    PRIMARY KEY (id_homologacion),
    UNIQUE (nom_externo, id_proveedor)
);

COMMENT ON TABLE  homologacion                  IS 'Mapeo de nombres externos (factura) a productos internos del catálogo';
COMMENT ON COLUMN homologacion.nom_externo      IS 'Nombre tal como aparece en la factura del proveedor';
COMMENT ON COLUMN homologacion.confirmado       IS 'true = el bodeguero validó el mapeo. false = sugerencia de la IA pendiente';
COMMENT ON COLUMN homologacion.id_usuario       IS 'Usuario que confirmó el mapeo';

ALTER TABLE homologacion ADD CONSTRAINT homolog_proveedor_fk FOREIGN KEY (id_proveedor) REFERENCES proveedor (id_proveedor);
ALTER TABLE homologacion ADD CONSTRAINT homolog_producto_fk  FOREIGN KEY (id_producto)  REFERENCES producto  (id_producto);
ALTER TABLE homologacion ADD CONSTRAINT homolog_usuario_fk   FOREIGN KEY (id_usuario)   REFERENCES usuario   (id_usuario);


/* ──────────────────────────────────────────────────────────────
   9. DEVOLUCION
   Registro de insumos devueltos por un docente
   al finalizar un taller. Obliga a justificar el sobrante.
────────────────────────────────────────────────────────────── */
CREATE TABLE devolucion (
    id_devolucion       SERIAL,
    fecha               date            NOT NULL DEFAULT current_date,
    ano_academ          smallint        NOT NULL,
    cod_periodo_academ  smallint        NOT NULL,
    sigla               varchar(15)     NOT NULL,
    seccion             smallint        NOT NULL,
    id_taller           int             NOT NULL,
    id_usuario          int             NOT NULL,
    motivo_sobrante     varchar(500)    NOT NULL,
    PRIMARY KEY (id_devolucion)
);

COMMENT ON TABLE  devolucion                IS 'Registro de devoluciones de insumos tras un taller';
COMMENT ON COLUMN devolucion.motivo_sobrante IS 'Comentario obligatorio que justifica por qué sobró material';

ALTER TABLE devolucion ADD CONSTRAINT devolucion_registaller_fk FOREIGN KEY (fecha, ano_academ, cod_periodo_academ, sigla, seccion, id_taller) REFERENCES regis_taller (fecha, ano_academ, cod_periodo_academ, sigla, seccion, id_taller);
ALTER TABLE devolucion ADD CONSTRAINT devolucion_usuario_fk     FOREIGN KEY (id_usuario) REFERENCES usuario (id_usuario);


/* ──────────────────────────────────────────────────────────────
   10. DET_DEVOLUCION
   Detalle de productos devueltos.
   Un trigger suma el stock devuelto en inventario.
────────────────────────────────────────────────────────────── */
CREATE TABLE det_devolucion (
    id_devolucion   int             NOT NULL,
    id_producto     int             NOT NULL,
    cantidad        numeric(12,6)   NOT NULL,
    PRIMARY KEY (id_devolucion, id_producto)
);

COMMENT ON TABLE det_devolucion IS 'Detalle de productos devueltos en una devolución';

ALTER TABLE det_devolucion ADD CONSTRAINT detdev_devolucion_fk FOREIGN KEY (id_devolucion) REFERENCES devolucion (id_devolucion);
ALTER TABLE det_devolucion ADD CONSTRAINT detdev_producto_fk   FOREIGN KEY (id_producto)   REFERENCES producto   (id_producto);


/* ──────────────────────────────────────────────────────────────
   11. MOTIVO_MERMA
   Catálogo de motivos por los que se descarta un insumo.
────────────────────────────────────────────────────────────── */
CREATE TABLE motivo_merma (
    cod_motivo_merma    smallint        NOT NULL,
    nom_motivo_merma    varchar(50)     NOT NULL,
    PRIMARY KEY (cod_motivo_merma)
);

COMMENT ON TABLE motivo_merma IS 'Catálogo de motivos de descarte de insumos';

INSERT INTO motivo_merma VALUES (1, 'Vencimiento');
INSERT INTO motivo_merma VALUES (2, 'Mal estado al ingreso');
INSERT INTO motivo_merma VALUES (3, 'Daño en bodega');
INSERT INTO motivo_merma VALUES (4, 'Error de preparación');
INSERT INTO motivo_merma VALUES (5, 'Otro');


/* ──────────────────────────────────────────────────────────────
   12. MERMA
   Registro de insumos descartados con evidencia fotográfica
   (la URL de la foto se guarda, la imagen en almacenamiento externo).
────────────────────────────────────────────────────────────── */
CREATE TABLE merma (
    id_merma            SERIAL,
    fecha               date            NOT NULL DEFAULT current_date,
    id_producto         int             NOT NULL,
    cantidad            numeric(12,6)   NOT NULL,
    cod_motivo_merma    smallint        NOT NULL,
    id_usuario          int             NOT NULL,
    obs                 varchar(500),
    url_foto            varchar(300),
    PRIMARY KEY (id_merma)
);

COMMENT ON TABLE  merma           IS 'Registro de mermas (insumos descartados)';
COMMENT ON COLUMN merma.url_foto  IS 'URL de la fotografía de evidencia del estado del producto';

ALTER TABLE merma ADD CONSTRAINT merma_producto_fk     FOREIGN KEY (id_producto)       REFERENCES producto    (id_producto);
ALTER TABLE merma ADD CONSTRAINT merma_motivo_fk       FOREIGN KEY (cod_motivo_merma)  REFERENCES motivo_merma (cod_motivo_merma);
ALTER TABLE merma ADD CONSTRAINT merma_usuario_fk      FOREIGN KEY (id_usuario)        REFERENCES usuario     (id_usuario);


/* ──────────────────────────────────────────────────────────────
   MODIFICACIONES A TABLAS EXISTENTES
────────────────────────────────────────────────────────────── */

-- Agregar jornada a taller
ALTER TABLE taller
    ADD COLUMN IF NOT EXISTS jornada varchar(6) DEFAULT 'manana'
    CONSTRAINT taller_jornada_ck CHECK (jornada IN ('manana','tarde','noche'));

COMMENT ON COLUMN taller.jornada IS 'Jornada del taller: manana | tarde | noche';


/* ──────────────────────────────────────────────────────────────
   TRIGGERS DE STOCK (tiempo real)
   
   Trigger 1: al confirmar factura → SUBE stock en inventario
   Trigger 2: al registrar taller  → BAJA stock en inventario
   Trigger 3: al registrar devol.  → SUBE stock en inventario
────────────────────────────────────────────────────────────── */

-- Función genérica que ajusta el stock
CREATE OR REPLACE FUNCTION fn_ajustar_stock()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO inventario (id_producto, stock_actual, fecha_actualizacion)
    VALUES (NEW.id_producto, 0, now())
    ON CONFLICT (id_producto) DO NOTHING;

    IF TG_TABLE_NAME = 'det_factura' THEN
        UPDATE inventario
        SET stock_actual = stock_actual + NEW.cantidad,
            fecha_actualizacion = now()
        WHERE id_producto = NEW.id_producto;

    ELSIF TG_TABLE_NAME = 'det_regis_taller' THEN
        UPDATE inventario
        SET stock_actual = stock_actual - NEW.cantidad,
            fecha_actualizacion = now()
        WHERE id_producto = NEW.id_producto;

    ELSIF TG_TABLE_NAME = 'det_devolucion' THEN
        UPDATE inventario
        SET stock_actual = stock_actual + NEW.cantidad,
            fecha_actualizacion = now()
        WHERE id_producto = NEW.id_producto;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger 1: factura ingresada → sube stock
DROP TRIGGER IF EXISTS trg_stock_entrada ON det_factura;
CREATE TRIGGER trg_stock_entrada
    AFTER INSERT ON det_factura
    FOR EACH ROW EXECUTE FUNCTION fn_ajustar_stock();

-- Trigger 2: taller ejecutado → baja stock
DROP TRIGGER IF EXISTS trg_stock_salida ON det_regis_taller;
CREATE TRIGGER trg_stock_salida
    AFTER INSERT ON det_regis_taller
    FOR EACH ROW EXECUTE FUNCTION fn_ajustar_stock();

-- Trigger 3: devolución registrada → sube stock
DROP TRIGGER IF EXISTS trg_stock_devolucion ON det_devolucion;
CREATE TRIGGER trg_stock_devolucion
    AFTER INSERT ON det_devolucion
    FOR EACH ROW EXECUTE FUNCTION fn_ajustar_stock();

COMMIT;
