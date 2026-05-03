from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt, JWTError

from app.database import get_db
from app.config import get_settings

settings = get_settings()
bearer_scheme = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: AsyncSession = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido o expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.secret_key,
            algorithms=[settings.algorithm]
        )
        id_usuario: str = payload.get("sub")
        if id_usuario is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    from app.services.usuario_service import get_usuario_by_id
    usuario = await get_usuario_by_id(db, int(id_usuario))
    if usuario is None:
        raise credentials_exception
    return usuario


def require_perfil(*perfiles: int):
    async def verificar(usuario=Depends(get_current_user)):
        if usuario.cod_perfil not in perfiles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permisos para realizar esta acción"
            )
        return usuario
    return verificar