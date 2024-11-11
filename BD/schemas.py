from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class ResultadosBase(BaseModel):
    resultados: str

class ResultadosCreate(ResultadosBase):
    id_usuario: int
    id_cuestionario: int

class Resultados(ResultadosBase):
    id: int
    id_usuario: int
    id_cuestionario: int
    
    class Config:
        from_atributtes = True

class ResultadosFODABase(BaseModel):
    resultados: str

class ResultadosFODACreate(ResultadosFODABase):
    id_usuario: int
    id_cuestionario: int

class ResultadosFODA(ResultadosFODABase):
    id: int
    id_usuario: int
    id_cuestionario: int
    
    class Config:
        from_atributtes = True

class User(BaseModel):
     id: Optional[int] = None
     nickname: str
     correo: str
     contrasena: str
     resultados: Optional[List[Resultados]] = []
     codigo: int
     resultadosFODA: Optional[List[ResultadosFODA]] = []

     class Config:
       from_attributes = True

class Admin(BaseModel):
     id: Optional[int] = None
     nickname: str
     contrasena: str

     class Config:
       from_attributes = True

class ModificarUsernameAdmin(BaseModel):
     nickname: str

     class Config:
       from_attributes = True

class ModificarPassWordAdmin(BaseModel):
     contrasena: str

     class Config:
       from_attributes = True

class RegisterUser(BaseModel):
     id: Optional[int] = None
     nickname: str
     correo: str
     contrasena: str
     codigo: int

     class Config:
       from_attributes = True

class ModificarUser(BaseModel):
     id: Optional[int] = None
     nickname: str
     correo: str

     class Config:
       from_attributes = True

class Modificarcontrasena(BaseModel):
     contrasena: str

     class Config:
       from_attributes = True

class PreguntaBase(BaseModel):
    id: Optional[int] = None
    id_cuestionario: int
    pregunta: str
    tipo: str
    
class CuestionarioCreate(BaseModel):
    descripcion: str

class CuestionarioBase(CuestionarioCreate):
    preguntas: List[PreguntaBase]

class Cuestionario(CuestionarioBase):
    id: int
    resultados: Optional[List[Resultados]] = []
    class Config:
        from_attributes = True  

class respuestas(BaseModel):
     id: Optional[int] = None
     id_cuestionario: int
     pregunta: str
     id_usuario: int
     ponderacion: int

     class Config:
         from_attributes = True

class cambiarRespuestas(BaseModel):
     respuesta: str

     class Config:
         from_attributes = True
       
class respuesta(BaseModel):
     mensaje: str

class respuestasprueba(BaseModel):
     id: Optional[int] = None
     id_cuestionario: int
     id_pregunta: int
     nickname: str
     ponderacion: int

     class Config:
         from_attributes = True

class cambiarRespuestasprueba(BaseModel):
     ponderacion: int

     class Config:
         from_attributes = True         

class PruebasBase(BaseModel):
    resultados: str

class PruebasCreate(PruebasBase):
    id_admin: int
    id_cuestionario: int

class Pruebas(PruebasBase):
    id: int
    id_admin: int
    id_cuestionario: int
    
    class Config:
        from_atributtes = True
