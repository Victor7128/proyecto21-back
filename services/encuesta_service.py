from typing import Optional
import pyodbc
from services.utils import rows_to_list, row_to_dict, exec_sp


def get_encuestas(conn: pyodbc.Connection, id_encuesta: int | None = None,
                  id_orden_hospedaje: int | None = None,
                  motivo_viaje: str | None = None) -> list[dict]:
    cursor = conn.cursor()
    exec_sp(cursor,"EXEC sp_GetEncuesta ?, ?, ?",
                   id_encuesta, id_orden_hospedaje, motivo_viaje)
    return rows_to_list(cursor)


def create_encuesta(conn: pyodbc.Connection, id_orden_hospedaje: int, recomendacion: int,
                    descripcion: Optional[str] = None, lugar_origen: Optional[str] = None,
                    motivo_viaje: Optional[str] = None,
                    calificacion_limpieza: Optional[int] = None,
                    calificacion_servicio: Optional[int] = None,
                    calificacion_ubicacion: Optional[int] = None,
                    calificacion_precio: Optional[int] = None,
                    comentarios: Optional[str] = None) -> Optional[dict]:
    cursor = conn.cursor()
    exec_sp(cursor,
        "EXEC sp_InsertEncuesta ?, ?, ?, ?, ?, ?, ?, ?, ?, ?",
        id_orden_hospedaje, descripcion, recomendacion, lugar_origen, motivo_viaje,
        calificacion_limpieza, calificacion_servicio,
        calificacion_ubicacion, calificacion_precio, comentarios
    )
    result = row_to_dict(cursor)
    conn.commit()
    return result


def update_encuesta(conn: pyodbc.Connection, id_encuesta: int, recomendacion: int,
                    descripcion: Optional[str] = None, lugar_origen: Optional[str] = None,
                    motivo_viaje: Optional[str] = None,
                    calificacion_limpieza: Optional[int] = None,
                    calificacion_servicio: Optional[int] = None,
                    calificacion_ubicacion: Optional[int] = None,
                    calificacion_precio: Optional[int] = None,
                    comentarios: Optional[str] = None) -> None:
    cursor = conn.cursor()
    exec_sp(cursor,
        "EXEC sp_UpdateEncuesta ?, ?, ?, ?, ?, ?, ?, ?, ?, ?",
        id_encuesta, descripcion, recomendacion, lugar_origen, motivo_viaje,
        calificacion_limpieza, calificacion_servicio,
        calificacion_ubicacion, calificacion_precio, comentarios
    )
    conn.commit()


def delete_encuesta(conn: pyodbc.Connection, id_encuesta: int) -> None:
    cursor = conn.cursor()
    exec_sp(cursor,"EXEC sp_DeleteEncuesta ?", id_encuesta)
    conn.commit()