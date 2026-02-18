from fastapi import APIRouter, Depends, HTTPException, status
import pyodbc

from dependencies import get_db, get_current_user
from schemas.personal import (
    PersonalCreate, PersonalUpdate, PersonalCambioPassword, PersonalResponse
)
from schemas.common import MensajeResponse
from services.personal_service import (
    get_personal, create_personal, update_personal, delete_personal,
    update_password, verify_password
)

router = APIRouter(prefix="/personal", tags=["Personal"])


@router.get("", response_model=list[PersonalResponse])
def listar_personal(
    id_personal: int | None = None,
    nombre: str | None = None,
    id_rol: int | None = None,
    activo: bool | None = None,
    conn: pyodbc.Connection = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    return get_personal(conn, id_personal, nombre, id_rol, activo)


@router.get("/{id_personal}", response_model=PersonalResponse)
def obtener_personal(
    id_personal: int,
    conn: pyodbc.Connection = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    result = get_personal(conn, id_personal=id_personal)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Personal no encontrado.")
    return result[0]


@router.post("", response_model=PersonalResponse, status_code=status.HTTP_201_CREATED)
def crear_personal(
    body: PersonalCreate,
    conn: pyodbc.Connection = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    result = create_personal(
        conn, body.nombre, body.tipo_documento, body.num_documento,
        body.email, body.password, body.id_rol, body.activo
    )
    if not result:
        raise HTTPException(status_code=500, detail="Error al crear el personal.")
    return get_personal(conn, id_personal=result["id_personal"])[0]


@router.put("/{id_personal}", response_model=MensajeResponse)
def actualizar_personal(
    id_personal: int,
    body: PersonalUpdate,
    conn: pyodbc.Connection = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    existing = get_personal(conn, id_personal=id_personal)
    if not existing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Personal no encontrado.")
    update_personal(
        conn, id_personal, body.nombre, body.tipo_documento,
        body.num_documento, body.email, body.id_rol, body.activo
    )
    return {"mensaje": "Personal actualizado correctamente."}


@router.delete("/{id_personal}", response_model=MensajeResponse)
def eliminar_personal(
    id_personal: int,
    conn: pyodbc.Connection = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    existing = get_personal(conn, id_personal=id_personal)
    if not existing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Personal no encontrado.")
    delete_personal(conn, id_personal)
    return {"mensaje": "Personal desactivado correctamente."}


@router.put("/{id_personal}/password", response_model=MensajeResponse)
def cambiar_password(
    id_personal: int,
    body: PersonalCambioPassword,
    conn: pyodbc.Connection = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Cambia la contraseña del personal.
    Solo puede cambiarse por el propio usuario o por un administrador.
    """
    # Verificar que el personal existe
    existing = get_personal(conn, id_personal=id_personal)
    if not existing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Personal no encontrado.")

    # Solo el propio usuario puede cambiar su contraseña (o admins, si aplica tu lógica de roles)
    if current_user["id_personal"] != id_personal:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para cambiar la contraseña de otro usuario."
        )

    # Obtener el hash actual directamente de la BD para verificación
    cursor = conn.cursor()
    cursor.execute(
        "SELECT password_hash FROM Personal WHERE id_personal = ?", id_personal
    )
    row = cursor.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Personal no encontrado.")

    password_hash_actual = row[0]
    if not verify_password(body.password_actual, password_hash_actual):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La contraseña actual es incorrecta."
        )

    update_password(conn, id_personal, body.password_nuevo)
    return {"mensaje": "Contraseña actualizada correctamente."}