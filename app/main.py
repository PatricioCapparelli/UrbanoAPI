from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
import random

from app.database import engine, Base, get_db
from app import models, schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="UrbanoAPI",
    description="API RESTful para gestión logística y trazabilidad de envíos",
    version="1.0.0"
)

@app.post("/envios/", response_model=schemas.EnvioResponse, tags=["Envíos"])
def crear_envio(envio: schemas.EnvioCreate, db: Session = Depends(get_db)):
    tracking = f"URB-{random.randint(1000, 9999)}"
    
    nuevo_envio = models.Envio(
        destinatario=envio.destinatario,
        direccion=envio.direccion,
        peso_kg=envio.peso_kg,
        es_fragil=envio.es_fragil,
        estado="En deposito",  
        tracking_number=tracking
    )
    
    db.add(nuevo_envio)
    db.commit()         
    db.refresh(nuevo_envio)
    
    return nuevo_envio

@app.get("/envios/", response_model=List[schemas.EnvioResponse], tags=["Envíos"])
def listar_envios(db: Session = Depends(get_db)):
    return db.query(models.Envio).all()


@app.get("/envios/{envio_id}", response_model=schemas.EnvioResponse, tags=["Envíos"])
def obtener_envio(envio_id: int, db: Session = Depends(get_db)):
    envio = db.query(models.Envio).filter(models.Envio.id == envio_id).first()
    
    if envio is None:
        raise HTTPException(status_code=404, detail="Envío no encontrado")
        
    return envio


@app.put("/envios/{envio_id}/estado", response_model=schemas.EnvioResponse, tags=["Operaciones"])
def actualizar_estado(envio_id: int, nuevo_estado: str, db: Session = Depends(get_db)):
    envio = db.query(models.Envio).filter(models.Envio.id == envio_id).first()
    
    if envio is None:
        raise HTTPException(status_code=404, detail="Envío no encontrado")
    
    estados_validos = ["En deposito", "En camino", "Entregado", "Cancelado"]
    
    if nuevo_estado not in estados_validos:
        raise HTTPException(
            status_code=400, 
            detail=f"Estado inválido. Los estados permitidos son: {estados_validos}"
        )
    
    envio.estado = nuevo_estado
    db.commit()
    db.refresh(envio)
    
    return envio