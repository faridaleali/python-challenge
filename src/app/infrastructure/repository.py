from typing import List
from uuid import UUID, uuid4
from app.domain.models import Lista, UserInDB

fake_db: List[Lista] = [
    Lista(
        id = UUID("123e4567-e89b-12d3-a456-426614174000"),
        title = "Tareas personales",
        tasks = []
    )
]

fake_db_users = [
    UserInDB(
        id = UUID("d46f53ab-a9d4-4abc-ab3b-920d7d130edd"),
        username = "admin",
        full_name = "Administrador",
        email = "admin@example.com",
        hashed_password = "admin"
    )
]
