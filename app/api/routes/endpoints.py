from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from typing import List
from fastapi.params import Depends

from app.api.DTO.dtos import usuarioDTOPeticion, usuarioDTORespuesta
from app.api.DTO.dtos import GastoDTOPeticion, GastoDTORespuesta
from app.api.DTO.dtos import CategoriaDTOPeticion, CategoriaDTORespuesta
from app.api.DTO.dtos import IngresoDTOPeticion, IngresoDTORespuesta
from app.api.DTO.dtos import AhorroDTOPeticion, AhorroDTORespuesta
from app.api.DTO.dtos import LoginCredentials

from app.api.models.tablasSQL import Usuario, Gastos, Categoria, Ingreso, Ahorro
from app.database.configuration import sessionLocals, engine
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer


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

#Define funciones para manejar contraseñas y tokens:

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


#Verificar el token en endpoints protegidos

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme), database: Session = Depends(connectarConBD)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("usuario_id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Token inválido")
        usuario = database.query(Usuario).filter(Usuario.id == user_id).first()
        if not usuario:
            raise HTTPException(status_code=401, detail="Usuario no encontrado")
        return usuario
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")


# Configuración de hashing de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Claves para el manejo de JWT
SECRET_KEY = "Sabu"  # Cambia esto por un valor aleatorio y seguro
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


#Endpoint para inicio de sesion

@rutas.post("/login", summary="Iniciar sesión con correo y contraseña")
def iniciar_sesion(credentials: LoginCredentials, database: Session = Depends(connectarConBD)):
    usuario = database.query(Usuario).filter(Usuario.strEmail == credentials.email).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    if not verify_password(credentials.password, usuario.strContraseña):
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")
    
    # Crear token de acceso
    access_token = create_access_token(
        data={"usuario_id": usuario.id, "email": usuario.strEmail},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}


@rutas.post("/usuario", response_model=usuarioDTORespuesta, summary="Registrar un usuario")
def guardarUsuario(datosUsuario: usuarioDTOPeticion, database: Session = Depends(connectarConBD)):
    try:
        # Verificar si el correo ya está registrado
        usuario_existente = database.query(Usuario).filter(Usuario.strEmail == datosUsuario.strEmail).first()
        if usuario_existente:
            raise HTTPException(status_code=400, detail="El correo ya está registrado.")
        
        usuario = Usuario(
            strNombre=datosUsuario.strNombre,
            dateFechaNacimiento=datosUsuario.dateFechaNacimiento,
            strUbicacion=datosUsuario.strUbicacion,
            intMetaAhorro=datosUsuario.intMetaAhorro,
            strEmail=datosUsuario.strEmail,
            strContraseña=hash_password(datosUsuario.strContraseña),  # Guardar contraseña hasheada
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
    if datosGasto.intValorGastos <= 0:
        raise HTTPException(status_code=400, detail="El valor del gasto debe ser mayor a cero.")
    
    try:
        gasto = Gastos(
            strDescripcionGastos=datosGasto.strDescripcionGastos,
            strCategoriaGastos=datosGasto.strCategoriaGastos,
            dateFechaGastos=datosGasto.dateFechaGastos,
            intValorGastos=datosGasto.intValorGastos,
        )
        database.add(gasto)
        database.commit()
        database.refresh(gasto)
        return gasto
    except Exception as error:
        database.rollback()
        raise HTTPException(status_code=400, detail=f"Error al registrar el gasto: {error}")


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
    print("Datos recibidos en el backend:", datosIngreso)
    try:
        # Crea el ingreso
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
        raise HTTPException(status_code=400, detail=f"Error al registrar el ingreso: {str(error)}")


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
    
