from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import date


class DetOrdenCompraCreate(BaseModel):
    id_producto: int
    cantidad: float
    precio_unitario: int


class OrdenCompraCreate(BaseModel):
    fecha_emision: date
    fecha_entrega_est: date
    id_proveedor: int
    id_usuario: int
    obs: Optional[str] = None
    detalles: List[DetOrdenCompraCreate]


class OrdenCompraUpdate(BaseModel):
    estado: Optional[str] = None
    obs: Optional[str] = None
    fecha_entrega_est: Optional[date] = None


class DetOrdenCompraResponse(BaseModel):
    id_orden_compra: int
    id_producto: int
    cantidad: float
    precio_unitario: int

    model_config = ConfigDict(from_attributes=True)


class OrdenCompraResponse(BaseModel):
    id_orden_compra: int
    fecha_emision: date
    fecha_entrega_est: date
    id_proveedor: int
    id_usuario: int
    estado: str
    obs: Optional[str] = None
    detalles: List[DetOrdenCompraResponse] = []

    model_config = ConfigDict(from_attributes=True)