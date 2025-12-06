from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
import random

# Importamos desde el paquete padre 'app'
from app.database import get_db
from app import models, schemas

# Creamos el Router (Es como un mini-app FastAPI dedicado solo a envíos)
router = APIRouter(
    prefix="/envios",      # Todas las rutas empezarán con /envios
    tags=["Envíos"]        # Etiqueta para la documentación
)

# 1. CREAR (Nota que la ruta ahora es "/" porque ya definimos el prefijo arriba)
@router.post("/", response_model=schemas.EnvioResponse)
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

# 2. LISTAR
@router.get("/", response_model=List[schemas.EnvioResponse])
def listar_envios(db: Session = Depends(get_db)):
    return db.query(models.Envio).all()

# 3. BUSCAR POR ID
@router.get("/{envio_id}", response_model=schemas.EnvioResponse)
def obtener_envio(envio_id: int, db: Session = Depends(get_db)):
    envio = db.query(models.Envio).filter(models.Envio.id == envio_id).first()
    if envio is None:
        raise HTTPException(status_code=404, detail="Envío no encontrado")
    return envio

# 4. ACTUALIZAR ESTADO
@router.put("/{envio_id}/estado", response_model=schemas.EnvioResponse)
def actualizar_estado(envio_id: int, nuevo_estado: str, db: Session = Depends(get_db)):
    envio = db.query(models.Envio).filter(models.Envio.id == envio_id).first()
    if envio is None:
        raise HTTPException(status_code=404, detail="Envío no encontrado")
    
    estados_validos = ["En deposito", "En camino", "Entregado", "Cancelado"]
    if nuevo_estado not in estados_validos:
        raise HTTPException(status_code=400, detail="Estado inválido")
    
    envio.estado = nuevo_estado
    db.commit()
    db.refresh(envio)
    return envio