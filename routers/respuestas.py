from fastapi import APIRouter, Request ,HTTPException
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


def get_respuestas():
    try:
        db = sessionlocal()
        yield db
    finally:
        db.close()



@router.get("/gemini/{id_usuario}")
async def gemini_AI(id_usuario: int, db: session = Depends(get_respuestas)):
    # Seleccionar solo las columnas de preguntas y ponderación para el usuario especificado
    respuestas = db.query(page_models.Respuestas).filter(page_models.Respuestas.id_usuario == id_usuario).all()

    # Extraer las preguntas y ponderaciones
    preguntas = [respuesta.pregunta for respuesta in respuestas]
    ponderaciones = [respuesta.ponderacion for respuesta in respuestas]

    # Devolver las columnas en un formato adecuado
    data = {"preguntas": preguntas, "ponderaciones": ponderaciones}

    prompt = '''Por favor, realiza un análisis de rendimiento escolar, una predicción de rendimiento a futuro y proporciona recomendaciones para el usuario basado en las respuestas que te enviaré a continuación. Las respuestas tienen una ponderación del 1 al 5, donde 1 es la calificación más baja y 5 es la más alta.
            Intenta ser lo más extenso y específico posible.
            Tanto en el punto de "Analisis de rendimiento" como en "Prediccion de rendimiento a futuro" necesito una conclusión lo más extensa posible, con respuesta específica y no tan general.
            En el punto de "Recomendaciones" desglosa tu respuesta, e intenta explicar y sobretodo dar ejemplos de como aplicar cada una de esas recomendaciones que sugieres.
            Formato de Respuesta:
            Análisis de Rendimiento (asegurate de escribir exacta y literalmente el nombre de sección como Análisis de Rendimiento, con las tildes adecuadas y mayúsculas necesarias. No uses ":" en el nombre de sección, solo haz un salto de línea)
            [Ponga aquí detalles del análisis de rendimiento]

            Predicción de Rendimiento a Futuro (asegurate de escribir exacta y literalmente el nombre de sección como Predicción de Rendimiento a Futuro, con las tildes adecuadas y mayúsculas necesarias. No uses ":" en el nombre de sección, solo haz un salto de línea)
            [Ponga aquí su predicción de rendimiento a futuro]

            Recomendaciones (asegurate de escribir exacta y literalmente el nombre de sección como Recomendaciones, con las tildes adecuadas y mayúsculas necesarias. No uses ":" en el nombre de sección, solo haz un salto de línea)
            [Ponga aquí las recomendaciones para el usuario]'''

    generated_text = prompt_gen(prompt, data)

    # Crear una nueva entrada en la tabla resultados
    nuevo_resultado = page_models.Resultados(
        id_usuario=id_usuario,
        id_cuestionario=6,  # Asumiendo que todas las respuestas pertenecen al mismo cuestionario
        resultados=generated_text
    )

    # Añadir y guardar los cambios en la base de datos
    db.add(nuevo_resultado)
    db.commit()
    db.refresh(nuevo_resultado)

    return generated_text

@router.get("/verRespuestas/", response_model=List[page_schemas.respuestas])
async def show_Respuestas(db:session=Depends(get_respuestas)):
    respuesta = db.query(page_models.Respuestas).all()
    return respuesta

@router.post("/registrarRespuestas/",response_model=page_schemas.respuestas)
def create_respuestas(entrada:page_schemas.respuestas,db:session=Depends(get_respuestas)):
   # Verificar si la respuesta ya existe
    respuesta_existente = db.query(page_models.Respuestas).filter(
        page_models.Respuestas.id_usuario == entrada.id_usuario,
        page_models.Respuestas.id_cuestionario == entrada.id_cuestionario,
        page_models.Respuestas.pregunta == entrada.pregunta
    ).first()

    if respuesta_existente:
        # Actualizar la respuesta existente
        respuesta_existente.ponderacion = entrada.ponderacion
        db.commit()
        db.refresh(respuesta_existente)
        return respuesta_existente
    else:
        # Crear una nueva respuesta
        nueva_respuesta = page_models.Respuestas(
            id_cuestionario=entrada.id_cuestionario,
            pregunta=entrada.pregunta,
            id_usuario=entrada.id_usuario,
            ponderacion=entrada.ponderacion
        )
        db.add(nueva_respuesta)
        db.commit()
        db.refresh(nueva_respuesta)
        return nueva_respuesta

@router.put("/CambiarRespuestas/{Respuesta_id}",response_model=page_schemas.respuestas)
def mod_respuestas(respuestasid: int, entrada:page_schemas.respuestas,db:session=Depends(get_respuestas)):
    respuestas = db.query(page_models.Respuestas).filter_by(id=respuestasid).first()
    respuestas.id_cuestionario = entrada.id_cuestionario 
    respuestas.id_pregunta = entrada.id_pregunta
    respuestas.nickname = entrada.nickname
    respuestas.ponderacion = entrada.ponderacion
    db.commit()
    db.refresh(respuestas)
    return respuestas

@router.delete("/EliminarRespuestas/{respuestas_id}",response_model=page_schemas.respuesta)
def del_respuestas(respuestasid: int,db:session=Depends(get_respuestas)):
    respuestas = db.query(page_models.Respuestas).filter_by(id=respuestasid).first()
    db.delete(respuestas)
    db.commit()
    respuesta = page_schemas.respuesta(mensaje="Eliminado exitosamente")
    return respuesta