from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from uuid import UUID, uuid4

class User(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    username: str
    full_name: Optional[str] = None
    email: Optional[str] = None

class UserCreate(BaseModel):
    username: str
    full_name: Optional[str] = None
    email: Optional[str] = None
    password: str

class UserInDB(User):
    hashed_password: str

task_status = [ "No iniciada", "Iniciada", "En revision", "Rechazada", "Aprobada" ]
task_progress = [ "0%", "25", "50%", "75", "100%" ]
task_priority = [ "Muy bajo", "Bajo", "Medio", "Alto", "Muy alto" ]

class TareaCreate(BaseModel):
    title: str
    description: str
    partner: str
    rol: str
    status: str = Field(default_factory=lambda: task_status[0]) 
    progress: str = Field(default_factory=lambda: task_progress[0])
    priority: str = Field(default_factory=lambda: task_priority[2])
    assigned_to: Optional[str] = None

class Tarea(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    title: str
    description: str
    partner: str
    rol: str
    status: str
    progress: str
    priority: str
    assigned_to: Optional[str] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Tareas personales",
                "description": "Hacer la cama",
                "partner": "EMPRESA A",
                "rol": "Administrador de lista",
                "status": "No iniciada",
                "progress": "0%",
                "priority": "Muy bajo",
                "assigned_to":"admin"
            }
        }
    )

class ListaCreate(BaseModel):
    name: str

class Lista(BaseModel):
    id: UUID = Field(default_factory = uuid4)
    name: str
    tasks: Optional[List[Tarea]] = Field(default_factory=list)

    model_config = ConfigDict(
        json_schema_extra = {
            "example": {
                "name": "Tareas personales",
                "tasks": []
            }
        }
    )
