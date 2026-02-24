from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
import pyodbc

from config import get_settings
from exceptions import UnauthorizedError
from services.personal_service import get_personal_by_email, verify_password as verify_personal_password
from services.huesped_service import get_huesped_by_email_login, verify_password as verify_huesped_password
from services.huesped_service import register_huesped as _register_huesped

settings = get_settings()


# ── Login de Personal (staff / administrador) ──────────────────────────────────

def login_personal(conn: pyodbc.Connection, email: str, password: str) -> dict:
    """
    Autentica a un miembro del personal.
    Llama a sp_LoginPersonal vía get_personal_by_email.
    El payload del JWT incluye tipo="personal", id_personal, id_rol y nombre_rol.
    """
    personal = get_personal_by_email(conn, email)

    if personal is None:
        raise UnauthorizedError("Credenciales inválidas.")

    if not personal["activo"]:
        raise UnauthorizedError("Usuario inactivo.")

    if not verify_personal_password(password, personal["password_hash"]):
        raise UnauthorizedError("Credenciales inválidas.")

    token = _crear_token({
        "sub":         str(personal["id_personal"]),
        "tipo":        "personal",
        "id_personal": int(personal["id_personal"]),   # ← cast
        "id_rol":      int(personal["id_rol"]),         # ← cast
        "nombre_rol":  personal.get("nombre_rol"),
    })

    return {"access_token": token, "token_type": "bearer", "tipo": "personal"}


# Alias para retrocompatibilidad con el router existente
def login(conn: pyodbc.Connection, email: str, password: str) -> dict:
    return login_personal(conn, email, password)


# ── Login de Huésped (portal web / móvil) ──────────────────────────────────────

def login_huesped(conn: pyodbc.Connection, email_login: str, password: str) -> dict:
    """
    Autentica a un huésped del portal.
    Llama a sp_LoginHuesped vía get_huesped_by_email_login.
    El payload del JWT incluye tipo="huesped" e id_huesped.
    """
    huesped = get_huesped_by_email_login(conn, email_login)

    if huesped is None:
        raise UnauthorizedError("Credenciales inválidas.")

    if not huesped["activo"]:
        raise UnauthorizedError("Cuenta inactiva. Contacte con recepción.")

    if not verify_huesped_password(password, huesped["password_hash"]):
        raise UnauthorizedError("Credenciales inválidas.")

    token = _crear_token({
        "sub":        str(huesped["id_huesped"]),
        "tipo":       "huesped",
        "id_huesped": int(huesped["id_huesped"]),       # ← cast
    })

    return {"access_token": token, "token_type": "bearer", "tipo": "huesped"}


# ── Registro de Huésped (auto-registro desde el portal) ────────────────────────

def registro_huesped(conn: pyodbc.Connection, nombres: str, apellidos: str,
                     tipo_documento: int, num_documento: str,
                     email_login: str, password: str,
                     telefono: str | None = None,
                     correo: str | None = None) -> dict:
    """
    Crea la cuenta del huésped y devuelve un JWT directamente,
    para que quede autenticado sin necesidad de un segundo login.
    """
    result = _register_huesped(
        conn, nombres, apellidos, tipo_documento, num_documento,
        email_login, password, telefono, correo
    )

    if result is None:
        raise UnauthorizedError("Error al registrar el huésped.")

    id_huesped = int(result["id_huesped"])

    token = _crear_token({
        "sub":        str(id_huesped),
        "tipo":       "huesped",
        "id_huesped": id_huesped,
    })

    return {
        "access_token": token,
        "token_type":   "bearer",
        "tipo":         "huesped",
        "id_huesped":   id_huesped,
        "nombres":      nombres,
        "apellidos":    apellidos,
    }


# ── Verificación del JWT (usada en dependencies.py) ────────────────────────────

def verificar_token(token: str) -> dict:
    """
    Decodifica y valida el JWT.
    Devuelve el payload con tipo + identificador primario.

    Para Personal → {"tipo": "personal", "id_personal": int, "id_rol": int, ...}
    Para Huésped  → {"tipo": "huesped",  "id_huesped":  int}
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError:
        raise UnauthorizedError("Token inválido o expirado.")

    tipo = payload.get("tipo")

    if tipo == "personal":
        id_personal = payload.get("id_personal")
        if id_personal is None:
            raise UnauthorizedError("Token inválido.")
        return {
            "tipo":        "personal",
            "id_personal": int(id_personal),
            "id_rol":      payload.get("id_rol"),
            "nombre_rol":  payload.get("nombre_rol"),
        }

    if tipo == "huesped":
        id_huesped = payload.get("id_huesped")
        if id_hueshed := id_huesped:  # noqa: F841 — simple check
            pass
        if id_huesped is None:
            raise UnauthorizedError("Token inválido.")
        return {
            "tipo":       "huesped",
            "id_huesped": int(id_huesped),
        }

    raise UnauthorizedError("Token inválido: tipo de usuario desconocido.")


# ── Helper interno ─────────────────────────────────────────────────────────────

def _crear_token(data: dict) -> str:
    payload = data.copy()
    expira = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload["exp"] = expira
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)