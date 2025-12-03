# 🚚 UrbanoAPI ()

API RESTful desarrollada con **Python** y **FastAPI** para la gestión logística de envíos y trazabilidad de paquetes. Este proyecto implementa un sistema robusto de estados (State Machine) y persistencia de datos relacional.

## 🚀 Tecnologías Utilizadas
* **Python 3.10+**
* **FastAPI** (Framework moderno de alto rendimiento)
* **SQLAlchemy** (ORM para manejo de base de datos)
* **SQLite** (Base de datos para desarrollo, escalable a PostgreSQL)
* **Pydantic** (Validación de datos y serialización)

## ⚙️ Funcionalidades
* ✅ **Creación de Envíos:** Generación automática de Tracking Number.
* ✅ **Trazabilidad:** Consulta de estado de paquetes en tiempo real.
* ✅ **Gestión de Estados:** Validación de reglas de negocio para transiciones de estado (En depósito -> En camino -> Entregado).
* ✅ **Documentación Automática:** Swagger UI integrado.

## 🛠️ Instalación y Uso

1. Clonar el repositorio:
   ```bash
    git clone [https://github.com/PatricioCapparelli/UrbanoAPI]
    cd UrbanoAPI
    ```