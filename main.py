from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import login
from routers import LoginAdmin
from routers import registerUser
from routers import AdminRegistro
from routers import cuestionarios
from routers import preguntas
from routers import respuestas
from routers import resultados
from routers import resultadosFODA
from routers import respuestasprueba
from routers import pruebas
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(login.router, tags=["Login"])
app.include_router(LoginAdmin.router, tags=["LoginAdmin"])
app.include_router(AdminRegistro.router, tags=["AdminRegistro"])
app.include_router(registerUser.router, tags=["RegisterUser"])
app.include_router(cuestionarios.router, tags=["Cuestionario"])
app.include_router(preguntas.router, tags=["Preguntas"])
app.include_router(resultados.router, tags=["Resultados"])
app.include_router(resultadosFODA.router, tags=["ResultadosFODA"])
app.include_router(respuestas.router, tags=["Respuestas"])
app.include_router(respuestasprueba.router, tags=["RespuestasPrueba"])
app.include_router(pruebas.router, tags=["Pruebas"])

app.mount("/static", StaticFiles(directory=Path.cwd() / "public" / "static"), name="static")

@app.get("/", response_class=RedirectResponse)
async def redirect_to_login():
    return RedirectResponse(url="/login")

@app.get("/login", response_class=HTMLResponse)
async def serve_react_login():
    index_file = Path.cwd() / "public" / "index.html"
    with open(index_file, "r") as f:
        return f.read()
    
@app.get("/{full_path:path}", response_class=HTMLResponse)
async def serve_react(full_path: str):
    index_file = Path.cwd() / "public" / "index.html"
    with open(index_file, "r") as f:
        return f.read()

from threading import Thread
import time
import requests

def keep_alive():
    while True:
        try:
            requests.get("https://back-rendimiento-estudiantes.onrender.com")
        except Exception as e:
            print(f"Error al hacer ping interno: {e}")
        time.sleep(180)  # 5 minutos

Thread(target=keep_alive, daemon=True).start()

if __name__ == "__main__":
    import os
    import uvicorn
    port = int(os.environ.get("PORT", 8000))  # Render proporciona el puerto en PORT
    uvicorn.run("main:app", host="0.0.0.0", port=port)  # Cambia "main" por el nombre de tu archivo Python


