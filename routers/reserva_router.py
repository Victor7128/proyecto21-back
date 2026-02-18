from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status
import pyodbc

from dependencies import get_db, get_current_user
from schemas.reserva import ReservaCreate, ReservaUpdate, ReservaResponse
from schemas.common import MensajeResponse
from services.reserva_service import get_reservas, create_reserva, update_reserva, delete_reserva

router = APIRouter(prefix="/reservas", tags=["Reservas"])


@router.get("", response_model=list[ReservaResponse])
def listar_reservas(
    id_reserva: int | None = None,
    id_huesped: int | None = None,
    id_habitacion: int | None = None,
    estado: int | None = None,
    fecha_entrada: date | None = None,
    fecha_salida: date | None = None,
    conn: pyodbc.Connection = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    return get_reservas(conn, id_reserva, id_huesped, id_habitacion, estado, fecha_entrada, fecha_salida)


@router.get("/{id_reserva}", response_model=ReservaResponse)
def obtener_reserva(
    id_reserva: int,
    conn: pyodbc.Connection = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    result = get_reservas(conn, id_reserva=id_reserva)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reserva no encontrada.")
    return result[0]


@router.post("", response_model=ReservaResponse, status_code=status.HTTP_201_CREATED)
def crear_reserva(
    body: ReservaCreate,
    conn: pyodbc.Connection = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    result = create_reserva(
        conn, body.id_huesped, body.id_habitacion, body.fecha_entrada,
        body.fecha_salida, body.num_personas, body.monto_total, body.estado
    )
    if not result:
        raise HTTPException(status_code=500, detail="Error al crear la reserva.")
    return get_reservas(conn, id_reserva=result["id_reserva"])[0]


@router.put("/{id_reserva}", response_model=MensajeResponse)
def actualizar_reserva(
    id_reserva: int,
    body: ReservaUpdate,
    conn: pyodbc.Connection = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    existing = get_reservas(conn, id_reserva=id_reserva)
    if not existing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reserva no encontrada.")
    update_reserva(
        conn, id_reserva, body.id_huesped, body.id_habitacion, body.fecha_entrada,
        body.fecha_salida, body.num_personas, body.monto_total, body.estado
    )
    return {"mensaje": "Reserva actualizada correctamente."}


@router.delete("/{id_reserva}", response_model=MensajeResponse)
def eliminar_reserva(
    id_reserva: int,
    conn: pyodbc.Connection = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    existing = get_reservas(conn, id_reserva=id_reserva)
    if not existing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reserva no encontrada.")
    delete_reserva(conn, id_reserva)
    return {"mensaje": "Reserva eliminada correctamente."}