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


def get_cuestionario():
    try:
        db = sessionlocal()
        yield db
    finally:
        db.close()


@router.get("/verCuestionarios/", response_model=List[page_schemas.Cuestionario])
async def show_Cuestionarios(db:session=Depends(get_cuestionario)):
    cuestionario = db.query(page_models.Cuestionarios).all()
    return cuestionario

@router.get("/verCuestionario/{id}", response_model=page_schemas.Cuestionario)
async def show_Cuestionario(id: int, db: session = Depends(get_cuestionario)):
    cuestionario = db.query(page_models.Cuestionarios).filter_by(id=id).first()
    if cuestionario is None:
        raise HTTPException(status_code=404, detail="Cuestionario not found")
    return cuestionario

@router.post("/registrarCuestionario/", response_model=page_schemas.Cuestionario)
def create_cuestionario(entrada: page_schemas.CuestionarioBase, db: session = Depends(get_cuestionario)):
    # Crea un nuevo cuestionario en la base de datos
    nuevo_cuestionario = page_models.Cuestionarios(descripcion=entrada.descripcion)
    db.add(nuevo_cuestionario)
    db.commit()
    db.refresh(nuevo_cuestionario)

    # Si hay preguntas proporcionadas en la entrada, asócialas al cuestionario
    if entrada.preguntas:
        for pregunta in entrada.preguntas:
            nueva_pregunta = page_models.Preguntas(
                id_cuestionario=nuevo_cuestionario.id,
                pregunta=pregunta.pregunta,
                tipo=pregunta.tipo
            )
            db.add(nueva_pregunta)
        db.commit()

    return nuevo_cuestionario

from typing import List

@router.put("/CambiarCuestionario/{cuestionario_id}", response_model=page_schemas.Cuestionario)
def mod_cuestionario(cuestionario_id: int, entrada: page_schemas.Cuestionario, db: session = Depends(get_cuestionario)):
    cuestionario = db.query(page_models.Cuestionarios).filter_by(id=cuestionario_id).first()

    # Recuperar las preguntas existentes asociadas al cuestionario actual
    preguntas_actuales = cuestionario.preguntas

    # Crear un diccionario para almacenar las preguntas existentes por su ID
    preguntas_actuales_por_id = {pregunta.id: pregunta for pregunta in preguntas_actuales}

    # Eliminar las preguntas existentes que no están presentes en las nuevas preguntas proporcionadas
    for pregunta in preguntas_actuales:
        if pregunta.id not in [pregunta.id for pregunta in entrada.preguntas]:
            db.delete(pregunta)

    # Actualizar las preguntas existentes con los nuevos datos proporcionados
    for pregunta_nueva in entrada.preguntas:
        if pregunta_nueva.id in preguntas_actuales_por_id:
            pregunta_existente = preguntas_actuales_por_id[pregunta_nueva.id]
            pregunta_existente.pregunta = pregunta_nueva.pregunta
            pregunta_existente.tipo = pregunta_nueva.tipo

    # Insertar las nuevas preguntas proporcionadas que no están asociadas al cuestionario actual
    for pregunta_nueva in entrada.preguntas:
        if pregunta_nueva.id is None:
            pregunta_db = page_models.Preguntas(
                id_cuestionario=cuestionario_id,
                pregunta=pregunta_nueva.pregunta,
                tipo=pregunta_nueva.tipo
            )
            db.add(pregunta_db)

    cuestionario.descripcion = entrada.descripcion

    db.commit()
    db.refresh(cuestionario)
    return cuestionario

from sqlalchemy.orm import joinedload

@router.delete("/EliminarCuestionario/{cuestionario_id}/", response_model=page_schemas.respuesta)
def del_cuestionario(cuestionario_id: int, db: session = Depends(get_cuestionario)):
    # Recuperar el cuestionario y todas sus preguntas y resultados asociados
    cuestionario = db.query(page_models.Cuestionarios).options(joinedload(page_models.Cuestionarios.preguntas), joinedload(page_models.Cuestionarios.resultados)).filter_by(id=cuestionario_id).first()

    if cuestionario:
        # Eliminar todas las preguntas asociadas al cuestionario
        for pregunta in cuestionario.preguntas:
            db.delete(pregunta)

        # Eliminar todos los resultados asociados al cuestionario
        for resultado in cuestionario.resultados:
            db.delete(resultado)

        # Eliminar el cuestionario
        db.delete(cuestionario)
        db.commit()

        respuesta = page_schemas.respuesta(mensaje="Eliminado exitosamente")
    else:
        respuesta = page_schemas.respuesta(mensaje="Cuestionario no encontrado")

    return respuesta

