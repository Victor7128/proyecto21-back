import pyodbc
from services.utils import rows_to_list, row_to_dict
from services.utils import exec_sp

def get_huespedes(conn: pyodbc.Connection, id_huesped: int | None = None,
                  num_documento: str | None = None, nombre: str | None = None) -> list[dict]:
    cursor = conn.cursor()
    exec_sp(cursor,"EXEC sp_GetHuesped ?, ?, ?", id_huesped, num_documento, nombre)
    return rows_to_list(cursor)


def create_huesped(conn: pyodbc.Connection, nombres: str, apellidos: str,
                   tipo_documento: int, num_documento: str,
                   telefono: str | None = None, correo: str | None = None) -> dict | None:
    cursor = conn.cursor()
    exec_sp(cursor,
        "EXEC sp_InsertHuesped ?, ?, ?, ?, ?, ?",
        nombres, apellidos, tipo_documento, num_documento, telefono, correo
    )
    result = row_to_dict(cursor)
    conn.commit()
    return result


def update_huesped(conn: pyodbc.Connection, id_huesped: int, nombres: str, apellidos: str,
                   tipo_documento: int, num_documento: str,
                   telefono: str | None = None, correo: str | None = None) -> None:
    cursor = conn.cursor()
    exec_sp(cursor,
        "EXEC sp_UpdateHuesped ?, ?, ?, ?, ?, ?, ?",
        id_huesped, nombres, apellidos, tipo_documento, num_documento, telefono, correo
    )
    conn.commit()


def delete_huesped(conn: pyodbc.Connection, id_huesped: int) -> None:
    cursor = conn.cursor()
    exec_sp(cursor, "EXEC sp_DeleteHuesped ?", id_huesped)
    conn.commit()