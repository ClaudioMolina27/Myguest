from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.database import get_db # Tu dependencia que inyecta la AsyncSession
from app.schemas.usuario_schema import UsuarioCreate, UsuarioResponse
from app.services import usuario_service

router = APIRouter()

@router.post("/", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
async def registrar_usuario(usuario: UsuarioCreate, db: AsyncSession = Depends(get_db)):
    # Validar que el correo no exista
    db_user = await usuario_service.get_usuario_by_email(db, email=usuario.email)
    if db_user:
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    
    return await usuario_service.create_usuario(db, usuario)

@router.get("/", response_model=List[UsuarioResponse])
async def listar_usuarios(db: AsyncSession = Depends(get_db)):
    return await usuario_service.get_usuarios(db)