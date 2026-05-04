from pydantic import BaseModel, ConfigDict
from typing import Optional


class ProductoCreate(BaseModel):
    nom_producto: str
    precio: int
    cod_unidad_medida: int
    cod_categ_producto: int
    cod_familia: Optional[int] = None


class ProductoUpdate(BaseModel):
    nom_producto: Optional[str] = None
    precio: Optional[int] = None
    cod_unidad_medida: Optional[int] = None
    cod_categ_producto: Optional[int] = None
    cod_familia: Optional[int] = None


class ProductoResponse(BaseModel):
    id_producto: int
    nom_producto: str
    precio: int
    cod_unidad_medida: int
    cod_categ_producto: int
    cod_familia: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class InventarioUpdate(BaseModel):
    stock_minimo: float


class InventarioResponse(BaseModel):
    id_producto: int
    nom_producto: str
    stock_actual: float
    stock_minimo: float

    model_config = ConfigDict(from_attributes=True)


class AlertaStock(BaseModel):
    id_producto: int
    nom_producto: str
    stock_actual: float
    stock_minimo: float
    diferencia: float

    model_config = ConfigDict(from_attributes=True)