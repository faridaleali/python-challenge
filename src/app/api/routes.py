import os
from fastapi import APIRouter, Body, HTTPException, Query, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from app.auth.auth_handler import create_access_token
from app.auth.auth_bearer import JWTBearer
from typing import Annotated, List
from uuid import UUID
from passlib.context import CryptContext
from app.infrastructure.repository import fake_db_users
from jose import jwt, JWTError
from fastapi import HTTPException, status
from dotenv import load_dotenv


from app.domain.models import ListaCreate, TareaCreate, Lista, Tarea, User
from app.application.use_cases import (
    get_lists, create_list, update_list, delete_list, get_list_completion,
    get_tasks, create_task, update_task, update_task_status, delete_task, filter_tasks
)

## Descriptar ##

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    print("Token recibido:", token)
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        if username is None:
            raise credentials_exception
        
    except JWTError:
        raise credentials_exception
    user = get_user_by_username(username)
    if user is None:
        raise credentials_exception
    return user

##### Rutas ####

# Publica #
public_router = APIRouter()

# Privada - Aca aplicamos a todos los endpoints que necesitas JWT #
router = APIRouter(
    dependencies=[Depends(JWTBearer())]
)

##### Home ####

@public_router.get("/", tags=["Main"])
def home():
    return {"message": "Servidor levantado :)"}

##### Login #####

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_user_by_username(username: str):
    for user in fake_db_users:
        if user.username == username:
            return user
    return None

@public_router.post("/login", tags=["Login para obtener JWT"], summary="Login de usuario para obtener JWT")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = get_user_by_username(form_data.username)

    if not user:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    token_data = {
        "username": user.username,
        "email": user.email,
    }

    token = create_access_token(token_data)

    return {
        "access_token": token,
        "token_type": "bearer"
    }

##### Listas #####

@router.get("/lists", response_model=List[Lista], tags=["Endpoints de lista"], summary="Traer todas las listas")
def api_get_lists():
    return get_lists()

@router.post("/list", response_model=Lista, tags=["Endpoints de lista"], summary="Crear una lista")
def api_create_list(lista_data: ListaCreate):
    return create_list(lista_data)

@router.put("/lists/{list_id}", response_model=Lista, tags=["Endpoints de lista"], summary="Editar una lista")
def api_update_list(list_id: UUID, lista_data: ListaCreate):
    return update_list(list_id, lista_data)

@router.delete("/lists/{list_id}", tags=["Endpoints de lista"], summary="Eliminar una lista", status_code=204)
def api_delete_list(list_id: UUID):
    delete_list(list_id)
    return None

@router.get("/lists/completion/{list_id}", tags=["Endpoints de lista"], summary="Porcentaje de tareas completadas")
def api_get_list_completion(list_id: UUID):
    return {"completion": get_list_completion(list_id)}

##### Tareas #####

@router.get("/tasks/{list_id}", response_model=List[Tarea], tags=["Endpoints de tareas"], summary="Traer todas las tareas de una lista")
def api_get_tasks(list_id: UUID):
    return get_tasks(list_id)

@router.post("/tasks/{list_id}/", response_model=Tarea, tags=["Endpoints de tareas"], summary="Crear tareas en una lista")
def api_create_task(list_id: UUID, tarea_data: TareaCreate, current_user: User = Depends(get_current_user)):
    return create_task(list_id, tarea_data, current_user)

@router.put("/tasks/{task_id}", response_model=Tarea, tags=["Endpoints de tareas"], summary="Actualizar tarea por ID")
def api_update_task(task_id: UUID, tarea_data: TareaCreate, current_user: User = Depends(get_current_user)):
    return update_task(task_id, tarea_data, current_user)

@router.patch("/tasks/status/{task_id}", response_model=Tarea, tags=["Endpoints de tareas"], summary="Modificar estado de una tarea por ID")
def api_update_task_status(task_id: UUID, status: str = Body(..., embed=True)):
    return update_task_status(task_id, status)

@router.delete("/tasks/{task_id}", tags=["Endpoints de tareas"], summary="Eliminar tarea por ID", status_code=204)
def api_delete_task(task_id: UUID):
    delete_task(task_id)
    return None

@router.get("/tasks/filter/{list_id}", response_model=List[Tarea], tags=["Endpoints de tareas"], summary="Filtrar tareas por estado o prioridad")
def api_filter_tasks(list_id: UUID, status: str = Query(None), priority: str = Query(None)):
    return filter_tasks(list_id, status, priority)
