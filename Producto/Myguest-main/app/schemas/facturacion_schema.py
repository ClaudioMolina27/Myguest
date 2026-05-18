from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import date, datetime


class DetFacturaCreate(BaseModel):
    id_producto: int
    cantidad: float
    precio_unitario: int
    fecha_vencimiento: Optional[date] = None


class FacturaCreate(BaseModel):
    num_documento: str
    fecha_emision: date
    id_proveedor: int
    id_orden_compra: Optional[int] = None
    id_usuario: int
    obs: Optional[str] = None
    detalles: List[DetFacturaCreate]


class FacturaUpdate(BaseModel):
    estado_conciliacion: Optional[str] = None
    obs: Optional[str] = None


class DetFacturaResponse(BaseModel):
    id_factura: int
    id_producto: int
    cantidad: float
    precio_unitario: int
    fecha_vencimiento: Optional[date] = None

    model_config = ConfigDict(from_attributes=True)


class FacturaResponse(BaseModel):
    id_factura: int
    num_documento: str
    fecha_emision: date
    fecha_ingreso: Optional[datetime] = None
    id_proveedor: int
    id_orden_compra: Optional[int] = None
    id_usuario: int
    estado_conciliacion: str
    obs: Optional[str] = None
    detalles: List[DetFacturaResponse] = []

    model_config = ConfigDict(from_attributes=True)