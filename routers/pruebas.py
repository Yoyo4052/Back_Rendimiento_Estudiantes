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


def get_pruebas():
    try:
        db = sessionlocal()
        yield db
    finally:
        db.close()


@router.get("/verPruebas/", response_model=List[page_schemas.Pruebas])
async def show_Pruebas(db:session=Depends(get_pruebas)):
    prueba = db.query(page_models.Pruebas).all()
    return prueba

@router.get("/verPruebas/{id_admin}/", response_model=List[page_schemas.Pruebas])
async def show_pruebas_por_admin(id_admin: int, db: session = Depends(get_pruebas)):
    resultados = db.query(page_models.Pruebas).filter(page_models.Pruebas.id_admin == id_admin).all()
    if not resultados:
        raise HTTPException(status_code=404, detail="No results found for this user")
    return resultados

@router.post("/registrarPrueba/", response_model=page_schemas.PruebasCreate)
def create_prueba(entrada: page_schemas.PruebasCreate, db: session = Depends(get_pruebas)):
    # Crea un nuevo resultado en la base de datos
    nuevaPrueba = page_models.Pruebas(resultados=entrada.resultados)
    nuevaPrueba.id_admin = entrada.id_admin
    nuevaPrueba.id_cuestionario = entrada.id_cuestionario
    db.add(nuevaPrueba)
    db.commit()
    db.refresh(nuevaPrueba)

    return nuevaPrueba

@router.put("/CambiarPrueba/{prueba_id}",response_model=page_schemas.PruebasBase)
def mod_prueba(prueba_id: int, entrada:page_schemas.PruebasBase,db:session=Depends(get_pruebas)):
    prueba = db.query(page_models.Pruebas).filter_by(id=prueba_id).first()
    prueba.resultados = entrada.resultados
    db.commit()
    db.refresh(prueba)
    return prueba

@router.delete("/Eliminarprueba/{prueba_id}",response_model=page_schemas.respuesta)
def del_prueba(prueba_id: int,db:session=Depends(get_pruebas)):
    prueba = db.query(page_models.Pruebas).filter_by(id=prueba_id).first()
    db.delete(prueba)
    db.commit()
    respuesta = page_schemas.respuesta(mensaje="Eliminado exitosamente")
    return respuesta