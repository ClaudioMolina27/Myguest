from pydantic import BaseModel, ConfigDict
from typing import Optional, List


class IngredienteReceta(BaseModel):
    id_producto: int
    nom_producto: str
    cod_agrupador: int
    nom_agrupador: str
    cantidad: float
    nom_unidad_medida: str
    precio_unitario: int
    costo_ingrediente: float

    model_config = ConfigDict(from_attributes=True)


class RecetaResumen(BaseModel):
    id_taller: int
    titulo_preparacion: Optional[str] = None
    detalle_preparacion: Optional[str] = None
    semana: int
    sigla: str
    jornada: Optional[str] = None
    num_ingredientes: int
    costo_estimado: float

    model_config = ConfigDict(from_attributes=True)


class RecetaDetalle(BaseModel):
    id_taller: int
    titulo_preparacion: Optional[str] = None
    detalle_preparacion: Optional[str] = None
    semana: int
    sigla: str
    jornada: Optional[str] = None
    ingredientes: List[IngredienteReceta] = []
    costo_estimado: float
    costo_por_alumno: float

    model_config = ConfigDict(from_attributes=True)


class IngredienteDisponibilidad(BaseModel):
    id_producto: int
    nom_producto: str
    cantidad_necesaria: float
    stock_actual: float
    disponible: bool
    faltante: float

    model_config = ConfigDict(from_attributes=True)


class RecetaDisponibilidad(BaseModel):
    id_taller: int
    titulo_preparacion: Optional[str] = None
    ejecutable: bool
    ingredientes: List[IngredienteDisponibilidad] = []


class IngredienteEscalado(BaseModel):
    id_producto: int
    nom_producto: str
    nom_agrupador: str
    cantidad_base: float
    cantidad_escalada: float
    nom_unidad_medida: str
    costo_ingrediente: float


class RecetaEscalada(BaseModel):
    id_taller: int
    titulo_preparacion: Optional[str] = None
    alumnos: int
    porciones_base: int
    ingredientes: List[IngredienteEscalado] = []
    costo_total: float
    costo_por_alumno: float