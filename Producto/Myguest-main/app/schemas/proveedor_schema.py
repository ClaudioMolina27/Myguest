from pydantic import BaseModel, ConfigDict
from typing import Optional


class ProveedorCreate(BaseModel):
    nom_proveedor: str
    rut: Optional[str] = None
    contacto: Optional[str] = None
    email: Optional[str] = None
    telefono: Optional[str] = None


class ProveedorUpdate(BaseModel):
    nom_proveedor: Optional[str] = None
    rut: Optional[str] = None
    contacto: Optional[str] = None
    email: Optional[str] = None
    telefono: Optional[str] = None
    activo: Optional[bool] = None


class ProveedorResponse(BaseModel):
    id_proveedor: int
    nom_proveedor: str
    rut: Optional[str] = None
    contacto: Optional[str] = None
    email: Optional[str] = None
    telefono: Optional[str] = None
    activo: bool

    model_config = ConfigDict(from_attributes=True)


class FamiliaCreate(BaseModel):
    cod_familia: int
    nom_familia: str
    id_proveedor: Optional[int] = None


class FamiliaUpdate(BaseModel):
    nom_familia: Optional[str] = None
    id_proveedor: Optional[int] = None


class FamiliaResponse(BaseModel):
    cod_familia: int
    nom_familia: str
    id_proveedor: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)