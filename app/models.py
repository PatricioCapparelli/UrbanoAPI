from sqlalchemy import Column, Integer, String, Float, Boolean
from app.database import Base

class Envio(Base):
    __tablename__ = "envios" 

    id = Column(Integer, primary_key=True, index=True)
    destinatario = Column(String, index=True)
    direccion = Column(String)
    peso_kg = Column(Float)
    es_fragil = Column(Boolean, default=False)
    estado = Column(String, default="En deposito")
    tracking_number = Column(String, unique=True, index=True)