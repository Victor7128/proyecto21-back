from fastapi import APIRouter, Depends, HTTPException, status
import pyodbc

from dependencies import get_db, get_current_user
from schemas.huesped import HuespedCreate, HuespedUpdate, HuespedCambioPassword, HuespedResponse
from schemas.common import MensajeResponse
from services.huesped_service import (
    get_huespedes, create_huesped, update_huesped, delete_huesped,
    get_huesped_by_email_login, cambiar_password_huesped, verify_password,
)

router = APIRouter(prefix="/huespedes", tags=["Huéspedes"])


@router.get("", response_model=list[HuespedResponse])
def listar_huespedes(
    id_huesped: int | None = None,
    num_documento: str | None = None,
    nombre: str | None = None,
    conn: pyodbc.Connection = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    return get_huespedes(conn, id_huesped, num_documento, nombre)


@router.get("/{id_huesped}", response_model=HuespedResponse)
def obtener_huesped(
    id_huesped: int,
    conn: pyodbc.Connection = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    result = get_huespedes(conn, id_huesped=id_huesped)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Huésped no encontrado.")
    return result[0]


@router.post("", response_model=HuespedResponse, status_code=status.HTTP_201_CREATED)
def crear_huesped(
    body: HuespedCreate,
    conn: pyodbc.Connection = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Registro manual de huésped por parte del personal.
    Solo accesible con token de tipo 'personal'.
    Los campos email_login y password son opcionales:
    si se proveen, el huésped quedará con acceso al portal.
    """
    if current_user.get("tipo") != "personal":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo el personal puede registrar huéspedes manualmente."
        )
    result = create_huesped(
        conn,
        body.nombres, body.apellidos,
        body.tipo_documento, body.num_documento,
        body.telefono, body.correo,
        body.email_login, body.password,
    )
    if not result:
        raise HTTPException(status_code=500, detail="Error al crear el huésped.")
    return get_huespedes(conn, id_huesped=result["id_huesped"])[0]


@router.put("/{id_huesped}", response_model=MensajeResponse)
def actualizar_huesped(
    id_huesped: int,
    body: HuespedUpdate,
    conn: pyodbc.Connection = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Actualiza datos personales del huésped.
    El personal puede editar cualquier huésped.
    Un huésped autenticado solo puede editar su propio perfil.
    """
    existing = get_huespedes(conn, id_huesped=id_huesped)
    if not existing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Huésped no encontrado.")

    if current_user.get("tipo") == "huesped" and current_user["id_huesped"] != id_huesped:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para editar el perfil de otro huésped."
        )

    update_huesped(
        conn, id_huesped,
        body.nombres, body.apellidos,
        body.tipo_documento, body.num_documento,
        body.telefono, body.correo,
    )
    return {"mensaje": "Huésped actualizado correctamente."}


@router.delete("/{id_huesped}", response_model=MensajeResponse)
def eliminar_huesped(
    id_huesped: int,
    conn: pyodbc.Connection = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Borrado lógico del huésped (activo = 0).
    Solo accesible con token de tipo 'personal'.
    """
    if current_user.get("tipo") != "personal":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo el personal puede desactivar huéspedes."
        )
    existing = get_huespedes(conn, id_huesped=id_huesped)
    if not existing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Huésped no encontrado.")
    delete_huesped(conn, id_huesped)
    return {"mensaje": "Huésped desactivado correctamente."}


@router.put("/{id_huesped}/password", response_model=MensajeResponse)
def cambiar_password(
    id_huesped: int,
    body: HuespedCambioPassword,
    conn: pyodbc.Connection = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Cambia la contraseña del huésped.
    Solo el propio huésped autenticado puede cambiar su contraseña.
    """
    if current_user.get("tipo") != "huesped" or current_user["id_huesped"] != id_huesped:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo el propio huésped puede cambiar su contraseña."
        )

    existing = get_huespedes(conn, id_huesped=id_huesped)
    if not existing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Huésped no encontrado.")

    # Verificar que tiene cuenta con credenciales
    huesped_auth = get_huesped_by_email_login(conn, existing[0]["email_login"])
    if not huesped_auth or not huesped_auth.get("password_hash"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este huésped no tiene una cuenta con contraseña registrada."
        )

    if not verify_password(body.password_actual, huesped_auth["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La contraseña actual es incorrecta."
        )

    cambiar_password_huesped(conn, id_huesped, body.password_nuevo)
    return {"mensaje": "Contraseña actualizada correctamente."}