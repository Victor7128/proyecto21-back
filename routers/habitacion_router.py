from fastapi import APIRouter, Depends, HTTPException, status
import pyodbc

from dependencies import get_db, get_current_user
from schemas.habitacion import HabitacionCreate, HabitacionUpdate, HabitacionResponse
from schemas.common import MensajeResponse
from services.habitacion_service import get_habitaciones, create_habitacion, update_habitacion, delete_habitacion

router = APIRouter(prefix="/habitaciones", tags=["Habitaciones"])


@router.get("", response_model=list[HabitacionResponse])
def listar_habitaciones(
    id_habitacion: int | None = None,
    piso: int | None = None,
    estado: int | None = None,
    id_tipo_habitacion: int | None = None,
    conn: pyodbc.Connection = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    return get_habitaciones(conn, id_habitacion, piso, estado, id_tipo_habitacion)


@router.get("/{id_habitacion}", response_model=HabitacionResponse)
def obtener_habitacion(
    id_habitacion: int,
    conn: pyodbc.Connection = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    result = get_habitaciones(conn, id_habitacion=id_habitacion)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Habitación no encontrada.")
    return result[0]


@router.post("", response_model=HabitacionResponse, status_code=status.HTTP_201_CREATED)
def crear_habitacion(
    body: HabitacionCreate,
    conn: pyodbc.Connection = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    result = create_habitacion(conn, body.numero, body.piso, body.id_tipo_habitacion, body.estado)
    if not result:
        raise HTTPException(status_code=500, detail="Error al crear la habitación.")
    return get_habitaciones(conn, id_habitacion=result["id_habitacion"])[0]


@router.put("/{id_habitacion}", response_model=MensajeResponse)
def actualizar_habitacion(
    id_habitacion: int,
    body: HabitacionUpdate,
    conn: pyodbc.Connection = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    existing = get_habitaciones(conn, id_habitacion=id_habitacion)
    if not existing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Habitación no encontrada.")
    update_habitacion(conn, id_habitacion, body.numero, body.piso, body.id_tipo_habitacion, body.estado)
    return {"mensaje": "Habitación actualizada correctamente."}


@router.delete("/{id_habitacion}", response_model=MensajeResponse)
def eliminar_habitacion(
    id_habitacion: int,
    conn: pyodbc.Connection = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    existing = get_habitaciones(conn, id_habitacion=id_habitacion)
    if not existing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Habitación no encontrada.")
    delete_habitacion(conn, id_habitacion)
    return {"mensaje": "Habitación eliminada correctamente."}