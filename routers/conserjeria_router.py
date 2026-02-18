from fastapi import APIRouter, Depends, HTTPException, status
import pyodbc

from dependencies import get_db, get_current_user
from schemas.conserjeria import OrdenConserjeriaCreate, OrdenConserjeriaUpdate, OrdenConserjeriaResponse
from schemas.common import MensajeResponse
from services.conserjeria_service import (
    get_ordenes_conserjeria, create_orden_conserjeria,
    update_orden_conserjeria, delete_orden_conserjeria
)

router = APIRouter(prefix="/conserjeria", tags=["Conserjería"])


@router.get("", response_model=list[OrdenConserjeriaResponse])
def listar_ordenes_conserjeria(
    id_orden_conserj: int | None = None,
    id_habitacion: int | None = None,
    id_personal: int | None = None,
    estado: int | None = None,
    conn: pyodbc.Connection = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    return get_ordenes_conserjeria(conn, id_orden_conserj, id_habitacion, id_personal, estado)


@router.get("/{id_orden_conserj}", response_model=OrdenConserjeriaResponse)
def obtener_orden_conserjeria(
    id_orden_conserj: int,
    conn: pyodbc.Connection = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    result = get_ordenes_conserjeria(conn, id_orden_conserj=id_orden_conserj)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Orden de conserjería no encontrada.")
    return result[0]


@router.post("", response_model=OrdenConserjeriaResponse, status_code=status.HTTP_201_CREATED)
def crear_orden_conserjeria(
    body: OrdenConserjeriaCreate,
    conn: pyodbc.Connection = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    result = create_orden_conserjeria(
        conn, body.id_personal, body.id_habitacion, body.fecha_inicio,
        body.precio, body.estado, body.id_reserva, body.fecha_fin, body.descripcion
    )
    if not result:
        raise HTTPException(status_code=500, detail="Error al crear la orden de conserjería.")
    return get_ordenes_conserjeria(conn, id_orden_conserj=result["id_orden_conserj"])[0]


@router.put("/{id_orden_conserj}", response_model=MensajeResponse)
def actualizar_orden_conserjeria(
    id_orden_conserj: int,
    body: OrdenConserjeriaUpdate,
    conn: pyodbc.Connection = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    existing = get_ordenes_conserjeria(conn, id_orden_conserj=id_orden_conserj)
    if not existing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Orden de conserjería no encontrada.")
    update_orden_conserjeria(
        conn, id_orden_conserj, body.id_personal, body.id_habitacion,
        body.fecha_inicio, body.precio, body.estado,
        body.id_reserva, body.fecha_fin, body.descripcion
    )
    return {"mensaje": "Orden de conserjería actualizada correctamente."}


@router.delete("/{id_orden_conserj}", response_model=MensajeResponse)
def eliminar_orden_conserjeria(
    id_orden_conserj: int,
    conn: pyodbc.Connection = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    existing = get_ordenes_conserjeria(conn, id_orden_conserj=id_orden_conserj)
    if not existing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Orden de conserjería no encontrada.")
    delete_orden_conserjeria(conn, id_orden_conserj)
    return {"mensaje": "Orden de conserjería eliminada correctamente."}