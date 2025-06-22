import pytest
from uuid import uuid4
from app.application import use_cases
from app.domain.models import ListaCreate, TareaCreate, task_status, task_progress, task_priority
from app.domain.exceptions import (
    EstadoInvalidoException,
    ProgresoInvalidoException,
    PrioridadInvalidaException,
    ListaNoEncontradaException,
    TareaNoEncontradaException
)

def test_create_list():
    initial_count = len(use_cases.fake_db)
    lista = use_cases.create_list(ListaCreate(name="Test Lista"))
    assert lista.name == "Test Lista"
    assert len(use_cases.fake_db) == initial_count + 1

def test_get_lists():
    listas = use_cases.get_lists()
    assert isinstance(listas, list)
    assert all(hasattr(l, "name") for l in listas)

def test_validar_estado_excepcion():
    with pytest.raises(EstadoInvalidoException):
        use_cases.validar_estado("estado_invalido")

def test_validar_progreso_excepcion():
    with pytest.raises(ProgresoInvalidoException):
        use_cases.validar_progreso("progreso_invalido")

def test_validar_prioridad_excepcion():
    with pytest.raises(PrioridadInvalidaException):
        use_cases.validar_prioridad("prioridad_invalida")

def test_update_list_success():
    lista = use_cases.create_list(ListaCreate(name="Lista Original"))
    updated = use_cases.update_list(lista.id, ListaCreate(name="Lista Actualizada"))
    assert updated.name == "Lista Actualizada"

def test_update_list_no_encontrada():
    with pytest.raises(ListaNoEncontradaException):
        use_cases.update_list(uuid4(), ListaCreate(name="No existe"))

def test_delete_list_success():
    lista = use_cases.create_list(ListaCreate(name="Para borrar"))
    use_cases.delete_list(lista.id)
    with pytest.raises(ListaNoEncontradaException):
        use_cases.delete_list(lista.id)  # Ya no existe

def test_delete_list_no_encontrada():
    with pytest.raises(ListaNoEncontradaException):
        use_cases.delete_list(uuid4())

def test_get_list_completion_empty():
    lista = use_cases.create_list(ListaCreate(name="Vacía"))
    assert use_cases.get_list_completion(lista.id) == "0%"

def test_get_list_completion_with_tasks():
    lista = use_cases.create_list(ListaCreate(name="Con tareas"))
    tarea_data_1 = TareaCreate(
        title="T1", description="Desc1", partner="P", rol="R",
        status=task_status[0],  # Ej: "Aprobada"
        progress=task_progress[0], priority=task_priority[0]
    )
    tarea_data_2 = TareaCreate(
        title="T2", description="Desc2", partner="P", rol="R",
        status=task_status[1],  # Otro estado válido pero no "Aprobada"
        progress=task_progress[0], priority=task_priority[0]
    )
    use_cases.create_task(lista.id, tarea_data_1)
    use_cases.create_task(lista.id, tarea_data_2)

    # Debug print
    for tarea in lista.tasks:
        print(f"Tarea: {tarea.title}, Status: {tarea.status}")

    porcentaje = use_cases.get_list_completion(lista.id)
    assert porcentaje == "50%"

def test_get_list_completion_no_encontrada():
    with pytest.raises(ListaNoEncontradaException):
        use_cases.get_list_completion(uuid4())

def test_create_task_validations():
    lista = use_cases.create_list(ListaCreate(name="Test Lista Tasks"))
    tarea_data = TareaCreate(
        title="Test Task",
        description="Desc",
        partner="Partner",
        rol="Rol",
        status=task_status[0],
        progress=task_progress[0],
        priority=task_priority[0]
    )
    tarea = use_cases.create_task(lista.id, tarea_data)
    assert tarea.title == "Test Task"
    assert tarea.status == task_status[0]

    with pytest.raises(EstadoInvalidoException):
        tarea_data.status = "Estado inválido"
        use_cases.create_task(lista.id, tarea_data)

    with pytest.raises(ProgresoInvalidoException):
        tarea_data.status = task_status[0]
        tarea_data.progress = "Progreso inválido"
        use_cases.create_task(lista.id, tarea_data)

    with pytest.raises(PrioridadInvalidaException):
        tarea_data.progress = task_progress[0]
        tarea_data.priority = "Prioridad inválida"
        use_cases.create_task(lista.id, tarea_data)

def test_create_task_list_no_encontrada():
    tarea_data = TareaCreate(
        title="Task",
        description="Desc",
        partner="Partner",
        rol="Rol",
        status=task_status[0],
        progress=task_progress[0],
        priority=task_priority[0]
    )
    with pytest.raises(ListaNoEncontradaException):
        use_cases.create_task(uuid4(), tarea_data)

def test_get_tasks_success():
    lista = use_cases.create_list(ListaCreate(name="Con tareas"))
    tarea_data = TareaCreate(
        title="T1", description="Desc", partner="P", rol="R",
        status=task_status[0], progress=task_progress[0], priority=task_priority[0]
    )
    tarea = use_cases.create_task(lista.id, tarea_data)
    tareas = use_cases.get_tasks(lista.id)
    assert tarea in tareas

def test_get_tasks_list_no_encontrada():
    with pytest.raises(ListaNoEncontradaException):
        use_cases.get_tasks(uuid4())

def test_update_task_success():
    lista = use_cases.create_list(ListaCreate(name="Lista"))
    tarea_data = TareaCreate(
        title="T1", description="Desc", partner="P", rol="R",
        status=task_status[0], progress=task_progress[0], priority=task_priority[0]
    )
    tarea = use_cases.create_task(lista.id, tarea_data)
    tarea_update = TareaCreate(
        title="T1 updated", description="Desc updated", partner="P", rol="R",
        status=task_status[0], progress=task_progress[0], priority=task_priority[0]
    )
    updated = use_cases.update_task(tarea.id, tarea_update)
    assert updated.title == "T1 updated"

def test_update_task_not_found():
    tarea_data = TareaCreate(
        title="Task",
        description="Desc",
        partner="Partner",
        rol="Rol",
        status=task_status[0],
        progress=task_progress[0],
        priority=task_priority[0]
    )
    with pytest.raises(TareaNoEncontradaException):
        use_cases.update_task(uuid4(), tarea_data)

def test_update_task_status_success():
    lista = use_cases.create_list(ListaCreate(name="Lista"))
    tarea_data = TareaCreate(
        title="T1", description="Desc", partner="P", rol="R",
        status=task_status[0], progress=task_progress[0], priority=task_priority[0]
    )
    tarea = use_cases.create_task(lista.id, tarea_data)
    updated = use_cases.update_task_status(tarea.id, task_status[1])
    assert updated.status == task_status[1]

def test_update_task_status_invalid():
    with pytest.raises(EstadoInvalidoException):
        use_cases.update_task_status(uuid4(), "estado_invalido")

def test_update_task_status_task_no_encontrada():
    with pytest.raises(TareaNoEncontradaException):
        use_cases.update_task_status(uuid4(), task_status[0])

def test_delete_task_success():
    lista = use_cases.create_list(ListaCreate(name="Lista"))
    tarea_data = TareaCreate(
        title="T1", description="Desc", partner="P", rol="R",
        status=task_status[0], progress=task_progress[0], priority=task_priority[0]
    )
    tarea = use_cases.create_task(lista.id, tarea_data)
    use_cases.delete_task(tarea.id)
    with pytest.raises(TareaNoEncontradaException):
        use_cases.delete_task(tarea.id)

def test_delete_task_no_encontrada():
    with pytest.raises(TareaNoEncontradaException):
        use_cases.delete_task(uuid4())

def test_filter_tasks():
    lista = use_cases.create_list(ListaCreate(name="Lista"))
    tarea_data1 = TareaCreate(
        title="T1", description="Desc", partner="P", rol="R",
        status=task_status[0], progress=task_progress[0], priority=task_priority[0]
    )
    tarea_data2 = TareaCreate(
        title="T2", description="Desc", partner="P", rol="R",
        status=task_status[1], progress=task_progress[0], priority=task_priority[1]
    )
    use_cases.create_task(lista.id, tarea_data1)
    use_cases.create_task(lista.id, tarea_data2)

    filtered_status = use_cases.filter_tasks(lista.id, status=task_status[0])
    assert all(t.status == task_status[0] for t in filtered_status)

    filtered_priority = use_cases.filter_tasks(lista.id, priority=task_priority[1])
    assert all(t.priority == task_priority[1] for t in filtered_priority)

    with pytest.raises(EstadoInvalidoException):
        use_cases.filter_tasks(lista.id, status="estado_invalido")

    with pytest.raises(PrioridadInvalidaException):
        use_cases.filter_tasks(lista.id, priority="prioridad_invalida")

def test_filter_tasks_list_no_encontrada():
    with pytest.raises(ListaNoEncontradaException):
        use_cases.filter_tasks(uuid4())

