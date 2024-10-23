from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from typing import List
from fastapi.params import Depends

from app.api.DTO.dtos import usuarioDTOPeticion, usuarioDTORespuesta
from app.api.DTO.dtos import GastoDTOPeticion, GastoDTORespuesta
from app.api.DTO.dtos import CategoriaDTOPeticion, CategoriaDTORespuesta
from app.api.DTO.dtos import IngresoDTOPeticion, IngresoDTORespuesta
from app.api.DTO.dtos import AhorroDTOPeticion, AhorroDTORespuesta

from app.api.models.tablasSQL import Usuario, Gastos, Categoria, Ingreso, Ahorro
from app.database.configuration import sessionLocals, engine

rutas = APIRouter()

def connectarConBD():
    try:
        basedatos = sessionLocals()
        yield basedatos
    
    except Exception as error:
        basedatos.rollback()
        raise error
    finally:
        basedatos.close()

# Rutas

@rutas.post("/usuario", response_model=usuarioDTORespuesta, summary="registrar un usuario en la base de datos")
def guardarUsuario(datosUsuario: usuarioDTOPeticion, database: Session = Depends(connectarConBD)):
    try:
        usuario = Usuario(
            strNombre=datosUsuario.strNombre,
            dateFechaNacimiento=datosUsuario.dateFechaNacimiento,
            strUbicacion=datosUsuario.strUbicacion,
            intMetaAhorro=datosUsuario.intMetaAhorro
        )
        database.add(usuario)
        database.commit()
        database.refresh(usuario)
        return usuario
    
    except Exception as error:
        database.rollback()
        raise HTTPException(status_code=400, detail=f"Tenemos un problema {error}")

@rutas.get("/usuario", response_model=List[usuarioDTORespuesta], summary="buscar todos los usuarios en base de datos")
def buscarUsuario(database: Session = Depends(connectarConBD)):
    try:
        usuarios = database.query(Usuario).all()
        return usuarios
    except Exception as error:
        database.rollback()
        raise HTTPException(status_code=400, detail=f"No se encuentran los usuarios {error}")

@rutas.post("/gasto", response_model=GastoDTORespuesta, summary="registrar un gasto en la base de datos")
def guardarGasto(datosGasto: GastoDTOPeticion, database: Session = Depends(connectarConBD)):
    try:
        gasto = Gastos(
            strDescripcionGastos=datosGasto.strDescripcionGastos,
            strCategoriaGastos=datosGasto.strCategoriaGastos,
            dateFechaGastos=datosGasto.dateFechaGastos,
            intValorGastos=datosGasto.intValorGastos
        )
        database.add(gasto)
        database.commit()
        database.refresh(gasto)
        return gasto
    
    except Exception as error:
        database.rollback()
        raise HTTPException(status_code=400, detail=f"Tenemos un problema {error}")

@rutas.get("/gasto", response_model=List[GastoDTORespuesta], summary="buscar todos los gastos en base de datos")
def buscarGasto(database: Session = Depends(connectarConBD)):
    try:
        gastos = database.query(Gastos).all()  # Cambiar Usuario por Gastos
        return gastos
    except Exception as error:
        database.rollback()
        raise HTTPException(status_code=400, detail=f"No se encuentran los gastos {error}")

@rutas.post("/categoria", response_model=CategoriaDTORespuesta, summary="Registrar una nueva categoría")
def guardarCategoria(datosCategoria: CategoriaDTOPeticion, database: Session = Depends(connectarConBD)):
    try:
        categoria = Categoria(
            strNombreCategoria=datosCategoria.strNombreCategoria,
            strDescripcionCategoria=datosCategoria.strDescripcionCategoria,
            strFotoCategoria=datosCategoria.strFotoCategoria
        )
        database.add(categoria)
        database.commit()
        database.refresh(categoria)
        return categoria
    except Exception as error:
        database.rollback()
        raise HTTPException(status_code=400, detail=f"Error al registrar la categoría: {error}")

@rutas.get("/categorias", response_model=List[CategoriaDTORespuesta], summary="Obtener todas las categorías")
def obtenerCategorias(database: Session = Depends(connectarConBD)):
    try:
        categorias = database.query(Categoria).all()
        return categorias
    except Exception as error:
        database.rollback()
        raise HTTPException(status_code=400, detail=f"Error al obtener las categorías: {error}")

@rutas.post("/ingreso", response_model=IngresoDTORespuesta, summary="Registrar un nuevo ingreso")
def guardarIngreso(datosIngreso: IngresoDTOPeticion, database: Session = Depends(connectarConBD)):
    try:
        ingreso = Ingreso(
            strDescripcionIngreso=datosIngreso.strDescripcionIngreso,
            dateFechaIngreso=datosIngreso.dateFechaIngreso,
            intValorIngreso=datosIngreso.intValorIngreso
        )
        database.add(ingreso)
        database.commit()
        database.refresh(ingreso)
        return ingreso
    except Exception as error:
        database.rollback()
        raise HTTPException(status_code=400, detail=f"Error al registrar el ingreso: {error}")

@rutas.get("/ingresos", response_model=List[IngresoDTORespuesta], summary="Obtener todos los ingresos")
def obtenerIngresos(database: Session = Depends(connectarConBD)):
    try:
        ingresos = database.query(Ingreso).all()
        return ingresos
    except Exception as error:
        database.rollback()
        raise HTTPException(status_code=400, detail=f"Error al obtener los ingresos: {error}")

@rutas.post("/ahorro", response_model=AhorroDTORespuesta, summary="Registrar un nuevo ahorro")
def guardarAhorro(datosAhorro: AhorroDTOPeticion, database: Session = Depends(connectarConBD)):
    try:
        ahorro = Ahorro(
            strConceptoAhorro=datosAhorro.strConceptoAhorro,
            dateFechaAhorro=datosAhorro.dateFechaAhorro,
            intValorAhorro=datosAhorro.intValorAhorro
        )
        database.add(ahorro)
        database.commit()
        database.refresh(ahorro)
        return ahorro
    except Exception as error:
        database.rollback()
        raise HTTPException(status_code=400, detail=f"Error al registrar el ahorro: {error}")

@rutas.get("/ahorros", response_model=List[AhorroDTORespuesta], summary="Obtener todos los ahorros")
def obtenerAhorros(database: Session = Depends(connectarConBD)):
    try:
        ahorros = database.query(Ahorro).all()
        return ahorros
    except Exception as error:
        database.rollback()
        raise HTTPException(status_code=400, detail=f"Error al obtener los ahorros: {error}")
