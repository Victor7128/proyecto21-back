class HotelException(Exception):
    """
    Excepción base del proyecto.
    Todas las excepciones personalizadas heredan de esta.
    """
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail
        super().__init__(detail)


class NotFoundError(HotelException):
    """Recurso no encontrado. → HTTP 404"""
    def __init__(self, entidad: str):
        super().__init__(404, f"{entidad} no encontrado.")


class ConflictError(HotelException):
    """Conflicto de datos (duplicados, restricciones únicas). → HTTP 409"""
    def __init__(self, detail: str):
        super().__init__(409, detail)


class BusinessRuleError(HotelException):
    """Regla de negocio violada (fechas inválidas, saldo excedido, etc.). → HTTP 422"""
    def __init__(self, detail: str):
        super().__init__(422, detail)


class UnauthorizedError(HotelException):
    """Credenciales inválidas o token expirado. → HTTP 401"""
    def __init__(self, detail: str = "No autorizado."):
        super().__init__(401, detail)


class ForbiddenError(HotelException):
    """Usuario autenticado pero sin permisos suficientes. → HTTP 403"""
    def __init__(self, detail: str = "No tienes permisos para realizar esta acción."):
        super().__init__(403, detail)