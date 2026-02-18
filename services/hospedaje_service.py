from datetime import datetime
from typing import Optional
import pyodbc
from services.utils import rows_to_list, row_to_dict, exec_sp


def get_ordenes_hospedaje(conn: pyodbc.Connection, id_orden_hospedaje: int | None = None,
                          id_reserva: int | None = None, estado: int | None = None) -> list[dict]:
    cursor = conn.cursor()
    exec_sp(cursor,"EXEC sp_GetOrdenHospedaje ?, ?, ?",
                   id_orden_hospedaje, id_reserva, estado)
    return rows_to_list(cursor)


def create_orden_hospedaje(conn: pyodbc.Connection, id_reserva: int, estado: int,
                           fecha_checkin: Optional[datetime] = None,
                           fecha_checkout: Optional[datetime] = None) -> dict | None:
    cursor = conn.cursor()
    exec_sp(cursor,"EXEC sp_InsertOrdenHospedaje ?, ?, ?, ?",
                   id_reserva, estado, fecha_checkin, fecha_checkout)
    result = row_to_dict(cursor)
    conn.commit()
    return result


def update_orden_hospedaje(conn: pyodbc.Connection, id_orden_hospedaje: int, estado: int,
                           fecha_checkin: Optional[datetime] = None,
                           fecha_checkout: Optional[datetime] = None) -> None:
    cursor = conn.cursor()
    exec_sp(cursor,"EXEC sp_UpdateOrdenHospedaje ?, ?, ?, ?",
                   id_orden_hospedaje, estado, fecha_checkin, fecha_checkout)
    conn.commit()


def delete_orden_hospedaje(conn: pyodbc.Connection, id_orden_hospedaje: int) -> None:
    cursor = conn.cursor()
    exec_sp(cursor,"EXEC sp_DeleteOrdenHospedaje ?", id_orden_hospedaje)
    conn.commit()