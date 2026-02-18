from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
import pyodbc

from config import get_settings
from exceptions import UnauthorizedError
from services.personal_service import get_personal_by_email, verify_password

settings = get_settings()


def login(conn: pyodbc.Connection, email: str, password: str) -> dict:
    personal = get_personal_by_email(conn, email)

    if personal is None:
        raise UnauthorizedError("Credenciales inválidas.")

    if not personal["activo"]:
        raise UnauthorizedError("Usuario inactivo.")

    if not verify_password(password, personal["password_hash"]):
        raise UnauthorizedError("Credenciales inválidas.")

    token = _crear_token({
        "sub": str(personal["id_personal"]),
        "rol": str(personal["id_rol"]),
    })

    return {"access_token": token, "token_type": "bearer"}


def _crear_token(data: dict) -> str:
    payload = data.copy()
    expira = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload.update({"exp": expira})
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def verificar_token(token: str) -> dict:
    """
    Decodifica y valida el JWT.
    Devuelve el payload con id_personal y rol.
    Usado en dependencies.py para proteger rutas.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        id_personal = payload.get("sub")
        rol = payload.get("rol")
        if id_personal is None:
            raise UnauthorizedError("Token inválido.")
        return {"id_personal": int(id_personal), "rol": rol}
    except JWTError:
        raise UnauthorizedError("Token inválido o expirado.")