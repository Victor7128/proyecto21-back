"""
Dependencias compartidas para los routers de FastAPI.
"""
import pyodbc
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from config import get_settings
from exceptions import UnauthorizedError
from services.auth_service import verificar_token

settings = get_settings()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Connection string construido desde las variables del .env
# Driver compatible con Azure SQL Server y SQL Server local
_CONNECTION_STRING = (
    f"DRIVER={{ODBC Driver 18 for SQL Server}};"
    f"SERVER={settings.DB_SERVER},{settings.DB_PORT};"
    f"DATABASE={settings.DB_NAME};"
    f"UID={settings.DB_USER};"
    f"PWD={settings.DB_PASSWORD};"
    f"Encrypt=yes;"
    f"TrustServerCertificate=no;"
    f"Connection Timeout=30;"
)


def get_db():
    """
    Abre una conexión pyodbc y la cierra al finalizar la request.
    Usar con Depends(get_db).
    """
    conn = pyodbc.connect(_CONNECTION_STRING)
    try:
        yield conn
    finally:
        conn.close()


def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    """
    Verifica el JWT y retorna {"id_personal": int, "rol": str}.
    Lanza 401 si el token es inválido o expirado.
    """
    try:
        return verificar_token(token)
    except UnauthorizedError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )