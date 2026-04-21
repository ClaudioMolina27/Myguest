from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.usuario_model import Usuario
from app.schemas.usuario_schema import UsuarioCreate
from app.utils.security import get_password_hash

async def get_usuario_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(Usuario).where(Usuario.email == email))
    return result.scalars().first()

async def create_usuario(db: AsyncSession, usuario_in: UsuarioCreate):
    # Encriptamos la contraseña antes de guardar
    hashed_password = get_password_hash(usuario_in.password)
    
    # Mapeamos los datos al modelo SQLAlchemy
    nuevo_usuario = Usuario(
        rut=usuario_in.rut,
        nombre_completo=usuario_in.nombre_completo,
        email=usuario_in.email,
        password_hash=hashed_password,
        id_perfil=usuario_in.id_perfil,
        activo=usuario_in.activo
    )
    
    db.add(nuevo_usuario)
    await db.commit()
    await db.refresh(nuevo_usuario) # Recargamos para obtener el id_usuario generado
    
    return nuevo_usuario

async def get_usuarios(db: AsyncSession):
    result = await db.execute(select(Usuario))
    return result.scalars().all()