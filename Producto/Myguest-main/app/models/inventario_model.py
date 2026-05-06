from sqlalchemy import String, SmallInteger, ForeignKey, Numeric, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from app.database import Base


class CategoriaProducto(Base):
    __tablename__ = "categ_producto"

    cod_categ_producto: Mapped[int] = mapped_column(SmallInteger, primary_key=True)
    nom_categ_producto: Mapped[str] = mapped_column(String(30), nullable=False)

    productos: Mapped[list["Producto"]] = relationship(back_populates="categoria")


class UnidadMedida(Base):
    __tablename__ = "unidad_medida"

    cod_unidad_medida: Mapped[int] = mapped_column(SmallInteger, primary_key=True)
    nom_unidad_medida: Mapped[str] = mapped_column(String(20), nullable=False)
    nom_unidad_medida_abrev: Mapped[str] = mapped_column(String(12), nullable=False)
    cod_unidad_medida_base: Mapped[Optional[int]] = mapped_column(SmallInteger, ForeignKey("unidad_medida.cod_unidad_medida"))
    factor: Mapped[Optional[float]] = mapped_column(Numeric(6, 2))

    productos: Mapped[list["Producto"]] = relationship(back_populates="unidad_medida")


class Producto(Base):
    __tablename__ = "producto"

    id_producto: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nom_producto: Mapped[str] = mapped_column(String(100), nullable=False)
    precio: Mapped[int] = mapped_column(Integer, nullable=False)
    cod_unidad_medida: Mapped[int] = mapped_column(SmallInteger, ForeignKey("unidad_medida.cod_unidad_medida"), nullable=False)
    cod_categ_producto: Mapped[int] = mapped_column(SmallInteger, ForeignKey("categ_producto.cod_categ_producto"), nullable=False)
    cod_familia: Mapped[Optional[int]] = mapped_column(SmallInteger, nullable=True)

    categoria: Mapped["CategoriaProducto"] = relationship(back_populates="productos")
    unidad_medida: Mapped["UnidadMedida"] = relationship(back_populates="productos")
    inventario: Mapped[Optional["Inventario"]] = relationship(back_populates="producto")


class Inventario(Base):
    __tablename__ = "inventario"

    id_producto: Mapped[int] = mapped_column(Integer, ForeignKey("producto.id_producto"), primary_key=True)
    stock_actual: Mapped[float] = mapped_column(Numeric(12, 6), nullable=False, default=0)
    stock_minimo: Mapped[float] = mapped_column(Numeric(12, 6), nullable=False, default=0)

    producto: Mapped["Producto"] = relationship(back_populates="inventario")