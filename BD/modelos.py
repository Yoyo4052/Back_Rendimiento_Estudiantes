from sqlalchemy import JSON, Column, Integer, String, LargeBinary, Float, Date, ForeignKey
from sqlalchemy.dialects.mysql import LONGTEXT, TEXT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Usuarios(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True, index=True)
    nickname = Column(String(50, collation='utf8mb4_bin'), unique=True)  # Hace que el nickname sea único
    correo = Column(String(200), unique=True)
    contrasena =  Column(String(1000))
    resultados = relationship("Resultados", back_populates="usuario")
    codigo = Column(Integer)
    resultadosFODA = relationship("ResultadosFODA", back_populates="usuario")

class Resultados(Base):
    __tablename__ = 'resultados'

    id = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey('usuarios.id'))
    usuario = relationship("Usuarios", back_populates="resultados")
    
    id_cuestionario = Column(Integer, ForeignKey('cuestionarios.id'))
    cuestionario = relationship("Cuestionarios", back_populates="resultados")
    resultados = Column(TEXT)

class ResultadosFODA(Base):
    __tablename__ = 'resultadosFODA'

    id = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey('usuarios.id'))
    usuario = relationship("Usuarios", back_populates="resultadosFODA")
    
    id_cuestionario = Column(Integer, ForeignKey('cuestionarios.id'))
    cuestionario = relationship("Cuestionarios", back_populates="resultadosFODA")
    resultados = Column(TEXT)

class Admin(Base):
    __tablename__ = 'admins'

    id = Column(Integer, primary_key=True, index=True)
    nickname = Column(String(50))
    contrasena =  Column(String(1000))
    pruebas = relationship("Pruebas", back_populates="admins")

class Cuestionarios(Base):
    __tablename__ = 'cuestionarios'

    id = Column(Integer, primary_key=True, index=True)
    preguntas = relationship("Preguntas", back_populates="cuestionario")
    resultados = relationship("Resultados", back_populates="cuestionario")
    resultadosFODA = relationship("ResultadosFODA", back_populates="cuestionario")
    descripcion = Column(String(500))
    pruebas = relationship("Pruebas", back_populates="cuestionario")

class Preguntas(Base):
    __tablename__ = 'preguntas'

    id = Column(Integer, primary_key=True, index=True)
    id_cuestionario = Column(Integer, ForeignKey('cuestionarios.id'))
    cuestionario = relationship("Cuestionarios", back_populates="preguntas")
    pregunta = Column(String(500))
    tipo = Column(String(150))

class Respuestas(Base):
    __tablename__ = 'respuestas'

    id = Column(Integer, primary_key=True, index=True)
    id_cuestionario = Column(Integer, ForeignKey('cuestionarios.id'))
    pregunta = Column(String(1000))
    id_usuario = Column(Integer, ForeignKey('usuarios.id'))
    ponderacion = Column(Integer)

class Respuestasprueba(Base):
    __tablename__ = 'respuestasprueba'

    id = Column(Integer, primary_key=True, index=True)
    id_cuestionario = Column(Integer)
    id_pregunta = Column(Integer)
    nickname = Column(String(50))
    ponderacion = Column(Integer)
    
class Pruebas(Base):
    __tablename__ = 'pruebas'

    id = Column(Integer, primary_key=True, index=True)
    id_admin = Column(Integer, ForeignKey('admins.id'))

    admins= relationship("Admin", back_populates="pruebas") 
    
    id_cuestionario = Column(Integer, ForeignKey('cuestionarios.id'))
    cuestionario = relationship("Cuestionarios", back_populates="pruebas")
    resultados = Column(TEXT)
    