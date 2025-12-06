from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

Base.metadata.create_all(bind=engine)

client = TestClient(app)


def test_crear_envio():
    payload = {
        "destinatario": "Cliente Test",
        "direccion": "Calle Falsa 123",
        "peso_kg": 10.5,
        "es_fragil": True
    }
    response = client.post("/envios/", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["destinatario"] == "Cliente Test"
    assert "id" in data
    assert "tracking_number" in data

def test_listar_envios():
    response = client.get("/envios/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)