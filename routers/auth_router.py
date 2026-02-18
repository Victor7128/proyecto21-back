from fastapi import APIRouter, Depends, HTTPException, status
import pyodbc

from dependencies import get_db
from exceptions import UnauthorizedError
from schemas.auth import LoginRequest, TokenResponse
from services.auth_service import login

router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.post("/login", response_model=TokenResponse)
def iniciar_sesion(body: LoginRequest, conn: pyodbc.Connection = Depends(get_db)):
    """
    Recibe num_documento y password.
    Retorna un JWT Bearer token si las credenciales son válidas.
    """
    try:
        return login(conn, body.num_documento, body.password)
    except UnauthorizedError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))