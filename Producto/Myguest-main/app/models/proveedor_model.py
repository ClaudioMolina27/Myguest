from sqlalchemy import String, SmallInteger, ForeignKey, Boolean, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from app.database import Base


class Proveedor(Base):
    __tablename__ = "proveedor"

    id_proveedor: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nom_proveedor: Mapped[str] = mapped_column(String(100), nullable=False)
    rut: Mapped[Optional[str]] = mapped_column(String(12))
    contacto: Mapped[Optional[str]] = mapped_column(String(60))
    email: Mapped[Optional[str]] = mapped_column(String(80))
    telefono: Mapped[Optional[str]] = mapped_column(String(20))
    activo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    familias: Mapped[list["FamiliaProducto"]] = relationship(back_populates="proveedor")


class FamiliaProducto(Base):
    __tablename__ = "familia_producto"

    cod_familia: Mapped[int] = mapped_column(SmallInteger, primary_key=True)
    nom_familia: Mapped[str] = mapped_column(String(50), nullable=False)
    id_proveedor: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("proveedor.id_proveedor"))

    proveedor: Mapped[Optional["Proveedor"]] = relationship(back_populates="familias")