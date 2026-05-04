from pydantic import BaseModel, ConfigDict
from typing import Optional


class UsuarioBase(BaseModel):
    login: str
    primer_apellido: str
    segundo_apellido: Optional[str] = None
    nom: str
    nom_preferido: Optional[str] = None
    cod_perfil: int
    cod_carrera: int


class UsuarioCreate(UsuarioBase):
    password: str


class UsuarioUpdate(BaseModel):
    primer_apellido: Optional[str] = None
    segundo_apellido: Optional[str] = None
    nom: Optional[str] = None
    nom_preferido: Optional[str] = None
    cod_perfil: Optional[int] = None
    cod_carrera: Optional[int] = None


class UsuarioResponse(UsuarioBase):
    id_usuario: int

    model_config = ConfigDict(from_attributes=True)