from sqlalchemy import String, SmallInteger, ForeignKey, Date, Integer, Numeric, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from datetime import date, datetime
from app.database import Base


class Factura(Base):
    __tablename__ = "factura"

    id_factura: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    num_documento: Mapped[str] = mapped_column(String(20), nullable=False)
    fecha_emision: Mapped[date] = mapped_column(Date, nullable=False)
    fecha_ingreso: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    id_proveedor: Mapped[int] = mapped_column(Integer, ForeignKey("proveedor.id_proveedor"), nullable=False)
    id_orden_compra: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    id_usuario: Mapped[int] = mapped_column(Integer, ForeignKey("usuario.id_usuario"), nullable=False)
    estado_conciliacion: Mapped[str] = mapped_column(String(20), nullable=False, default="pendiente")
    obs: Mapped[Optional[str]] = mapped_column(String(500))

    detalles: Mapped[list["DetFactura"]] = relationship(back_populates="factura", cascade="all, delete-orphan")


class DetFactura(Base):
    __tablename__ = "det_factura"

    id_factura: Mapped[int] = mapped_column(Integer, ForeignKey("factura.id_factura"), primary_key=True)
    id_producto: Mapped[int] = mapped_column(Integer, ForeignKey("producto.id_producto"), primary_key=True)
    cantidad: Mapped[float] = mapped_column(Numeric(12, 6), nullable=False)
    precio_unitario: Mapped[int] = mapped_column(Integer, nullable=False)
    fecha_vencimiento: Mapped[Optional[date]] = mapped_column(Date)

    factura: Mapped["Factura"] = relationship(back_populates="detalles")