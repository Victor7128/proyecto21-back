import pyodbc
from services.utils import rows_to_list, row_to_dict, exec_sp


def get_habitaciones(conn: pyodbc.Connection, id_habitacion: int | None = None, piso: int | None = None,
                     estado: int | None = None, id_tipo_habitacion: int | None = None) -> list[dict]:
    cursor = conn.cursor()
    exec_sp(cursor,"EXEC sp_GetHabitacion ?, ?, ?, ?",
                   id_habitacion, piso, estado, id_tipo_habitacion)
    return rows_to_list(cursor)


def create_habitacion(conn: pyodbc.Connection, numero: str, piso: int,
                      id_tipo_habitacion: int, estado: int) -> dict | None:
    cursor = conn.cursor()
    exec_sp(cursor,"EXEC sp_InsertHabitacion ?, ?, ?, ?",
                   numero, piso, id_tipo_habitacion, estado)
    result = row_to_dict(cursor)
    conn.commit()
    return result


def update_habitacion(conn: pyodbc.Connection, id_habitacion: int, numero: str,
                      piso: int, id_tipo_habitacion: int, estado: int) -> None:
    cursor = conn.cursor()
    exec_sp(cursor,"EXEC sp_UpdateHabitacion ?, ?, ?, ?, ?",
                   id_habitacion, numero, piso, id_tipo_habitacion, estado)
    conn.commit()


def delete_habitacion(conn: pyodbc.Connection, id_habitacion: int) -> None:
    cursor = conn.cursor()
    exec_sp(cursor,"EXEC sp_DeleteHabitacion ?", id_habitacion)
    conn.commit()