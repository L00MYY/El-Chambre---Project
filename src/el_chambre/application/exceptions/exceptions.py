"""
Excepciones propias de la capa de aplicación (application/).

Estas excepciones NO conocen códigos HTTP ni nada de Flask.
La capa api/ las traduce a respuestas HTTP:

    ValidationError        -> 400
    NotFoundError           -> 404
    ConflictError            -> 409
    InsufficientStockError   -> 409
"""


class ValidationError(Exception):
    """Los datos recibidos no cumplen una regla de validación básica."""
    pass


class NotFoundError(Exception):
    """El recurso solicitado (sucursal, producto, materia prima, etc.) no existe."""
    pass


class ConflictError(Exception):
    """La operación entra en conflicto con el estado actual de los datos
    (por ejemplo, crear un inventario que ya existe)."""
    pass


class InsufficientStockError(Exception):
    """No hay stock suficiente para completar la operación solicitada."""
    pass
