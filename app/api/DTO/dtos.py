from pydantic import BaseModel, Field, EmailStr
from datetime import date

#Los DTO son clases que establecen el modelo de transferencia de datos
class LoginCredentials(BaseModel):
    email: str
    password: str

class usuarioDTOPeticion(BaseModel):
    strNombre: str
    dateFechaNacimiento: date
    strUbicacion: str
    intMetaAhorro: int = Field(..., gt=0)
    strEmail: EmailStr  # Validación básica para un email correcto
    strContraseña: str
    
    class Config:
        from_attributes = True  # Actualizado para Pydantic V2

class usuarioDTORespuesta(BaseModel):
    id: int
    strNombre: str
    intMetaAhorro: int
    
    class Config:
        from_attributes = True  # Actualizado para Pydantic V2

class GastoDTOPeticion(BaseModel):
    strDescripcionGastos: str
    strCategoriaGastos: str
    dateFechaGastos: date
    intValorGastos: int = Field(..., gt=0)
    
    class Config:
        from_attributes = True  # Actualizado para Pydantic V2

class GastoDTORespuesta(BaseModel):
    id: int
    strDescripcionGastos: str
    strCategoriaGastos: str
    dateFechaGastos: date
    intValorGastos: int
    
    class Config:
        from_attributes = True  # Actualizado para Pydantic V2

class CategoriaDTOPeticion(BaseModel):
    strNombreCategoria: str
    strDescripcionCategoria: str
    strFotoCategoria: str
    
    class Config:
        from_attributes = True  # Actualizado para Pydantic V2

class CategoriaDTORespuesta(BaseModel):
    id: int
    strNombreCategoria: str
    strDescripcionCategoria: str
    strFotoCategoria: str
    
    class Config:
        from_attributes = True  # Actualizado para Pydantic V2

class IngresoDTOPeticion(BaseModel):
    strDescripcionIngreso: str
    dateFechaIngreso: date
    intValorIngreso: int = Field(..., gt=0)
    
    class Config:
        from_attributes = True  # Actualizado para Pydantic V2

class IngresoDTORespuesta(BaseModel):
    id: int
    strDescripcionIngreso: str
    dateFechaIngreso: date
    intValorIngreso: int
    
    class Config:
        from_attributes = True  # Actualizado para Pydantic V2

class AhorroDTOPeticion(BaseModel):
    strConceptoAhorro: str
    dateFechaAhorro: date
    intValorAhorro: int = Field(..., gt=0)
    
    class Config:
        from_attributes = True  # Actualizado para Pydantic V2

class AhorroDTORespuesta(BaseModel):
    id: int
    strConceptoAhorro: str
    dateFechaAhorro: date
    intValorAhorro: int
    
    class Config:
        from_attributes = True  # Actualizado para Pydantic V2
