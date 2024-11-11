from fastapi import APIRouter, Request ,HTTPException, status
from fastapi.responses import JSONResponse
from typing import List
from starlette.responses import RedirectResponse
from sqlalchemy.orm import session
from fastapi.params import Depends

from BD.Connn import engine, sessionlocal
import BD.schemas as page_schemas
import BD.Connn as page_conexion
import BD.modelos as page_models
from geminiAPI import prompt_gen


page_models.Base.metadata.create_all(bind=engine)
router = APIRouter()

def get_respuestasprueba():
    try:
        db = sessionlocal()
        yield db
    finally:
        db.close()



@router.get("/VerRespuestaspruebaPorNickname/{Nickname}")
async def VER_Res_nickname(Nickname: str,db:session=Depends(get_respuestasprueba)):
    pruebas = db.query(page_models.Respuestasprueba).filter_by(nickname=Nickname).first()
    return pruebas

@router.get("/geminiprueba/{Cuestionario_id}/{Nickname}")
async def gemini_AI_prueba(idcuestionario: int, Nickname: str,db:session=Depends(get_respuestasprueba)):
    
    # Seleccionar solo las columnas de preguntas y ponderación
    preguntas = db.query(page_models.Preguntas.pregunta).filter_by(id_cuestionario=idcuestionario).all()
    pruebas = db.query(page_models.Respuestasprueba.ponderacion).filter_by(id_cuestionario=idcuestionario, nickname=Nickname).all()
    if not preguntas and not pruebas: raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="no se pudo encontrar preguntas y/o respuestas")
    
    # Devolver las columnas en un formato adecuado
    data = {"preguntas": [pregunta[0] for pregunta in preguntas], "ponderaciones": [prueba[0] for prueba in pruebas]}
    prompt = "De estas preguntas y respuestas ayudame a predecir el rendimiento academico, las respuestas son del 1-5"
    respuesta = prompt_gen(prompt, data)
    res = page_models.Pruebas(admin=Nickname, id_cuestionario=idcuestionario, resultados=respuesta)
    if not res: raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="no se pudo guardar el resultado")
    db.add(res)
    db.commit()
    db.refresh(res)
    return respuesta

@router.get("/verRespuestaspruebas/", response_model=List[page_schemas.respuestasprueba])
async def show_Respuestaspruebas(db:session=Depends(get_respuestasprueba)):
    prueba = db.query(page_models.Respuestasprueba).all()
    return prueba

@router.post("/registrarRespuestasprueba/",response_model=page_schemas.respuestasprueba)
def create_respuestasprueba(entrada:page_schemas.respuestasprueba,db:session=Depends(get_respuestasprueba)):
   pruebas = page_models.Respuestasprueba(id_cuestionario = entrada.id_cuestionario, id_pregunta = entrada.id_pregunta, 
                                       nickname = entrada.nickname, ponderacion = entrada.ponderacion)
   db.add(pruebas)
   db.commit()
   db.refresh(pruebas)
   return pruebas

@router.put("/CambiarRespuestasprueba/{Respuesta_id}",response_model=page_schemas.respuestasprueba)
def mod_respuestasprueba(respuestasid: int, entrada:page_schemas.respuestasprueba,db:session=Depends(get_respuestasprueba)):
    prueba = db.query(page_models.Respuestasprueba).filter_by(id=respuestasid).first()
    prueba.id_cuestionario = entrada.id_cuestionario 
    prueba.id_pregunta = entrada.id_pregunta
    prueba.nickname = entrada.nickname
    prueba.ponderacion = entrada.ponderacion
    db.commit()
    db.refresh(prueba)
    return prueba

@router.put("/CambiarRespuestaprueba/{Id_respuesta}",response_model=page_schemas.cambiarRespuestasprueba)
def mod_RespuestasUsuarioprueba(idrespuesta: int, entrada:page_schemas.cambiarRespuestasprueba,db:session=Depends(get_respuestasprueba)):
    prueba = db.query(page_models.Respuestasprueba).filter_by(id=idrespuesta).first()
    prueba.ponderacion = entrada.ponderacion
    db.commit()
    db.refresh(prueba)
    return prueba

@router.delete("/EliminarRespuestasprueba/{respuestas_id}",response_model=page_schemas.respuesta)
def del_respuestasprueba(respuestasid: int,db:session=Depends(get_respuestasprueba)):
    prueba = db.query(page_models.Respuestasprueba).filter_by(id=respuestasid).first()
    db.delete(prueba)
    db.commit()
    respuesta = page_schemas.respuesta(mensaje="Eliminado exitosamente")
    return respuesta