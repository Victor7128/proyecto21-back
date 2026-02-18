from typing import Optional
import pyodbc
from services.utils import rows_to_list, row_to_dict, exec_sp


def get_pagos(conn: pyodbc.Connection, id_pago: int | None = None, id_documento: int | None = None,
              estado_pago: int | None = None, metodo: int | None = None) -> list[dict]:
    cursor = conn.cursor()
    exec_sp(cursor,"EXEC sp_GetPago ?, ?, ?, ?",
                   id_pago, id_documento, estado_pago, metodo)
    return rows_to_list(cursor)


def create_pago(conn: pyodbc.Connection, id_documento: int, monto_pagado: float,
                metodo: int, estado_pago: int,
                numero_comprobante: Optional[str] = None,
                numero_operacion: Optional[str] = None,
                observaciones: Optional[str] = None,
                id_personal: Optional[int] = None) -> dict | None:
    cursor = conn.cursor()
    exec_sp(cursor,
        "EXEC sp_InsertPago ?, ?, ?, ?, ?, ?, ?, ?",
        id_documento, monto_pagado, metodo, estado_pago,
        numero_comprobante, numero_operacion, observaciones, id_personal
    )
    result = row_to_dict(cursor)
    conn.commit()
    return result


def update_pago(conn: pyodbc.Connection, id_pago: int, estado_pago: int,
                numero_comprobante: Optional[str] = None,
                numero_operacion: Optional[str] = None,
                observaciones: Optional[str] = None) -> None:
    cursor = conn.cursor()
    exec_sp(cursor,
        "EXEC sp_UpdatePago ?, ?, ?, ?, ?",
        id_pago, estado_pago, numero_comprobante, numero_operacion, observaciones
    )
    conn.commit()


def delete_pago(conn: pyodbc.Connection, id_pago: int) -> None:
    """
    Elimina el pago y revierte el monto en el Documento.
    El SP maneja ambas operaciones en una sola transacción.
    """
    cursor = conn.cursor()
    exec_sp(cursor,"EXEC sp_DeletePago ?", id_pago)
    conn.commit()