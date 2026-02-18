"""
Service para todas las tablas catálogo (lookup tables).
Cada tabla sigue el mismo patrón: get, create, update, delete.
"""
import pyodbc
from services.utils import rows_to_list, row_to_dict
from services.utils import exec_sp

# ── TipoDocumento ──────────────────────────────────────────────────────────────

def get_tipo_documento(conn: pyodbc.Connection, id_tipo_documento: int | None = None) -> list[dict]:
    cursor = conn.cursor()
    exec_sp(cursor,"EXEC sp_GetTipoDocumento ?", id_tipo_documento)
    return rows_to_list(cursor)


def create_tipo_documento(conn: pyodbc.Connection, codigo: str, descripcion: str) -> dict | None:
    cursor = conn.cursor()
    exec_sp(cursor, "EXEC sp_InsertTipoDocumento ?, ?", codigo, descripcion)
    result = row_to_dict(cursor)
    conn.commit()
    return result


def update_tipo_documento(conn: pyodbc.Connection, id_tipo_documento: int, codigo: str, descripcion: str) -> None:
    cursor = conn.cursor()
    exec_sp(cursor,"EXEC sp_UpdateTipoDocumento ?, ?, ?", id_tipo_documento, codigo, descripcion)
    conn.commit()


def delete_tipo_documento(conn: pyodbc.Connection, id_tipo_documento: int) -> None:
    cursor = conn.cursor()
    exec_sp(cursor,"EXEC sp_DeleteTipoDocumento ?", id_tipo_documento)
    conn.commit()


# ── EstadoReserva ──────────────────────────────────────────────────────────────

def get_estado_reserva(conn: pyodbc.Connection, id_estado_reserva: int | None = None) -> list[dict]:
    cursor = conn.cursor()
    exec_sp(cursor,"EXEC sp_GetEstadoReserva ?", id_estado_reserva)
    return rows_to_list(cursor)


def create_estado_reserva(conn: pyodbc.Connection, nombre: str) -> dict | None:
    cursor = conn.cursor()
    exec_sp(cursor,"EXEC sp_InsertEstadoReserva ?", nombre)
    result = row_to_dict(cursor)
    conn.commit()
    return result


def update_estado_reserva(conn: pyodbc.Connection, id_estado_reserva: int, nombre: str) -> None:
    cursor = conn.cursor()
    exec_sp(cursor,"EXEC sp_UpdateEstadoReserva ?, ?", id_estado_reserva, nombre)
    conn.commit()


def delete_estado_reserva(conn: pyodbc.Connection, id_estado_reserva: int) -> None:
    cursor = conn.cursor()
    exec_sp(cursor,"EXEC sp_DeleteEstadoReserva ?", id_estado_reserva)
    conn.commit()


# ── EstadoHabitacion ───────────────────────────────────────────────────────────

def get_estado_habitacion(conn: pyodbc.Connection, id_estado_habitacion: int | None = None) -> list[dict]:
    cursor = conn.cursor()
    exec_sp(cursor,"EXEC sp_GetEstadoHabitacion ?", id_estado_habitacion)
    return rows_to_list(cursor)


def create_estado_habitacion(conn: pyodbc.Connection, nombre: str) -> dict | None:
    cursor = conn.cursor()
    exec_sp(cursor,"EXEC sp_InsertEstadoHabitacion ?", nombre)
    result = row_to_dict(cursor)
    conn.commit()
    return result


def update_estado_habitacion(conn: pyodbc.Connection, id_estado_habitacion: int, nombre: str) -> None:
    cursor = conn.cursor()
    exec_sp(cursor,"EXEC sp_UpdateEstadoHabitacion ?, ?", id_estado_habitacion, nombre)
    conn.commit()


def delete_estado_habitacion(conn: pyodbc.Connection, id_estado_habitacion: int) -> None:
    cursor = conn.cursor()
    exec_sp(cursor,"EXEC sp_DeleteEstadoHabitacion ?", id_estado_habitacion)
    conn.commit()


# ── EstadoOrdenConserjeria ─────────────────────────────────────────────────────

def get_estado_orden_conserjeria(conn: pyodbc.Connection, id_estado_orden_conserj: int | None = None) -> list[dict]:
    cursor = conn.cursor()
    exec_sp(cursor,"EXEC sp_GetEstadoOrdenConserjeria ?", id_estado_orden_conserj)
    return rows_to_list(cursor)


def create_estado_orden_conserjeria(conn: pyodbc.Connection, nombre: str) -> dict | None:
    cursor = conn.cursor()
    exec_sp(cursor,"EXEC sp_InsertEstadoOrdenConserjeria ?", nombre)
    result = row_to_dict(cursor)
    conn.commit()
    return result


def update_estado_orden_conserjeria(conn: pyodbc.Connection, id_estado_orden_conserj: int, nombre: str) -> None:
    cursor = conn.cursor()
    exec_sp(cursor,"EXEC sp_UpdateEstadoOrdenConserjeria ?, ?", id_estado_orden_conserj, nombre)
    conn.commit()


def delete_estado_orden_conserjeria(conn: pyodbc.Connection, id_estado_orden_conserj: int) -> None:
    cursor = conn.cursor()
    exec_sp(cursor,"EXEC sp_DeleteEstadoOrdenConserjeria ?", id_estado_orden_conserj)
    conn.commit()


# ── EstadoOrdenHospedaje ───────────────────────────────────────────────────────

def get_estado_orden_hospedaje(conn: pyodbc.Connection, id_estado_orden_hosp: int | None = None) -> list[dict]:
    cursor = conn.cursor()
    exec_sp(cursor,"EXEC sp_GetEstadoOrdenHospedaje ?", id_estado_orden_hosp)
    return rows_to_list(cursor)


def create_estado_orden_hospedaje(conn: pyodbc.Connection, nombre: str) -> dict | None:
    cursor = conn.cursor()
    exec_sp(cursor,"EXEC sp_InsertEstadoOrdenHospedaje ?", nombre)
    result = row_to_dict(cursor)
    conn.commit()
    return result


def update_estado_orden_hospedaje(conn: pyodbc.Connection, id_estado_orden_hosp: int, nombre: str) -> None:
    cursor = conn.cursor()
    exec_sp(cursor,"EXEC sp_UpdateEstadoOrdenHospedaje ?, ?", id_estado_orden_hosp, nombre)
    conn.commit()


def delete_estado_orden_hospedaje(conn: pyodbc.Connection, id_estado_orden_hosp: int) -> None:
    cursor = conn.cursor()
    exec_sp(cursor,"EXEC sp_DeleteEstadoOrdenHospedaje ?", id_estado_orden_hosp)
    conn.commit()


# ── EstadoPago ─────────────────────────────────────────────────────────────────

def get_estado_pago(conn: pyodbc.Connection, id_estado_pago: int | None = None) -> list[dict]:
    cursor = conn.cursor()
    exec_sp(cursor,"EXEC sp_GetEstadoPago ?", id_estado_pago)
    return rows_to_list(cursor)


def create_estado_pago(conn: pyodbc.Connection, nombre: str) -> dict | None:
    cursor = conn.cursor()
    exec_sp(cursor,"EXEC sp_InsertEstadoPago ?", nombre)
    result = row_to_dict(cursor)
    conn.commit()
    return result


def update_estado_pago(conn: pyodbc.Connection, id_estado_pago: int, nombre: str) -> None:
    cursor = conn.cursor()
    exec_sp(cursor,"EXEC sp_UpdateEstadoPago ?, ?", id_estado_pago, nombre)
    conn.commit()


def delete_estado_pago(conn: pyodbc.Connection, id_estado_pago: int) -> None:
    cursor = conn.cursor()
    exec_sp(cursor,"EXEC sp_DeleteEstadoPago ?", id_estado_pago)
    conn.commit()


# ── EstadoDocumento ────────────────────────────────────────────────────────────

def get_estado_documento(conn: pyodbc.Connection, id_estado_documento: int | None = None) -> list[dict]:
    cursor = conn.cursor()
    exec_sp(cursor,"EXEC sp_GetEstadoDocumento ?", id_estado_documento)
    return rows_to_list(cursor)


def create_estado_documento(conn: pyodbc.Connection, nombre: str) -> dict | None:
    cursor = conn.cursor()
    exec_sp(cursor,"EXEC sp_InsertEstadoDocumento ?", nombre)
    result = row_to_dict(cursor)
    conn.commit()
    return result


def update_estado_documento(conn: pyodbc.Connection, id_estado_documento: int, nombre: str) -> None:
    cursor = conn.cursor()
    exec_sp(cursor,"EXEC sp_UpdateEstadoDocumento ?, ?", id_estado_documento, nombre)
    conn.commit()


def delete_estado_documento(conn: pyodbc.Connection, id_estado_documento: int) -> None:
    cursor = conn.cursor()
    exec_sp(cursor,"EXEC sp_DeleteEstadoDocumento ?", id_estado_documento)
    conn.commit()


# ── MetodoPago ─────────────────────────────────────────────────────────────────

def get_metodo_pago(conn: pyodbc.Connection, id_metodo_pago: int | None = None) -> list[dict]:
    cursor = conn.cursor()
    exec_sp(cursor,"EXEC sp_GetMetodoPago ?", id_metodo_pago)
    return rows_to_list(cursor)


def create_metodo_pago(conn: pyodbc.Connection, nombre: str) -> dict | None:
    cursor = conn.cursor()
    exec_sp(cursor,"EXEC sp_InsertMetodoPago ?", nombre)
    result = row_to_dict(cursor)
    conn.commit()
    return result


def update_metodo_pago(conn: pyodbc.Connection, id_metodo_pago: int, nombre: str) -> None:
    cursor = conn.cursor()
    exec_sp(cursor,"EXEC sp_UpdateMetodoPago ?, ?", id_metodo_pago, nombre)
    conn.commit()


def delete_metodo_pago(conn: pyodbc.Connection, id_metodo_pago: int) -> None:
    cursor = conn.cursor()
    exec_sp(cursor,"EXEC sp_DeleteMetodoPago ?", id_metodo_pago)
    conn.commit()


# ── Rol ────────────────────────────────────────────────────────────────────────

def get_rol(conn: pyodbc.Connection, id_rol: int | None = None) -> list[dict]:
    cursor = conn.cursor()
    exec_sp(cursor,"EXEC sp_GetRol ?", id_rol)
    return rows_to_list(cursor)


def create_rol(conn: pyodbc.Connection, nombre: str, descripcion: str | None = None) -> dict | None:
    cursor = conn.cursor()
    exec_sp(cursor,"EXEC sp_InsertRol ?, ?", nombre, descripcion)
    result = row_to_dict(cursor)
    conn.commit()
    return result


def update_rol(conn: pyodbc.Connection, id_rol: int, nombre: str, descripcion: str | None = None) -> None:
    cursor = conn.cursor()
    exec_sp(cursor,"EXEC sp_UpdateRol ?, ?, ?", id_rol, nombre, descripcion)
    conn.commit()


def delete_rol(conn: pyodbc.Connection, id_rol: int) -> None:
    cursor = conn.cursor()
    exec_sp(cursor,"EXEC sp_DeleteRol ?", id_rol)
    conn.commit()


# ── TipoDocumentoCobro ─────────────────────────────────────────────────────────

def get_tipo_documento_cobro(conn: pyodbc.Connection, id_tipo_doc_cobro: int | None = None) -> list[dict]:
    cursor = conn.cursor()
    exec_sp(cursor,"EXEC sp_GetTipoDocumentoCobro ?", id_tipo_doc_cobro)
    return rows_to_list(cursor)


def create_tipo_documento_cobro(conn: pyodbc.Connection, nombre: str, descripcion: str | None = None) -> dict | None:
    cursor = conn.cursor()
    exec_sp(cursor,"EXEC sp_InsertTipoDocumentoCobro ?, ?", nombre, descripcion)
    result = row_to_dict(cursor)
    conn.commit()
    return result


def update_tipo_documento_cobro(conn: pyodbc.Connection, id_tipo_doc_cobro: int, nombre: str, descripcion: str | None = None) -> None:
    cursor = conn.cursor()
    exec_sp(cursor,"EXEC sp_UpdateTipoDocumentoCobro ?, ?, ?", id_tipo_doc_cobro, nombre, descripcion)
    conn.commit()


def delete_tipo_documento_cobro(conn: pyodbc.Connection, id_tipo_doc_cobro: int) -> None:
    cursor = conn.cursor()
    exec_sp(cursor,"EXEC sp_DeleteTipoDocumentoCobro ?", id_tipo_doc_cobro)
    conn.commit()


# ── TipoHabitacion ─────────────────────────────────────────────────────────────

def get_tipo_habitacion(conn: pyodbc.Connection, id_tipo_habitacion: int | None = None, nombre: str | None = None) -> list[dict]:
    cursor = conn.cursor()
    exec_sp(cursor,"EXEC sp_GetTipoHabitacion ?, ?", id_tipo_habitacion, nombre)
    return rows_to_list(cursor)


def create_tipo_habitacion(conn: pyodbc.Connection, nombre: str, descripcion: str | None = None,
                            capacidad_personas: int = 1, tarifa_base: float = 0.0) -> dict | None:
    cursor = conn.cursor()
    exec_sp(cursor,"EXEC sp_InsertTipoHabitacion ?, ?, ?, ?",
                   nombre, descripcion, capacidad_personas, tarifa_base)
    result = row_to_dict(cursor)
    conn.commit()
    return result


def update_tipo_habitacion(conn: pyodbc.Connection, id_tipo_habitacion: int, nombre: str,
                            descripcion: str | None = None, capacidad_personas: int = 1,
                            tarifa_base: float = 0.0) -> None:
    cursor = conn.cursor()
    exec_sp(cursor,"EXEC sp_UpdateTipoHabitacion ?, ?, ?, ?, ?",
                   id_tipo_habitacion, nombre, descripcion, capacidad_personas, tarifa_base)
    conn.commit()


def delete_tipo_habitacion(conn: pyodbc.Connection, id_tipo_habitacion: int) -> None:
    cursor = conn.cursor()
    exec_sp(cursor,"EXEC sp_DeleteTipoHabitacion ?", id_tipo_habitacion)
    conn.commit()