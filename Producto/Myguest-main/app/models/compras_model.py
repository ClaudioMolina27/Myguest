from sqlalchemy import String, ForeignKey, Date, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from datetime import date
from app.database import Base


class OrdenCompra(Base):
    __tablename__ = "orden_compra"

    id_orden_compra: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    fecha_emision: Mapped[date] = mapped_column(Date, nullable=False)
    fecha_entrega_est: Mapped[date] = mapped_column(Date, nullable=False)
    id_proveedor: Mapped[int] = mapped_column(Integer, ForeignKey("proveedor.id_proveedor"), nullable=False)
    id_usuario: Mapped[int] = mapped_column(Integer, ForeignKey("usuario.id_usuario"), nullable=False)
    estado: Mapped[str] = mapped_column(String(20), nullable=False, default="borrador")
    obs: Mapped[Optional[str]] = mapped_column(String(500))

    detalles: Mapped[list["DetOrdenCompra"]] = relationship(back_populates="orden_compra", cascade="all, delete-orphan")


class DetOrdenCompra(Base):
    __tablename__ = "det_orden_compra"

    id_orden_compra: Mapped[int] = mapped_column(Integer, ForeignKey("orden_compra.id_orden_compra"), primary_key=True)
    id_producto: Mapped[int] = mapped_column(Integer, ForeignKey("producto.id_producto"), primary_key=True)
    cantidad: Mapped[float] = mapped_column(Numeric(12, 6), nullable=False)
    precio_unitario: Mapped[int] = mapped_column(Integer, nullable=False)

    orden_compra: Mapped["OrdenCompra"] = relationship(back_populates="detalles")