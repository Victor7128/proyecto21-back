import pyodbc
from fastapi import HTTPException
from passlib.context import CryptContext
from services.utils import rows_to_list, row_to_dict, exec_sp

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> bytes:
    """Hashea la contraseña con bcrypt y la devuelve en bytes para VARBINARY."""
    return pwd_context.hash(password).encode("utf-8")


def verify_password(plain: str, hashed_bytes: bytes) -> bool:
    decoded = hashed_bytes.decode("utf-8")
    # Si no es un hash bcrypt válido, comparar directo
    try:
        return pwd_context.verify(plain, decoded)
    except Exception:
        return plain == decoded


def get_personal(conn: pyodbc.Connection, id_personal: int | None = None, nombre: str | None = None,
                 id_rol: int | None = None, activo: bool | None = None) -> list[dict]:
    cursor = conn.cursor()
    # pyodbc convierte bool a bit automáticamente; None pasa como NULL
    exec_sp(cursor,"EXEC sp_GetPersonal ?, ?, ?, ?", id_personal, nombre, id_rol, activo)
    return rows_to_list(cursor)


def create_personal(conn: pyodbc.Connection, nombre: str, tipo_documento: int,
                    num_documento: str, email: str | None = None, password: str | None = None,
                    id_rol: int | None = None, activo: bool = True) -> dict | None:
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
    exec_sp(cursor,"EXEC sp_DeletePersonal ?", id_personal)
    conn.commit()


def get_personal_by_email(conn: pyodbc.Connection, email: str) -> dict | None:
    cursor = conn.cursor()
    exec_sp(cursor,
        "SELECT id_personal, nombre, email, password_hash, id_rol, activo "
        "FROM Personal WHERE email = ?",
        email
    )
    return row_to_dict(cursor)

def update_password(conn: pyodbc.Connection, id_personal: int, new_password: str) -> None:
    password_hash = hash_password(new_password)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE Personal SET password_hash = ? WHERE id_personal = ?",
        password_hash, id_personal
    )
    conn.commit()