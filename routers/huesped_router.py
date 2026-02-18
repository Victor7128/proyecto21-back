from fastapi import APIRouter, Depends, HTTPException, status
import pyodbc

from dependencies import get_db, get_current_user
from schemas.huesped import HuespedCreate, HuespedUpdate, HuespedResponse
from schemas.common import MensajeResponse
from services.huesped_service import get_huespedes, create_huesped, update_huesped, delete_huesped

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
    _: dict = Depends(get_current_user),
):
    result = create_huesped(
        conn, body.nombres, body.apellidos, body.tipo_documento,
        body.num_documento, body.telefono, body.correo
    )
    if not result:
        raise HTTPException(status_code=500, detail="Error al crear el huésped.")
    return get_huespedes(conn, id_huesped=result["id_huesped"])[0]


@router.put("/{id_huesped}", response_model=MensajeResponse)
def actualizar_huesped(
    id_huesped: int,
    body: HuespedUpdate,
    conn: pyodbc.Connection = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    existing = get_huespedes(conn, id_huesped=id_huesped)
    if not existing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Huésped no encontrado.")
    update_huesped(
        conn, id_huesped, body.nombres, body.apellidos, body.tipo_documento,
        body.num_documento, body.telefono, body.correo
    )
    return {"mensaje": "Huésped actualizado correctamente."}


@router.delete("/{id_huesped}", response_model=MensajeResponse)
def eliminar_huesped(
    id_huesped: int,
    conn: pyodbc.Connection = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    existing = get_huespedes(conn, id_huesped=id_huesped)
    if not existing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Huésped no encontrado.")
    delete_huesped(conn, id_huesped)
    return {"mensaje": "Huésped eliminado correctamente."}