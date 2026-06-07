from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import date


class ReporteStockItem(BaseModel):
    id_producto: int
    nom_producto: str
    nom_categ_producto: str
    nom_unidad_medida: str
    stock_actual: float
    stock_minimo: float
    diferencia: float
    estado: str

    model_config = ConfigDict(from_attributes=True)


class ReporteConsumoItem(BaseModel):
    sigla: str
    nom_asign: str
    id_taller: int
    titulo_preparacion: Optional[str] = None
    fecha: date
    nom_producto: str
    cantidad: float
    precio_unitario: int
    costo_total: float

    model_config = ConfigDict(from_attributes=True)


class ReporteFacturaItem(BaseModel):
    id_factura: int
    num_documento: str
    fecha_emision: date
    nom_proveedor: str
    estado_conciliacion: str
    total_productos: int
    monto_total: float

    model_config = ConfigDict(from_attributes=True)


class ReporteMermaDevolucionItem(BaseModel):
    tipo: str
    fecha: date
    nom_producto: str
    cantidad: float
    motivo: str
    nom_usuario: str

    model_config = ConfigDict(from_attributes=True)


class ReporteCostoAsignaturaItem(BaseModel):
    sigla: str
    nom_asign: str
    num_talleres: int
    costo_total: float
    costo_promedio_taller: float

    model_config = ConfigDict(from_attributes=True)


class ReporteCompleto(BaseModel):
    ano_academ: Optional[int] = None
    cod_periodo_academ: Optional[int] = None
    sigla: Optional[str] = None
    stock: List[ReporteStockItem] = []
    consumo: List[ReporteConsumoItem] = []
    facturas: List[ReporteFacturaItem] = []
    mermas_devoluciones: List[ReporteMermaDevolucionItem] = []
    costos_asignatura: List[ReporteCostoAsignaturaItem] = []