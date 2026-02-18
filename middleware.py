import pyodbc
from fastapi import Request
from fastapi.responses import JSONResponse
from exceptions import HotelException


async def hotel_exception_handler(request: Request, exc: HotelException):
    """
    Captura todas las excepciones personalizadas del proyecto
    (NotFoundError, ConflictError, BusinessRuleError, etc.)
    y las convierte en respuestas JSON con el código HTTP correcto.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


async def pyodbc_exception_handler(request: Request, exc: pyodbc.Error):
    """
    Captura errores de pyodbc, incluyendo los RAISERROR lanzados
    por los stored procedures.

    Los RAISERROR del SP vienen en exc.args[1] con el mensaje exacto
    que definiste en SQL, por ejemplo:
        'La habitación no está disponible en ese rango de fechas.'

    Si por alguna razón el formato es distinto, cae al mensaje genérico.
    """
    try:
        # args[1] contiene el mensaje del RAISERROR
        mensaje = exc.args[1]
    except (IndexError, TypeError):
        mensaje = "Error en la base de datos."

    return JSONResponse(
        status_code=400,
        content={"detail": mensaje},
    )


async def generic_exception_handler(request: Request, exc: Exception):
    """
    Captura cualquier excepción no controlada.
    En producción oculta el detalle técnico; en desarrollo lo muestra.
    """
    from config import get_settings
    settings = get_settings()

    detail = str(exc) if settings.DEBUG else "Error interno del servidor."

    return JSONResponse(
        status_code=500,
        content={"detail": detail},
    )