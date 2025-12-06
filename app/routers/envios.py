from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List
import random

from app.database import get_db
from app import models, schemas

# Definimos los estados válidos como constante para evitar errores de tipeo
ESTADOS_VALIDOS = ["En deposito", "En camino", "Entregado", "Cancelado"]

router = APIRouter(
    prefix="/envios",
    tags=["Envíos"]
)

# --- RUTAS ---

@router.post("/", response_model=schemas.EnvioResponse, status_code=status.HTTP_201_CREATED, summary="Crear un nuevo envío")
def crear_envio(envio: schemas.EnvioCreate, db: Session = Depends(get_db)):
    """
    Registra un nuevo envío en el sistema.
    - Genera automáticamente un **Tracking Number** único.
    - Asigna el estado inicial: **En deposito**.
    """
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

@router.get("/", response_model=List[schemas.EnvioResponse], summary="Listar todos los envíos")
def listar_envios(db: Session = Depends(get_db)):
    """Retorna la lista completa de envíos registrados."""
    return db.query(models.Envio).all()

@router.get("/{envio_id}", response_model=schemas.EnvioResponse, summary="Obtener envío por ID")
def obtener_envio(envio_id: int, db: Session = Depends(get_db)):
    envio = db.query(models.Envio).filter(models.Envio.id == envio_id).first()
    if envio is None:
        raise HTTPException(status_code=404, detail="Envío no encontrado")
    return envio

@router.put("/{envio_id}/estado", response_model=schemas.EnvioResponse, summary="Actualizar estado")
def actualizar_estado(envio_id: int, nuevo_estado: str, db: Session = Depends(get_db)):
    """
    Actualiza el estado de un envío.
    Estados permitidos: "En deposito", "En camino", "Entregado", "Cancelado".
    """
    envio = db.query(models.Envio).filter(models.Envio.id == envio_id).first()
    if envio is None:
        raise HTTPException(status_code=404, detail="Envío no encontrado")
    
    if nuevo_estado not in ESTADOS_VALIDOS:
        raise HTTPException(
            status_code=400, 
            detail=f"Estado inválido. Opciones permitidas: {ESTADOS_VALIDOS}"
        )
    
    envio.estado = nuevo_estado
    db.commit()
    db.refresh(envio)
    return envio

@router.delete("/{envio_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar envío")
def eliminar_envio(envio_id: int, db: Session = Depends(get_db)):
    """Elimina físicamente un registro de la base de datos."""
    envio = db.query(models.Envio).filter(models.Envio.id == envio_id).first()
    if envio is None:
        raise HTTPException(status_code=404, detail="Envío no encontrado")
    
    db.delete(envio)
    db.commit()
    return None