"""
Funciones utilitarias compartidas por todos los services.
"""
import pyodbc
from typing import Optional
from decimal import Decimal

from fastapi import HTTPException

def exec_sp(cursor, sql, *params):
    """Ejecuta un SP y convierte errores de SQL en HTTPException."""
    try:
        cursor.execute(sql, *params)
    except pyodbc.Error as e:
        msg = str(e)
        raise HTTPException(status_code=400, detail=msg)


def rows_to_list(cursor: pyodbc.Cursor) -> list[dict]:
    """
    Convierte todas las filas del cursor en una lista de diccionarios.
    Usar después de un SELECT (sp_GetXxx).
    """
    if cursor.description is None:
        return []
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def row_to_dict(cursor: pyodbc.Cursor) -> Optional[dict]:
    if cursor.description is None:
        return None
    columns = [col[0] for col in cursor.description]
    row = cursor.fetchone()
    if row is None:
        return None
    result = {}
    for key, value in zip(columns, row):
        if isinstance(value, Decimal):
            value = int(value) if value == value.to_integral_value() else float(value)
        result[key] = value
    return result