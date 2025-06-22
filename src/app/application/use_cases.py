from typing import List, Optional
from uuid import UUID
from app.domain.models import Lista, ListaCreate, Tarea, TareaCreate, User, UserCreate, task_status, task_progress, task_priority
from app.domain.exceptions import (
    ListaNoEncontradaException, TareaNoEncontradaException,
    EstadoInvalidoException, ProgresoInvalidoException, PrioridadInvalidaException, UsuarioNoEncontradoException
)
from app.infrastructure.repository import fake_db, fake_db_users


# Validacioness
def validar_estado(status: str):
    if status not in task_status:
        raise EstadoInvalidoException()

def validar_progreso(progress: str):
    if progress not in task_progress:
        raise ProgresoInvalidoException()

def validar_prioridad(priority: str):
    if priority not in task_priority:
        raise PrioridadInvalidaException()

# USUARIOS

def create_user(user_data: UserCreate) -> User:
    user = User(
        username        =   user_data.username,
        full_name       =   user_data.full_name,
        email           =   user_data.email
    )
    fake_db_users.append(user)
    return user

def get_user_by_username(username: str) -> User:
    for user in fake_db_users:
        if user.username == username:
            return user
    raise UsuarioNoEncontradoException()

# LISTAS

def get_lists() -> List[Lista]:
    return fake_db

def create_list(lista_data: ListaCreate) -> Lista:
    nueva_lista = Lista(name=lista_data.name, tasks=[])
    fake_db.append(nueva_lista)
    return nueva_lista

def update_list(list_id: UUID, lista_data: ListaCreate) -> Lista:
    for i, lista in enumerate(fake_db):
        if lista.id == list_id:
            lista_actualizada = Lista(id=lista.id, name=lista_data.name, tasks=lista.tasks)
            fake_db[i] = lista_actualizada
            return lista_actualizada
    raise ListaNoEncontradaException()

def delete_list(list_id: UUID):
    for i, lista in enumerate(fake_db):
        if lista.id == list_id:
            del fake_db[i]
            return
    raise ListaNoEncontradaException()

def get_list_completion(list_id: UUID) -> str:
    for lista in fake_db:
        if lista.id == list_id:
            total = len(lista.tasks)
            if total == 0:
                return "0%"
            completadas = sum(1 for t in lista.tasks if t.status == task_status[0])
            porcentaje = round((completadas / total) * 100)
            return f"{porcentaje}%"
    raise ListaNoEncontradaException()

# TAREAS

def get_tasks(list_id: UUID) -> List[Tarea]:
    for lista in fake_db:
        if lista.id == list_id:
            return lista.tasks
    raise ListaNoEncontradaException()

def create_task(list_id: UUID, tarea_data: TareaCreate, current_user: User) -> Tarea:
    validar_estado(tarea_data.status)
    validar_progreso(tarea_data.progress)
    validar_prioridad(tarea_data.priority)

    assigned_user = current_user
    if tarea_data.assigned_to:
        assigned_user = get_user_by_username(tarea_data.assigned_to)

    for lista in fake_db:
        if lista.id == list_id:
            nueva_tarea = Tarea(
                title       = tarea_data.title,
                description = tarea_data.description,
                partner     = tarea_data.partner,
                rol         = tarea_data.rol,
                status      = tarea_data.status,
                progress    = tarea_data.progress,
                priority    = tarea_data.priority,
                assigned_to = assigned_user.username if assigned_user else None
            )
            lista.tasks.append(nueva_tarea)

            print(f"[Notificación] Se asignó la tarea '{tarea_data.title}' al usuario '{assigned_user.username}'")

            return nueva_tarea

    raise ListaNoEncontradaException()

def update_task(task_id: UUID, tarea_data: TareaCreate, current_user: User) -> Tarea:
    validar_estado(tarea_data.status)
    validar_progreso(tarea_data.progress)
    validar_prioridad(tarea_data.priority)

    assigned_user = current_user
    if tarea_data.assigned_to:
        assigned_user = get_user_by_username(tarea_data.assigned_to)

    for lista in fake_db:
        for i, tarea in enumerate(lista.tasks):
            if tarea.id == task_id:
                tarea_actualizada = Tarea(
                    id = tarea.id,
                    title = tarea_data.title,
                    description = tarea_data.description,
                    partner = tarea_data.partner,
                    rol = tarea_data.rol,
                    status = tarea_data.status,
                    progress = tarea_data.progress,
                    priority = tarea_data.priority,
                    assigned_to = assigned_user.username if assigned_user else None
                )
                lista.tasks[i] = tarea_actualizada
                return tarea_actualizada

    raise TareaNoEncontradaException()

def update_task_status(task_id: UUID, status: str) -> Tarea:
    validar_estado(status)
    for lista in fake_db:
        for tarea in lista.tasks:
            if tarea.id == task_id:
                tarea.status = status
                return tarea
    raise TareaNoEncontradaException()

def delete_task(task_id: UUID):
    for lista in fake_db:
        for i, tarea in enumerate(lista.tasks):
            if tarea.id == task_id:
                del lista.tasks[i]
                return
    raise TareaNoEncontradaException()

def filter_tasks(list_id: UUID, status: Optional[str] = None, priority: Optional[str] = None) -> List[Tarea]:
    for lista in fake_db:
        if lista.id == list_id:
            tareas = lista.tasks
            if status:
                validar_estado(status)
                tareas = [t for t in tareas if t.status == status]
            if priority:
                validar_prioridad(priority)
                tareas = [t for t in tareas if t.priority == priority]
            return tareas
    raise ListaNoEncontradaException()
