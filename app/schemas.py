from pydantic import BaseModel
from typing import Optional

class EnvioCreate(BaseModel):
    destinatario: str
    direccion: str
    peso_kg: float
    es_fragil: bool = False  

class EnvioResponse(EnvioCreate):
    id: int
    estado: str  
    tracking_number: str

    class Config:
        from_attributes = True