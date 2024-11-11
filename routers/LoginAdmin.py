from datetime import datetime, timedelta
from typing import Annotated, List
from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from starlette.responses import RedirectResponse
from sqlalchemy.orm import session
from fastapi.params import Depends
from BD.Connn import engine, sessionlocal
import BD.schemas as page_schemas
import BD.Connn as page_conexion
import BD.modelos as page_models

page_models.Base.metadata.create_all(bind=engine)
router = APIRouter()
# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def get_LOGINADMIN():
    try:
        db = sessionlocal()
        yield db
    finally:
        db.close()

class TokenAdmin(BaseModel):
    access_token: str
    token_type: str


class TokenDataAdmin(BaseModel):
    username: str | None = None


class useriniAdmin(BaseModel):
    id: int
    nickname: str

    class Config:
       from_attributes = True
class userspsAdmin(useriniAdmin):
    password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return userspsAdmin(**user_dict)


def authenticate_user(username: str, password: str, db:session=Depends(get_LOGINADMIN)):
    user = db.query(page_models.Admin).filter(page_models.Admin.nickname == username).first()
    if not user:
        return False
    if not verify_password(password, user.contrasena):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db:session=Depends(get_LOGINADMIN)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenDataAdmin(username=username)
    except JWTError:
        raise credentials_exception
    user = db.query(page_models.Admin).filter(page_models.Admin.nickname == username).first()
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[useriniAdmin, Depends(get_current_user)]
):
    if current_user == 1 :
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@router.post("/tokenAdmin/", response_model=TokenAdmin)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db:session=Depends(get_LOGINADMIN)
):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.nickname}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/usersAdmin/me", response_model=useriniAdmin)
async def read_users_me(
    current_user: Annotated[useriniAdmin, Depends(get_current_active_user)]
):
    return current_user


@router.get("/usersAdmin/me/items")
async def read_own_items(
    current_user: Annotated[useriniAdmin, Depends(get_current_active_user)]
):
    return [{"item_id": "Foo", "owner": current_user.username}]