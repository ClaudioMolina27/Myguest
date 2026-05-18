from sqlalchemy import String, SmallInteger, ForeignKey, Date, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from datetime import date
from app.database import Base


class Carrera(Base):
    __tablename__ = "carrera"

    cod_carrera: Mapped[int] = mapped_column(SmallInteger, primary_key=True)
    nom_carrera: Mapped[str] = mapped_column(String(30), nullable=False)
    nom_carrera_abrev: Mapped[Optional[str]] = mapped_column(String(10))


class Asignatura(Base):
    __tablename__ = "asign"

    sigla: Mapped[str] = mapped_column(String(15), primary_key=True)
    nom_asign: Mapped[str] = mapped_column(String(50), nullable=False)
    nom_asign_abrev: Mapped[str] = mapped_column(String(30), nullable=False)
    cod_carrera: Mapped[int] = mapped_column(SmallInteger, ForeignKey("carrera.cod_carrera"), nullable=False)


class Taller(Base):
    __tablename__ = "taller"

    id_taller: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    titulo_preparacion: Mapped[Optional[str]] = mapped_column(String(100))
    detalle_preparacion: Mapped[Optional[str]] = mapped_column(String(2000))
    semana: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    sigla: Mapped[str] = mapped_column(String(15), ForeignKey("asign.sigla"), nullable=False)
    jornada: Mapped[Optional[str]] = mapped_column(String(6), default="manana")


class PeriodoAcadem(Base):
    __tablename__ = "periodo_academ"

    cod_periodo_academ: Mapped[int] = mapped_column(SmallInteger, primary_key=True)
    nom_periodo_academ: Mapped[str] = mapped_column(String(30), nullable=False)
    nom_periodo_academ_abrev: Mapped[str] = mapped_column(String(12), nullable=False)


class ProgAsign(Base):
    __tablename__ = "prog_asign"

    ano_academ: Mapped[int] = mapped_column(SmallInteger, primary_key=True)
    cod_periodo_academ: Mapped[int] = mapped_column(SmallInteger, ForeignKey("periodo_academ.cod_periodo_academ"), primary_key=True)
    sigla: Mapped[str] = mapped_column(String(15), ForeignKey("asign.sigla"), primary_key=True)
    seccion: Mapped[int] = mapped_column(SmallInteger, primary_key=True)


class ProgTaller(Base):
    __tablename__ = "prog_taller"

    fecha: Mapped[date] = mapped_column(Date, primary_key=True)
    ano_academ: Mapped[int] = mapped_column(SmallInteger, primary_key=True)
    cod_periodo_academ: Mapped[int] = mapped_column(SmallInteger, primary_key=True)
    sigla: Mapped[str] = mapped_column(String(15), primary_key=True)
    seccion: Mapped[int] = mapped_column(SmallInteger, primary_key=True)
    id_taller: Mapped[int] = mapped_column(Integer, ForeignKey("taller.id_taller"), primary_key=True)
    id_usuario: Mapped[int] = mapped_column(Integer, ForeignKey("usuario.id_usuario"), nullable=False)


class RegisTaller(Base):
    __tablename__ = "regis_taller"

    fecha: Mapped[date] = mapped_column(Date, primary_key=True)
    ano_academ: Mapped[int] = mapped_column(SmallInteger, primary_key=True)
    cod_periodo_academ: Mapped[int] = mapped_column(SmallInteger, primary_key=True)
    sigla: Mapped[str] = mapped_column(String(15), primary_key=True)
    seccion: Mapped[int] = mapped_column(SmallInteger, primary_key=True)
    id_taller: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_usuario: Mapped[int] = mapped_column(Integer, ForeignKey("usuario.id_usuario"), nullable=False)
    obs: Mapped[str] = mapped_column(String(500), nullable=False, default="Sin observaciones")


class DetRegisTaller(Base):
    __tablename__ = "det_regis_taller"

    fecha: Mapped[date] = mapped_column(Date, primary_key=True)
    ano_academ: Mapped[int] = mapped_column(SmallInteger, primary_key=True)
    cod_periodo_academ: Mapped[int] = mapped_column(SmallInteger, primary_key=True)
    sigla: Mapped[str] = mapped_column(String(15), primary_key=True)
    seccion: Mapped[int] = mapped_column(SmallInteger, primary_key=True)
    id_producto: Mapped[int] = mapped_column(Integer, ForeignKey("producto.id_producto"), primary_key=True)
    id_taller: Mapped[int] = mapped_column(Integer, primary_key=True)
    cod_agrupador: Mapped[int] = mapped_column(SmallInteger, primary_key=True)
    precio: Mapped[int] = mapped_column(Integer, primary_key=True)
    cantidad: Mapped[float] = mapped_column(Numeric(12, 6), nullable=False)