# 🚚 UrbanoAPI: Sistema de Gestión Logística Fullstack

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.95%2B-009688)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED)
![Status](https://img.shields.io/badge/Status-Production-success)

> **Live Demo (Dashboard):** [https://urbanoapi-udmqj6flfvtrnfsg3d5sm9.streamlit.app/]
> **API Docs (Swagger):** [https://urbanoapi.onrender.com/docs]

## 📖 Descripción

**UrbanoAPI** es una solución integral para la gestión y trazabilidad de envíos logísticos. Diseñado con una arquitectura de microservicios modular, este proyecto demuestra la implementación de prácticas de ingeniería de software robustas en el ecosistema **Python**.

El sistema permite a los operarios registrar paquetes, gestionar estados mediante lógica de negocio estricta (State Machine) y visualizar métricas en tiempo real a través de un Dashboard interactivo.

## 🚀 Tecnologías y Arquitectura

Este proyecto marca una transición de arquitectura Java Enterprise a soluciones ágiles con Python moderno:

* **Backend:** [FastAPI](https://fastapi.tiangolo.com/) (Alto rendimiento, asíncrono y tipado estático).
* **Base de Datos & ORM:** [SQLAlchemy](https://www.sqlalchemy.org/) con SQLite (Dev) / PostgreSQL (Prod).
* **Validación de Datos:** [Pydantic](https://docs.pydantic.dev/) (Schemas y serialización robusta).
* **Frontend:** [Streamlit](https://streamlit.io/) (Dashboard interactivo para Data-Driven apps).
* **DevOps:** [Docker](https://www.docker.com/) & Docker Compose para contenerización.
* **Testing:** [Pytest](https://docs.pytest.org/) para pruebas unitarias e integración.

## ⚙️ Funcionalidades Clave

* ✅ **API RESTful Modular:** Endpoints organizados por Routers (`APIRouter`) siguiendo principios SOLID.
* ✅ **CRUD Completo:** Creación, Lectura, Actualización y Eliminación física de envíos.
* ✅ **Lógica de Negocio:** Validación de transiciones de estado (`En deposito` -> `En camino` -> `Entregado`).
* ✅ **Generación Automática:** Asignación de Tracking Numbers únicos (URB-XXXX).
* ✅ **Documentación Viva:** Swagger UI y ReDoc integrados automáticamente.

## 📂 Estructura del Proyecto

```text
UrbanoAPI/
├── app/
│   ├── routers/        # Controladores (Endpoints)
│   ├── tests/          # Tests automatizados
│   ├── database.py     # Configuración de BD (Singleton session)
│   ├── main.py         # Punto de entrada de la API
│   ├── models.py       # Entidades ORM (Tablas)
│   ├── schemas.py      # DTOs (Pydantic Models)
│   └── dashboard.py    # Frontend (Streamlit)
├── Dockerfile          # Receta de construcción de imagen
├── docker-compose.yml  # Orquestación de servicios
├── requirements.txt    # Dependencias
└── README.md           # Documentación
```
Instalación y Uso
## 🛠️ Instalación y Uso
### Requisitos Previos
* [Docker](https://www.docker.com/get-started) instalado en tu máquina.
* [Docker Compose](https://docs.docker.com/compose/install/) instalado.    
### Clonar el Repositorio
```bashbash
git clone https://github.com/PatricioCapparelli/UrbanoAPI
cd UrbanoAPI
```
### Construir y Levantar los Contenedores
```bash
docker-compose up --build
```
### Acceder a la Aplicación
* **API RESTful:** Navega a `http://localhost:8000/docs` para la documentación Swagger.
* **Dashboard Streamlit:** Navega a `https://urbanoapi-udmqj6flfvtrnfsg3d5sm9.streamlit.app/` para la interfaz de usuario.

## 🧪 Ejecutar Pruebas
Dentro del contenedor de la API, ejecuta:
```bash
pytest app/tests
```
## 🤝 Contribuciones
¡Las contribuciones son bienvenidas! Por favor, abre un issue o envía un pull request para mejoras o correcciones.

Made with ❤️ by Pato.
