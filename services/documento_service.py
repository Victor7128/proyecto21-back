from datetime import date
from typing import Optional
import pyodbc
from services.utils import rows_to_list, row_to_dict, exec_sp


def get_documentos(conn: pyodbc.Connection, id_documento: int | None = None,
                   numero_documento: str | None = None, estado_documento: int | None = None,
                   tipo_documento: int | None = None) -> list[dict]:
    cursor = conn.cursor()
    exec_sp(cursor,"EXEC sp_GetDocumento ?, ?, ?, ?",
                   id_documento, numero_documento, estado_documento, tipo_documento)
    return rows_to_list(cursor)


def create_documento(conn: pyodbc.Connection, numero_documento: str, tipo_documento: int,
                     monto_total: float, estado_documento: int,
                     id_reserva: Optional[int] = None,
                     id_orden_hospedaje: Optional[int] = None,
                     id_orden_conserjeria: Optional[int] = None,
                     monto_pagado: float = 0.0,
                     fecha_vencimiento: Optional[date] = None,
                     descripcion: Optional[str] = None) -> Optional[dict]:
    cursor = conn.cursor()
    exec_sp(cursor,
        "EXEC sp_InsertDocumento ?, ?, ?, ?, ?, ?, ?, ?, ?, ?",
        numero_documento, tipo_documento, id_reserva, id_orden_hospedaje,
        id_orden_conserjeria, monto_total, monto_pagado,
        fecha_vencimiento, descripcion, estado_documento
    )
    result = row_to_dict(cursor)
    conn.commit()
    return result


def update_documento(conn: pyodbc.Connection, id_documento: int, monto_pagado: float,
                     estado_documento: int, fecha_vencimiento: Optional[date] = None,
                     descripcion: Optional[str] = None) -> None:
    cursor = conn.cursor()
    exec_sp(cursor,
        "EXEC sp_UpdateDocumento ?, ?, ?, ?, ?",
        id_documento, monto_pagado, fecha_vencimiento, descripcion, estado_documento
    )
    conn.commit()


def delete_documento(conn: pyodbc.Connection, id_documento: int) -> None:
    cursor = conn.cursor()
    exec_sp(cursor,"EXEC sp_DeleteDocumento ?", id_documento)
    conn.commit()