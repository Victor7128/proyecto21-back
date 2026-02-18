from datetime import datetime
from typing import Optional
import pyodbc
from services.utils import rows_to_list, row_to_dict, exec_sp


def get_ordenes_conserjeria(conn: pyodbc.Connection, id_orden_conserj: int | None = None,
                            id_habitacion: int | None = None, id_personal: int | None = None,
                            estado: int | None = None) -> list[dict]:
    cursor = conn.cursor()
    exec_sp(cursor,"EXEC sp_GetOrdenConserjeria ?, ?, ?, ?",
                   id_orden_conserj, id_habitacion, id_personal, estado)
    return rows_to_list(cursor)


def create_orden_conserjeria(conn: pyodbc.Connection, id_personal: int, id_habitacion: int,
                             fecha_inicio: datetime, precio: float, estado: int,
                             id_reserva: Optional[int] = None,
                             fecha_fin: Optional[datetime] = None,
                             descripcion: Optional[str] = None) -> Optional[dict]:
    cursor = conn.cursor()
    exec_sp(cursor,
        "EXEC sp_InsertOrdenConserjeria ?, ?, ?, ?, ?, ?, ?, ?",
        id_personal, id_habitacion, id_reserva, fecha_inicio,
        fecha_fin, precio, estado, descripcion
    )
    result = row_to_dict(cursor)
    conn.commit()
    return result


def update_orden_conserjeria(conn: pyodbc.Connection, id_orden_conserj: int, id_personal: int,
                             id_habitacion: int, fecha_inicio: datetime, precio: float,
                             estado: int, id_reserva: Optional[int] = None,
                             fecha_fin: Optional[datetime] = None,
                             descripcion: Optional[str] = None) -> None:
    cursor = conn.cursor()
    exec_sp(cursor,
        "EXEC sp_UpdateOrdenConserjeria ?, ?, ?, ?, ?, ?, ?, ?, ?",
        id_orden_conserj, id_personal, id_habitacion, id_reserva,
        fecha_inicio, fecha_fin, precio, estado, descripcion
    )
    conn.commit()


def delete_orden_conserjeria(conn: pyodbc.Connection, id_orden_conserj: int) -> None:
    cursor = conn.cursor()
    exec_sp(cursor,"EXEC sp_DeleteOrdenConserjeria ?", id_orden_conserj)
    conn.commit()