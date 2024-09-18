from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey

from sqlalchemy.orm import relationship 

from sqlalchemy.ext.declarative import declarative_base

#Llamado a la base para crear tabla

Base = declarative_base()

#Definicion de las tablas de mi modelo

#Usuario

class Usuario(Base):
    __tablename__='tblUsuario'
    id = Column(Integer, primery_key=True, autoincrement=True)
    strNombre = Column(String(50))
    dateFechaNacimiento = Column(Date)
    strUbicacion = Column(String(100))
    intMetaAhorro = Column(Integer)

class Gastos(Base):
    __tablename__='tblGastos'
    id = Column(Integer, primery_key=True, autoincrement=True)
    strDescripcionGastos = Column(String(100))
    strCategoriaGastos = Column(String(100))
    dateFechaGastos = Column(Date)
    intValorGastos = Column(Integer)

class Categoria(Base):
    __tablename__='tblCategoria'
    id = Column(Integer, primery_key=True, autoincrement=True)
    strNombreCategoria = Column(String(100))
    strDescripcionCategoria = Column(String(100))
    strFotoCategoria = Column(String(100))


class Ingreso(Base):
    __tablename__='tblIngreso'
    id = Column(Integer, primery_key=True, autoincrement=True)
    strDescripcionIngreso = Column(String(100))
    dateFechaIngreso = Column(Date)
    intValorIngreso = Column(Integer)

    



