from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.config import get_settings

settings = get_settings()

# Motor async para PostgreSQL
engine = create_async_engine(
    settings.database_url,
    echo=settings.app_env == "development",  # logs SQL en dev
    pool_size=10,
    max_overflow=20,
)

# Fabrica de sesiones
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# Base para todos los modelos SQLAlchemy
class Base(DeclarativeBase):
    pass


# Dependencia para inyectar sesion en los routers
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
