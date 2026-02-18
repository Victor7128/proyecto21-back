from fastapi import APIRouter, Depends, HTTPException, status
import pyodbc

from dependencies import get_db, get_current_user
from schemas.hospedaje import OrdenHospedajeCreate, OrdenHospedajeUpdate, OrdenHospedajeResponse
from schemas.common import MensajeResponse
from services.hospedaje_service import (
    get_ordenes_hospedaje, create_orden_hospedaje,
    update_orden_hospedaje, delete_orden_hospedaje
)

router = APIRouter(prefix="/hospedaje", tags=["Hospedaje"])


@router.get("", response_model=list[OrdenHospedajeResponse])
def listar_ordenes_hospedaje(
    id_orden_hospedaje: int | None = None,
    id_reserva: int | None = None,
    estado: int | None = None,
    conn: pyodbc.Connection = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    return get_ordenes_hospedaje(conn, id_orden_hospedaje, id_reserva, estado)


@router.get("/{id_orden_hospedaje}", response_model=OrdenHospedajeResponse)
def obtener_orden_hospedaje(
    id_orden_hospedaje: int,
    conn: pyodbc.Connection = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    result = get_ordenes_hospedaje(conn, id_orden_hospedaje=id_orden_hospedaje)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Orden de hospedaje no encontrada.")
    return result[0]


@router.post("", response_model=OrdenHospedajeResponse, status_code=status.HTTP_201_CREATED)
def crear_orden_hospedaje(
    body: OrdenHospedajeCreate,
    conn: pyodbc.Connection = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    result = create_orden_hospedaje(conn, body.id_reserva, body.estado, body.fecha_checkin, body.fecha_checkout)
    if not result:
        raise HTTPException(status_code=500, detail="Error al crear la orden de hospedaje.")
    return get_ordenes_hospedaje(conn, id_orden_hospedaje=result["id_orden_hospedaje"])[0]


@router.put("/{id_orden_hospedaje}", response_model=MensajeResponse)
def actualizar_orden_hospedaje(
    id_orden_hospedaje: int,
    body: OrdenHospedajeUpdate,
    conn: pyodbc.Connection = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    existing = get_ordenes_hospedaje(conn, id_orden_hospedaje=id_orden_hospedaje)
    if not existing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Orden de hospedaje no encontrada.")
    update_orden_hospedaje(conn, id_orden_hospedaje, body.estado, body.fecha_checkin, body.fecha_checkout)
    return {"mensaje": "Orden de hospedaje actualizada correctamente."}


@router.delete("/{id_orden_hospedaje}", response_model=MensajeResponse)
def eliminar_orden_hospedaje(
    id_orden_hospedaje: int,
    conn: pyodbc.Connection = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    existing = get_ordenes_hospedaje(conn, id_orden_hospedaje=id_orden_hospedaje)
    if not existing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Orden de hospedaje no encontrada.")
    delete_orden_hospedaje(conn, id_orden_hospedaje)
    return {"mensaje": "Orden de hospedaje eliminada correctamente."}