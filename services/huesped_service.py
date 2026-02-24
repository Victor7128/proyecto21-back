from typing import Optional
import pyodbc
from passlib.context import CryptContext
from fastapi import HTTPException

from services.utils import rows_to_list, row_to_dict, exec_sp

# Reutiliza el mismo contexto bcrypt que personal_service
# para no tener dos instancias distintas en memoria.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ── Helpers de contraseña ──────────────────────────────────────────────────────

def hash_password(password: str) -> bytes:
    """Hashea con bcrypt y devuelve bytes para VARBINARY(MAX)."""
    return pwd_context.hash(password).encode("utf-8")


def verify_password(plain: str, hashed_bytes: bytes) -> bool:
    try:
        return pwd_context.verify(plain, hashed_bytes.decode("utf-8"))
    except Exception:
        return False


# ── CRUD estándar ──────────────────────────────────────────────────────────────

def get_huespedes(conn: pyodbc.Connection, id_huesped: int | None = None,
                  num_documento: str | None = None, nombre: str | None = None) -> list[dict]:
    cursor = conn.cursor()
    exec_sp(cursor, "EXEC sp_GetHuesped ?, ?, ?", id_huesped, num_documento, nombre)
    return rows_to_list(cursor)


def create_huesped(conn: pyodbc.Connection, nombres: str, apellidos: str,
                   tipo_documento: int, num_documento: str,
                   telefono: str | None = None, correo: str | None = None,
                   email_login: str | None = None,
                   password: str | None = None) -> dict | None:
    """
    Registro manual por recepción.
    Si se proveen email_login + password se crea la cuenta del portal.
    Ambos deben venir juntos o ninguno (validado también en el SP).
    """
    # Validar par coherente antes de llamar al SP
    if (email_login is None) != (password is None):
        raise HTTPException(
            status_code=400,
            detail="Debe proveer email_login y password juntos, o ninguno."
        )

    password_hash: bytes | None = hash_password(password) if password else None

    cursor = conn.cursor()
    exec_sp(cursor,
        "EXEC sp_InsertHuesped ?, ?, ?, ?, ?, ?, ?, ?",
        nombres, apellidos, tipo_documento, num_documento,
        telefono, correo, email_login, password_hash
    )
    result = row_to_dict(cursor)
    conn.commit()
    return result


def update_huesped(conn: pyodbc.Connection, id_huesped: int, nombres: str, apellidos: str,
                   tipo_documento: int, num_documento: str,
                   telefono: str | None = None, correo: str | None = None) -> None:
    """
    Actualiza solo datos personales.
    Credenciales se gestionan exclusivamente con cambiar_password_huesped.
    """
    cursor = conn.cursor()
    exec_sp(cursor,
        "EXEC sp_UpdateHuesped ?, ?, ?, ?, ?, ?, ?",
        id_huesped, nombres, apellidos, tipo_documento, num_documento, telefono, correo
    )
    conn.commit()


def delete_huesped(conn: pyodbc.Connection, id_huesped: int) -> None:
    """Borrado lógico: el SP hace UPDATE activo = 0."""
    cursor = conn.cursor()
    exec_sp(cursor, "EXEC sp_DeleteHuesped ?", id_huesped)
    conn.commit()


# ── Auth de huésped ────────────────────────────────────────────────────────────

def register_huesped(conn: pyodbc.Connection, nombres: str, apellidos: str,
                     tipo_documento: int, num_documento: str,
                     email_login: str, password: str,
                     telefono: str | None = None,
                     correo: str | None = None) -> dict | None:
    """
    Auto-registro desde el portal web/móvil.
    Las credenciales son OBLIGATORIAS (llama a sp_RegistrarHuesped).
    Devuelve el id_huesped para que auth_service construya el JWT.
    """
    password_hash = hash_password(password)
    cursor = conn.cursor()
    exec_sp(cursor,
        "EXEC sp_RegistrarHuesped ?, ?, ?, ?, ?, ?, ?, ?",
        nombres, apellidos, tipo_documento, num_documento,
        email_login, password_hash, telefono, correo
    )
    result = row_to_dict(cursor)
    conn.commit()
    return result


def get_huesped_by_email_login(conn: pyodbc.Connection, email_login: str) -> dict | None:
    """
    Recupera los datos necesarios para verificar el login de un huésped.
    Llama a sp_LoginHuesped → devuelve id_huesped, password_hash, activo.
    La verificación del hash se hace en auth_service, no aquí.
    """
    cursor = conn.cursor()
    exec_sp(cursor, "EXEC sp_LoginHuesped ?", email_login)
    return row_to_dict(cursor)


def cambiar_password_huesped(conn: pyodbc.Connection,
                              id_huesped: int, new_password: str) -> None:
    """
    Actualiza el hash de contraseña de un huésped.
    La verificación de la contraseña actual debe hacerse ANTES de llamar a esta función.
    """
    password_hash = hash_password(new_password)
    cursor = conn.cursor()
    exec_sp(cursor, "EXEC sp_CambiarPasswordHuesped ?, ?", id_huesped, password_hash)
    conn.commit()