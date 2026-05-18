from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import date


class CarreraResponse(BaseModel):
    cod_carrera: int
    nom_carrera: str
    nom_carrera_abrev: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class AsignaturaResponse(BaseModel):
    sigla: str
    nom_asign: str
    nom_asign_abrev: str
    cod_carrera: int

    model_config = ConfigDict(from_attributes=True)


class TallerResponse(BaseModel):
    id_taller: int
    titulo_preparacion: Optional[str] = None
    detalle_preparacion: Optional[str] = None
    semana: int
    sigla: str
    jornada: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class PeriodoAcademResponse(BaseModel):
    cod_periodo_academ: int
    nom_periodo_academ: str
    nom_periodo_academ_abrev: str

    model_config = ConfigDict(from_attributes=True)


class ProgAsignCreate(BaseModel):
    ano_academ: int
    cod_periodo_academ: int
    sigla: str
    seccion: int


class ProgAsignResponse(BaseModel):
    ano_academ: int
    cod_periodo_academ: int
    sigla: str
    seccion: int

    model_config = ConfigDict(from_attributes=True)


class ProgTallerCreate(BaseModel):
    fecha: date
    ano_academ: int
    cod_periodo_academ: int
    sigla: str
    seccion: int
    id_taller: int
    id_usuario: int


class ProgTallerResponse(BaseModel):
    fecha: date
    ano_academ: int
    cod_periodo_academ: int
    sigla: str
    seccion: int
    id_taller: int
    id_usuario: int

    model_config = ConfigDict(from_attributes=True)


class DetRegisTallerCreate(BaseModel):
    id_producto: int
    cod_agrupador: int
    precio: int
    cantidad: float


class RegisTallerCreate(BaseModel):
    fecha: date
    ano_academ: int
    cod_periodo_academ: int
    sigla: str
    seccion: int
    id_taller: int
    id_usuario: int
    obs: Optional[str] = "Sin observaciones"
    detalles: List[DetRegisTallerCreate]


class RegisTallerResponse(BaseModel):
    fecha: date
    ano_academ: int
    cod_periodo_academ: int
    sigla: str
    seccion: int
    id_taller: int
    id_usuario: int
    obs: str

    model_config = ConfigDict(from_attributes=True)