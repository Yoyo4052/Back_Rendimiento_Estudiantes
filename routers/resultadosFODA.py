from fastapi import APIRouter,HTTPException
from typing import List
from starlette.responses import RedirectResponse
from sqlalchemy.orm import session
from fastapi.params import Depends
from BD.Connn import engine, sessionlocal
import BD.schemas as page_schemas
import BD.Connn as page_conexion
import BD.modelos as page_models

page_models.Base.metadata.create_all(bind=engine)
router = APIRouter()

def get_resultadosFODA():
    try:
        db = sessionlocal()
        yield db
    finally:
        db.close()


@router.get("/verResultadosFODA/", response_model=List[page_schemas.ResultadosFODA])
async def show_ResultadoFODA(db:session=Depends(get_resultadosFODA)):
    resultado = db.query(page_models.ResultadosFODA).all()
    return resultado

@router.get("/verResultadosFODA/{id_usuario}/", response_model=List[page_schemas.ResultadosFODA])
async def show_ResultadoFODA_por_usuario(id_usuario: int, db: session = Depends(get_resultadosFODA)):
    resultados = db.query(page_models.ResultadosFODA).filter(page_models.ResultadosFODA.id_usuario == id_usuario).all()
    if not resultados:
        raise HTTPException(status_code=404, detail="No results found for this user")
    return resultados

@router.post("/registrarResultadoFODA/", response_model=page_schemas.ResultadosFODA)
def create_resultadoFODA(entrada: page_schemas.ResultadosFODACreate, db: session = Depends(get_resultadosFODA)):
    # Crea un nuevo resultado en la base de datos
    nuevo_resultado = page_models.ResultadosFODA(resultados=entrada.resultados)
    nuevo_resultado.id_usuario = entrada.id_usuario
    nuevo_resultado.id_cuestionario = entrada.id_cuestionario
    db.add(nuevo_resultado)
    db.commit()
    db.refresh(nuevo_resultado)

    return nuevo_resultado

@router.put("/CambiarResultadoFODA/{resultado_id}",response_model=page_schemas.ResultadosFODABase)
def mod_resultadoFODA(resultado_id: int, entrada:page_schemas.ResultadosFODABase,db:session=Depends(get_resultadosFODA)):
    resultado = db.query(page_models.ResultadosFODA).filter_by(id=resultado_id).first()
    resultado.resultados = entrada.resultados
    db.commit()
    db.refresh(resultado)
    return resultado

@router.delete("/EliminarResultadoFODA/{resultado_id}",response_model=page_schemas.respuesta)
def del_resultadoFODA(resultado_id: int,db:session=Depends(get_resultadosFODA)):
    resultado = db.query(page_models.ResultadosFODA).filter_by(id=resultado_id).first()
    db.delete(resultado)
    db.commit()
    respuesta = page_schemas.respuesta(mensaje="Eliminado exitosamente")
    return respuesta