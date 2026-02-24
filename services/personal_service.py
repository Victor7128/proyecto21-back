import pyodbc
import bcrypt
from fastapi import HTTPException
from services.utils import rows_to_list, row_to_dict, exec_sp

# ── Helpers de contraseña ──────────────────────────────────────────────────────

def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

def verify_password(plain: str, hashed_bytes: bytes) -> bool:
    try:
        return bcrypt.checkpw(plain.encode("utf-8"), hashed_bytes)
    except Exception:
        return False


# ── CRUD estándar ──────────────────────────────────────────────────────────────

def get_personal(conn: pyodbc.Connection, id_personal: int | None = None,
                 nombre: str | None = None, id_rol: int | None = None,
                 activo: bool | None = None) -> list[dict]:
    cursor = conn.cursor()
    exec_sp(cursor, "EXEC sp_GetPersonal ?, ?, ?, ?", id_personal, nombre, id_rol, activo)
    return rows_to_list(cursor)


def create_personal(conn: pyodbc.Connection, nombre: str, tipo_documento: int,
                    num_documento: str, email: str | None = None,
                    password: str | None = None, id_rol: int | None = None,
                    activo: bool = True) -> dict | None:
    if not password:
        raise HTTPException(status_code=400, detail="La contraseña es requerida.")
    password_hash = hash_password(password)
    cursor = conn.cursor()
    exec_sp(cursor,
        "EXEC sp_InsertPersonal ?, ?, ?, ?, ?, ?, ?",
        nombre, tipo_documento, num_documento, email, password_hash, id_rol, activo
    )
    result = row_to_dict(cursor)
    conn.commit()
    return result


def update_personal(conn: pyodbc.Connection, id_personal: int, nombre: str,
                    tipo_documento: int, num_documento: str, email: str | None = None,
                    id_rol: int | None = None, activo: bool = True) -> None:
    cursor = conn.cursor()
    exec_sp(cursor,
        "EXEC sp_UpdatePersonal ?, ?, ?, ?, ?, ?, ?",
        id_personal, nombre, tipo_documento, num_documento, email, id_rol, activo
    )
    conn.commit()


def delete_personal(conn: pyodbc.Connection, id_personal: int) -> None:
    """Borrado lógico: el SP hace UPDATE activo = 0, no DELETE físico."""
    cursor = conn.cursor()
    exec_sp(cursor, "EXEC sp_DeletePersonal ?", id_personal)
    conn.commit()


# ── Auth de personal ───────────────────────────────────────────────────────────

def get_personal_by_email(conn: pyodbc.Connection, email: str) -> dict | None:
    """
    Recupera los datos necesarios para verificar el login del personal.
    Ahora usa sp_LoginPersonal en vez de SQL inline, para incluir nombre_rol
    en el resultado y así poblar el JWT sin un query extra.
    """
    cursor = conn.cursor()
    exec_sp(cursor, "EXEC sp_LoginPersonal ?", email)
    return row_to_dict(cursor)


def update_password(conn: pyodbc.Connection, id_personal: int, new_password: str) -> None:
    """
    Actualiza el hash de contraseña del personal.
    Ahora usa sp_CambiarPasswordPersonal en vez de SQL inline,
    consistente con el patrón del resto de services.
    """
    password_hash = hash_password(new_password)
    cursor = conn.cursor()
    exec_sp(cursor, "EXEC sp_CambiarPasswordPersonal ?, ?", id_personal, password_hash)
    conn.commit()