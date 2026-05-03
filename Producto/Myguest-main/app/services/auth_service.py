from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta, timezone
from jose import jwt

from app.services.usuario_service import get_usuario_by_login
from app.utils.security import verify_password
from app.config import get_settings

settings = get_settings()


async def authenticate_usuario(db: AsyncSession, login: str, password: str):
    usuario = await get_usuario_by_login(db, login)
    if not usuario:
        return None
    if not verify_password(password, usuario.hash_password):
        return None
    return usuario


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)