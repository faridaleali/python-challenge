from fastapi import HTTPException

class UsuarioNoEncontradoException(HTTPException):
    def __init__(self, detail="Usuario no encontrado"):
        super().__init__(status_code = 404, detail = detail)

class ListaNoEncontradaException(HTTPException):
    def __init__(self, detail="Lista no encontrada"):
        super().__init__(status_code = 404, detail = detail)

class TareaNoEncontradaException(HTTPException):
    def __init__(self, detail="Tarea no encontrada"):
        super().__init__(status_code = 404, detail = detail)

class EstadoInvalidoException(HTTPException):
    def __init__(self, detail="Estado inválido."):
        super().__init__(status_code = 404, detail = detail)

class ProgresoInvalidoException(HTTPException):
    def __init__(self, detail="Progreso inválido."):
        super().__init__(status_code = 404, detail = detail)

class PrioridadInvalidaException(HTTPException):
    def __init__(self, detail="Prioridad inválida."):
        super().__init__(status_code = 404, detail = detail)
