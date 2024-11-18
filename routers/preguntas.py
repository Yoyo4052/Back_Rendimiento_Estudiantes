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


def get_pregunta():
    try:
        db = sessionlocal()
        yield db
    finally:
        db.close()



@router.get("/verPregunta/", response_model=List[page_schemas.PreguntaBase])
async def show_preguntas(db:session=Depends(get_pregunta)):
    pregunta = db.query(page_models.Preguntas).all()
    return pregunta

@router.post("/registrarPregunta/",response_model=page_schemas.PreguntaBase)
def create_preguntas(entrada:page_schemas.PreguntaBase,db:session=Depends(get_pregunta)):
   pregunta = page_models.Preguntas(id_cuestionario = entrada.id_cuestionario, pregunta = entrada.pregunta, tipo = entrada.tipo)
   db.add(pregunta)
   db.commit()
   db.refresh(pregunta)
   return pregunta

@router.put("/cambiarPregunta/{pregunta_id}",response_model=page_schemas.PreguntaBase)
def mod_pregunta(pregunta_id: int, entrada:page_schemas.PreguntaBase,db:session=Depends(get_pregunta)):
    pregunta = db.query(page_models.Preguntas).filter_by(id=pregunta_id).first()
    pregunta.id_cuestionario = entrada.id_cuestionario
    pregunta.pregunta = entrada.pregunta
    pregunta.tipo = entrada.tipo
    db.commit()
    db.refresh(pregunta)
    return pregunta

@router.delete("/EliminarPregunta/{pregunta_id}/",response_model=page_schemas.respuesta)
def del_pregunta(pregunta_id: int,db:session=Depends(get_pregunta)):
    pregunta = db.query(page_models.Preguntas).filter_by(id=pregunta_id).first()
    db.delete(pregunta)
    db.commit()
    respuesta = page_schemas.respuesta(mensaje="Eliminado exitosamente")
    return respuesta
