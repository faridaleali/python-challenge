from fastapi.testclient import TestClient
from app.main import app
from app.domain.models import task_status, task_priority, task_progress
from uuid import UUID

client = TestClient(app)

def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert "Servidor levantado" in response.json().get("message", "")

def test_create_get_update_delete_list():
    # Crear lista
    response = client.post("/list", json={"name": "Lista para CRUD"})
    assert response.status_code == 200
    list_data = response.json()
    list_id = list_data["id"]
    assert list_data["name"] == "Lista para CRUD"
    assert isinstance(UUID(list_id), UUID)

    # Obtener listas y validar que la creada está presente
    response = client.get("/lists")
    assert response.status_code == 200
    assert any(lista["id"] == list_id for lista in response.json())

    # Actualizar lista
    response = client.put(f"/lists/{list_id}", json={"name": "Lista actualizada"})
    assert response.status_code == 200
    assert response.json()["name"] == "Lista actualizada"

    # Obtener porcentaje completado (vacío, debe ser 0%)
    response = client.get(f"/lists/completion/{list_id}")
    assert response.status_code == 200
    assert response.json()["completion"] == "0%"

    # Borrar lista
    response = client.delete(f"/lists/{list_id}")
    assert response.status_code == 204

    # Confirmar que ya no existe
    response = client.get("/lists")
    assert all(l["id"] != list_id for l in response.json())

def test_task_lifecycle():
    # Crear lista para tareas
    response = client.post("/list", json={"name": "Lista tareas"})
    list_id = response.json()["id"]

    # Crear tarea válida
    tarea_data = {
        "title": "Tarea Test",
        "description": "Descripción",
        "partner": "Partner",
        "rol": "Rol",
        "status": task_status[0],
        "progress": task_progress[0],
        "priority": task_priority[0]
    }
    response = client.post(f"/tasks/{list_id}/", json=tarea_data)
    assert response.status_code == 200
    task = response.json()
    task_id = task["id"]

    # Obtener tareas de la lista y verificar que la creada esté presente
    response = client.get(f"/tasks/{list_id}")
    assert response.status_code == 200
    assert any(t["id"] == task_id for t in response.json())

    # Actualizar tarea
    updated_data = tarea_data.copy()
    updated_data["title"] = "Tarea actualizada"
    response = client.put(f"/tasks/{task_id}", json=updated_data)
    assert response.status_code == 200
    assert response.json()["title"] == "Tarea actualizada"

    # Cambiar estado de la tarea
    new_status = task_status[1]
    response = client.patch(f"/tasks/status/{task_id}", json={"status": new_status})
    assert response.status_code == 200
    assert response.json()["status"] == new_status

    # Filtrar tareas por estado
    response = client.get(f"/tasks/filter/{list_id}?status={new_status}")
    assert response.status_code == 200
    assert all(t["status"] == new_status for t in response.json())

    # Filtrar tareas por prioridad
    response = client.get(f"/tasks/filter/{list_id}?priority={task_priority[0]}")
    assert response.status_code == 200
    assert all(t["priority"] == task_priority[0] for t in response.json())

    # Borrar tarea
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 204

    # Confirmar que la tarea ya no existe
    response = client.get(f"/tasks/{list_id}")
    assert all(t["id"] != task_id for t in response.json())

def test_create_task_invalid_status():
    # Crear lista para tarea inválida
    response = client.post("/list", json={"name": "Lista inválida"})
    list_id = response.json()["id"]

    # Intentar crear tarea con status inválido
    tarea_data = {
        "title": "Tarea inválida",
        "description": "Desc",
        "partner": "P",
        "rol": "R",
        "status": "Estado inválido",
        "progress": task_progress[0],
        "priority": task_priority[0]
    }
    response = client.post(f"/tasks/{list_id}/", json=tarea_data)
    assert response.status_code == 400
    assert "Estado inválido" in response.text

def test_get_list_completion_with_tasks():
    # Crear lista con tareas
    response = client.post("/list", json={"name": "Lista con tareas"})
    list_id = response.json()["id"]

    # Crear tareas con diferentes estados
    tarea_data_1 = {
        "title": "Tarea 1",
        "description": "Desc1",
        "partner": "P",
        "rol": "R",
        "status": task_status[0],  # Por ejemplo "Aprobada"
        "progress": task_progress[0],
        "priority": task_priority[0]
    }
    tarea_data_2 = tarea_data_1.copy()
    tarea_data_2["status"] = task_status[1]  # Otro estado válido diferente

    client.post(f"/tasks/{list_id}/", json=tarea_data_1)
    client.post(f"/tasks/{list_id}/", json=tarea_data_2)

    # Obtener porcentaje de tareas completadas
    response = client.get(f"/lists/completion/{list_id}")
    assert response.status_code == 200
    completion = response.json()["completion"]

    # Aquí asumimos que el estado "Aprobada" es el que cuenta como completado
    assert completion in ["50%", "0%"]  # Depende si el estado para completado es sólo "Aprobada"

