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

## Usuario a ingresar para obtener el JWT

- Username: admin
- Password: admin

## Requisitos

- Python 3.13+
- Docker (opcional para correr en contenedor)
- `venv` para entorno virtual (opcional si usás Docker)

---

## Configuración del entorno local

1. Clonar el repositorio:
    ```bash
    git clone https://github.com/faridaleali/python-challenge.git
    cd proyecto/src
    ```

2. Crear y activar entorno virtual:
    ```bash
    python -m venv ../venv
    source ./venv/Scripts/activate     # Windows
    source ./venv/bin/activate         # Linux/macOS
    ```

3. Instalar dependencias:
    ```bash
    pip install -r requirements.txt
    ```

4. Crear archivo `.env` en `src/` con las variables necesarias, ejemplo:
    ```
    SECRET_KEY=prueba_tecnica_backend
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    ```

5. Ejecutar servidor:
    ```bash
    cd src
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

Para correr todos los tests y obtener cobertura:

```bash
pytest --cov=app --cov-report=html
```

Luego abrir htmlcov/index.html para ver el reporte completo.

---

## Decisiones Técnicas (Resumen)

- FastAPI elegido por su rapidez y facilidad para crear APIs con validación automática.
- Pydantic para modelos y validación de datos.
- JWT para autenticación segura y stateless.
- Uso de Router para separar endpoints públicos (login) y protegidos.
- Dependencias de seguridad con Depends(JWTBearer()) para proteger rutas.
- In-memory fake_db para simplicidad en la demo, con posibilidad de migrar a base real.
- Pruebas divididas en unitarias e integración, con uso de pytest y TestClient.
- Docker Compose para orquestar contenedor y facilitar despliegue local.
- .env para manejo seguro de secretos y configuración.
- Asignación de tareas y simulación de notificaciones como casos de uso extra para sumar puntos.

---

## Contacto

Linkedin: https://www.linkedin.com/in/alealifarid/
