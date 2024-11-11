from fastapi import APIRouter,HTTPException
from typing import List
from starlette.responses import RedirectResponse
from sqlalchemy.orm import session
from fastapi.params import Depends
from passlib.context import CryptContext

from BD.Connn import engine, sessionlocal

import BD.schemas as page_schemas
import BD.Connn as page_conexion
import BD.modelos as page_models
import bcrypt
import random
import yagmail

email = 'progamernazi@gmail.com'
passw = 'rcqiqlitxtgqraon'
yag = yagmail.SMTP(user=email, password=passw)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
page_models.Base.metadata.create_all(bind=engine)
router = APIRouter()


def get_Users():
    try:
        db = sessionlocal()
        yield db
    finally:
        db.close()


@router.get("/verUsers/", response_model=List[page_schemas.User])
async def show_User(db:session=Depends(get_Users)):
    Users = db.query(page_models.Usuarios).all()
    return Users


@router.get("/EnviarCodigoRecuperacion/{Correo}")
async def show_pass_correo(correo: str, db: session = Depends(get_Users)):
    passs = db.query(page_models.Usuarios).filter(page_models.Usuarios.correo == correo).first()
    if not passs:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    destinatario = correo
    asunto = 'codigo de recuperacion para: '+ passs.nickname
    mensaje = str(passs.codigo)
    
    yag.send(destinatario, asunto, mensaje)

    mensaje = ("codigo enviado")

    return mensaje

@router.post("/registrarUsers/",response_model=page_schemas.RegisterUser)
def create_user(entrada:page_schemas.RegisterUser,db:session=Depends(get_Users)):
   hashed_password = pwd_context.hash(entrada.contrasena)
   codigo1 = random.randint(1000, 9999)
   usuario = page_models.Usuarios(nickname = entrada.nickname,correo = entrada.correo, contrasena = hashed_password, codigo = codigo1)
   db.add(usuario)
   db.commit()
   db.refresh(usuario)
   return usuario

@router.put("/CambiarUsersadmin/{usuario_id}",response_model=page_schemas.ModificarUser)
def mod_user_admin(usuarioid: int, entrada:page_schemas.ModificarUser,db:session=Depends(get_Users)):
    usuario = db.query(page_models.Usuarios).filter_by(id=usuarioid).first()
    usuario.nickname = entrada.nickname
    usuario.correo = entrada.correo
    db.commit()
    db.refresh(usuario)
    return usuario

@router.put("/contrasena/{codigo}",response_model=page_schemas.Modificarcontrasena)
def mod_contra(codigo: int, entrada:page_schemas.Modificarcontrasena,db:session=Depends(get_Users)):
    usuario = db.query(page_models.Usuarios).filter_by(codigo=codigo).first()
    hashed_password = pwd_context.hash(entrada.contrasena)
    usuario.contrasena = hashed_password
    db.commit()
    db.refresh(usuario)
    return usuario

@router.delete("/EliminarUsers/{usuario_id}",response_model=page_schemas.respuesta)
def del_user(usuarioid: int,db:session=Depends(get_Users)):
    usuario = db.query(page_models.Usuarios).filter_by(id=usuarioid).first()
    db.delete(usuario)
    db.commit()
    respuesta = page_schemas.respuesta(mensaje="Eliminado exitosamente")
    return respuesta