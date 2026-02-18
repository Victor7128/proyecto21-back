from fastapi import APIRouter, Depends, HTTPException, status
import pyodbc

from dependencies import get_db, get_current_user
from schemas.encuesta import EncuestaCreate, EncuestaUpdate, EncuestaResponse
from schemas.common import MensajeResponse
from services.encuesta_service import get_encuestas, create_encuesta, update_encuesta, delete_encuesta

router = APIRouter(prefix="/encuestas", tags=["Encuestas"])


@router.get("", response_model=list[EncuestaResponse])
def listar_encuestas(
    id_encuesta: int | None = None,
    id_orden_hospedaje: int | None = None,
    motivo_viaje: str | None = None,
    conn: pyodbc.Connection = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    return get_encuestas(conn, id_encuesta, id_orden_hospedaje, motivo_viaje)


@router.get("/{id_encuesta}", response_model=EncuestaResponse)
def obtener_encuesta(
    id_encuesta: int,
    conn: pyodbc.Connection = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    result = get_encuestas(conn, id_encuesta=id_encuesta)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Encuesta no encontrada.")
    return result[0]


@router.post("", response_model=EncuestaResponse, status_code=status.HTTP_201_CREATED)
def crear_encuesta(
    body: EncuestaCreate,
    conn: pyodbc.Connection = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    """
    Crea una encuesta de satisfacción post-estancia.
    Solo puede existir una encuesta por orden de hospedaje (validado por el SP).
    """
    result = create_encuesta(
        conn, body.id_orden_hospedaje, body.recomendacion, body.descripcion,
        body.lugar_origen, body.motivo_viaje, body.calificacion_limpieza,
        body.calificacion_servicio, body.calificacion_ubicacion,
        body.calificacion_precio, body.comentarios
    )
    if not result:
        raise HTTPException(status_code=500, detail="Error al crear la encuesta.")
    return get_encuestas(conn, id_encuesta=result["id_encuesta"])[0]


@router.put("/{id_encuesta}", response_model=MensajeResponse)
def actualizar_encuesta(
    id_encuesta: int,
    body: EncuestaUpdate,
    conn: pyodbc.Connection = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    existing = get_encuestas(conn, id_encuesta=id_encuesta)
    if not existing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Encuesta no encontrada.")
    update_encuesta(
        conn, id_encuesta, body.recomendacion, body.descripcion, body.lugar_origen,
        body.motivo_viaje, body.calificacion_limpieza, body.calificacion_servicio,
        body.calificacion_ubicacion, body.calificacion_precio, body.comentarios
    )
    return {"mensaje": "Encuesta actualizada correctamente."}


@router.delete("/{id_encuesta}", response_model=MensajeResponse)
def eliminar_encuesta(
    id_encuesta: int,
    conn: pyodbc.Connection = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    existing = get_encuestas(conn, id_encuesta=id_encuesta)
    if not existing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Encuesta no encontrada.")
    delete_encuesta(conn, id_encuesta)
    return {"mensaje": "Encuesta eliminada correctamente."}