from fastapi import FastAPI
from app.database import engine
from app import models
from app.routers import envios 

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="UrbanoAPI",
    description="API Modular para gestión logística",
    version="2.0.0" # ¡Subimos de versión!
)

app.include_router(envios.router)

@app.get("/", tags=["Home"])
def home():
    return {"mensaje": "Bienvenido a UrbanoAPI v2 (Modular)"}