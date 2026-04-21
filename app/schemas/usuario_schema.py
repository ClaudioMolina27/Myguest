from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional

# Esquema base compartido
class UsuarioBase(BaseModel):
    rut: str
    nombre_completo: str
    email: EmailStr
    id_perfil: int
    activo: bool = True

# Esquema para recibir datos al crear (incluye la contraseña en texto plano)
class UsuarioCreate(UsuarioBase):
    password: str

# Esquema para responder al frontend (nunca incluye la contraseña)
class UsuarioResponse(UsuarioBase):
    id_usuario: int

    # Permite a Pydantic leer directamente del modelo SQLAlchemy
    model_config = ConfigDict(from_attributes=True)