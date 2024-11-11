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


def get_Admin():
    try:
        db = sessionlocal()
        yield db
    finally:
        db.close()


@router.get("/verAdmin/", response_model=List[page_schemas.Admin])
async def show_Admin(db:session=Depends(get_Admin)):
    Admin = db.query(page_models.Admin).all()
    return Admin


@router.post("/registrarAdmin/",response_model=page_schemas.Admin)
def create_Admin(entrada:page_schemas.Admin,db:session=Depends(get_Admin)):
   hashed_password = pwd_context.hash(entrada.contrasena)
   Admin = page_models.Admin(nickname = entrada.nickname,contrasena = hashed_password)
   db.add(Admin)
   db.commit()
   db.refresh(Admin)
   return Admin

@router.put("/CambiarUsernameAdmin/{Admin_id}",response_model=page_schemas.ModificarUsernameAdmin)
def mod_username_admin(adminid: int, entrada:page_schemas.ModificarUsernameAdmin,db:session=Depends(get_Admin)):
    admin = db.query(page_models.Admin).filter_by(id=adminid).first()
    admin.nickname = entrada.nickname
    db.commit()
    db.refresh(admin)
    return admin

@router.put("/contrasenaAdmin/{Admin_id}",response_model=page_schemas.ModificarPassWordAdmin)
def mod_contra_Admin(adminid: int, entrada:page_schemas.ModificarPassWordAdmin,db:session=Depends(get_Admin)):
    admin = db.query(page_models.Admin).filter_by(id=adminid).first()
    hashed_password = pwd_context.hash(entrada.contrasena)
    admin.contrasena = hashed_password
    db.commit()
    db.refresh(admin)
    return admin

@router.delete("/EliminarAdmin/{admin_id}",response_model=page_schemas.respuesta)
def del_admin(adminid: int,db:session=Depends(get_Admin)):
    admin = db.query(page_models.Admin).filter_by(id=adminid).first()
    db.delete(admin)
    db.commit()
    respuesta = page_schemas.respuesta(mensaje="Eliminado exitosamente")
    return respuesta