from fastapi import APIRouter, Body, HTTPException, Query, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.auth.auth_handler import create_access_token
from app.auth.auth_bearer import JWTBearer
from typing import List
from uuid import UUID

from app.domain.models import ListaCreate, TareaCreate, Lista, Tarea
from app.application.use_cases import (
    get_lists, create_list, update_list, delete_list, get_list_completion,
    get_tasks, create_task, update_task, update_task_status, delete_task, filter_tasks
)

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
@public_router.post("/login", tags=["Login para obtener JWT"], summary="Login de usuario para obtener JWT")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username == "admin" and form_data.password == "admin":
        token = create_access_token({"sub": form_data.username})
        return {
                "access_token": token, 
                "token_type": "bearer"
            }
    raise HTTPException(status_code=401, detail="Credenciales inválidas")

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
def api_create_task(list_id: UUID, tarea_data: TareaCreate):
    return create_task(list_id, tarea_data)

@router.put("/tasks/{task_id}", response_model=Tarea, tags=["Endpoints de tareas"], summary="Actualizar tarea por ID")
def api_update_task(task_id: UUID, tarea_data: TareaCreate):
    return update_task(task_id, tarea_data)

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
