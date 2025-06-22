# Proyecto Backend FastAPI - Lista de Tareas

## Descripción del proyecto

Este proyecto es una API REST construida con FastAPI para la gestión de listas y tareas, incluyendo funcionalidades de:

- CRUD para listas y tareas.
- Autenticación con JWT (login).
- Asignación de usuario responsable a cada tarea.
- Simulación de notificaciones por email (no real).
- Validaciones y manejo de errores.
- Tests unitarios e integración completos.

---

## Requisitos

- Python 3.13+
- Docker (opcional para correr en contenedor)
- `venv` para entorno virtual (opcional si usás Docker)

---

## Configuración del entorno local

1. Clonar el repositorio:
    ```bash
    git clone <URL-del-repo>
    cd proyecto/src
    ```

2. Crear y activar entorno virtual:
    ```bash
    python -m venv ../venv
    source ../venv/Scripts/activate     # Windows
    source ../venv/bin/activate         # Linux/macOS
    ```

3. Instalar dependencias:
    ```bash
    pip install -r requirements.txt
    ```

4. Crear archivo `.env` en `src/` con las variables necesarias, ejemplo:
    ```
    SECRET_KEY=tu_clave_secreta_aqui
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    ```

5. Ejecutar servidor:
    ```bash
    uvicorn app.main:app --reload
    ```

6. Acceder a la documentación Swagger:
    ```
    http://127.0.0.1:8000/docs
    ```

---

## Uso de Docker

1. Construir imagen Docker:
    ```bash
    docker compose build
    ```

2. Ejecutar contenedor:
    ```bash
    docker compose up
    ```

3. La API estará disponible en:
    ```
    http://localhost:8000
    ```

---

## Ejecutar pruebas

### Tests unitarios
```bash
pytest app/tests/test_unit.py --cov=app --cov-report=term-missing
```

### Tests integracion
```bash
pytest app/tests/test_integration.py --cov=app --cov-report=term-missing
```

```bash
pytest --cov=app --cov-report=html
```