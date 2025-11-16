from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

#!Importamos las variable router de cada uno de los modulos o archivos
from app.api.routers.auth_router import router as auth_router
from app.api.routers.notes_router import router as notes_router
from app.api.routers.labels_router import router as labels_router
from app.api.routers.shares_router import router as shares_router
from app.core.conf import settings
from app.core.db import init_db

# Leemos e archivo .env
load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    if settings.ENVIRONMENT=="DEV":
        init_db()
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan,  # 👉 usa el gestor del ciclo de vida para manejar el arranque y la finalizacion de la aplicacion
    swagger_ui_parameters={
        "persistAuthorization": True  # para mantener la session en swagger
    },
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# @app.get("/")
# def read_root():
#     return {"Hellor": "World"}


app.include_router(auth_router, prefix="/api/v1")
app.include_router(notes_router, prefix="/api/v1")
app.include_router(labels_router, prefix="/api/v1")
app.include_router(shares_router, prefix="/api/v1")
