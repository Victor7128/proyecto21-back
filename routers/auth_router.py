from fastapi import APIRouter, Depends, HTTPException, status
import pyodbc

from dependencies import get_db
from exceptions import UnauthorizedError
from schemas.auth import PersonalLoginRequest, HuespedLoginRequest, TokenResponse, RegistroHuespedResponse
from schemas.huesped import HuespedRegistro
from services.auth_service import login_personal, login_huesped, registro_huesped

router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.post("/login", response_model=TokenResponse)
def iniciar_sesion_personal(
    body: PersonalLoginRequest,
    conn: pyodbc.Connection = Depends(get_db),
):
    """
    Login para Personal (recepcionistas, administradores, etc.).
    Recibe email + password.
    El JWT devuelto incluye tipo='personal', id_personal, id_rol y nombre_rol.
    """
    try:
        return login_personal(conn, body.email, body.password)
    except UnauthorizedError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@router.post("/login/huesped", response_model=TokenResponse)
def iniciar_sesion_huesped(
    body: HuespedLoginRequest,
    conn: pyodbc.Connection = Depends(get_db),
):
    """
    Login para Huéspedes desde el portal web/móvil.
    Recibe email_login + password.
    El JWT devuelto incluye tipo='huesped' e id_huesped.
    Solo funciona si el huésped tiene cuenta (email_login registrado).
    """
    try:
        return login_huesped(conn, body.email_login, body.password)
    except UnauthorizedError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@router.post("/registro", response_model=RegistroHuespedResponse, status_code=status.HTTP_201_CREATED)
def registrar_huesped(
    body: HuespedRegistro,
    conn: pyodbc.Connection = Depends(get_db),
):
    """
    Auto-registro de huésped desde el portal web/móvil.
    Crea la cuenta y devuelve el JWT directamente,
    para que el usuario quede autenticado sin un segundo login.
    No requiere autenticación previa.
    """
    try:
        return registro_huesped(
            conn,
            body.nombres, body.apellidos,
            body.tipo_documento, body.num_documento,
            body.email_login, body.password,
            body.telefono, body.correo,
        )
    except UnauthorizedError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))