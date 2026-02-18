from datetime import date
import pyodbc
from services.utils import rows_to_list, row_to_dict, exec_sp


def get_reservas(conn: pyodbc.Connection, id_reserva: int | None = None, id_huesped: int | None = None,
                 id_habitacion: int | None = None, estado: int | None = None,
                 fecha_entrada: date | None = None, fecha_salida: date | None = None) -> list[dict]:
    cursor = conn.cursor()
    exec_sp(cursor,
        "EXEC sp_GetReserva ?, ?, ?, ?, ?, ?",
        id_reserva, id_huesped, id_habitacion, estado, fecha_entrada, fecha_salida
    )
    return rows_to_list(cursor)


def create_reserva(conn: pyodbc.Connection, id_huesped: int, id_habitacion: int,
                   fecha_entrada: date, fecha_salida: date, num_personas: int,
                   monto_total: float, estado: int) -> dict | None:
    cursor = conn.cursor()
    exec_sp(cursor,
        "EXEC sp_InsertReserva ?, ?, ?, ?, ?, ?, ?",
        id_huesped, id_habitacion, fecha_entrada, fecha_salida,
        num_personas, monto_total, estado
    )
    result = row_to_dict(cursor)
    conn.commit()
    return result


def update_reserva(conn: pyodbc.Connection, id_reserva: int, id_huesped: int,
                   id_habitacion: int, fecha_entrada: date, fecha_salida: date,
                   num_personas: int, monto_total: float, estado: int) -> None:
    cursor = conn.cursor()
    exec_sp(cursor,
        "EXEC sp_UpdateReserva ?, ?, ?, ?, ?, ?, ?, ?",
        id_reserva, id_huesped, id_habitacion, fecha_entrada,
        fecha_salida, num_personas, monto_total, estado
    )
    conn.commit()


def delete_reserva(conn: pyodbc.Connection, id_reserva: int) -> None:
    cursor = conn.cursor()
    exec_sp(cursor,"EXEC sp_DeleteReserva ?", id_reserva)
    conn.commit()