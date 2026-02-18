from fastapi import APIRouter, Depends, HTTPException, status
import pyodbc

from dependencies import get_db, get_current_user
from schemas.documento import DocumentoCreate, DocumentoUpdate, DocumentoResponse
from schemas.common import MensajeResponse
from services.documento_service import get_documentos, create_documento, update_documento, delete_documento

router = APIRouter(prefix="/documentos", tags=["Documentos"])


@router.get("", response_model=list[DocumentoResponse])
def listar_documentos(
    id_documento: int | None = None,
    numero_documento: str | None = None,
    estado_documento: int | None = None,
    tipo_documento: int | None = None,
    conn: pyodbc.Connection = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    return get_documentos(conn, id_documento, numero_documento, estado_documento, tipo_documento)


@router.get("/{id_documento}", response_model=DocumentoResponse)
def obtener_documento(
    id_documento: int,
    conn: pyodbc.Connection = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    result = get_documentos(conn, id_documento=id_documento)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Documento no encontrado.")
    return result[0]


@router.post("", response_model=DocumentoResponse, status_code=status.HTTP_201_CREATED)
def crear_documento(
    body: DocumentoCreate,
    conn: pyodbc.Connection = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    """
    Crea un documento de cobro.
    Exactamente uno de id_reserva, id_orden_hospedaje o id_orden_conserjeria debe ser provisto
    (validado tanto en el schema como en el SP).
    """
    result = create_documento(
        conn, body.numero_documento, body.tipo_documento, body.monto_total,
        body.estado_documento, body.id_reserva, body.id_orden_hospedaje,
        body.id_orden_conserjeria, body.monto_pagado, body.fecha_vencimiento, body.descripcion
    )
    if not result:
        raise HTTPException(status_code=500, detail="Error al crear el documento.")
    return get_documentos(conn, id_documento=result["id_documento"])[0]


@router.put("/{id_documento}", response_model=MensajeResponse)
def actualizar_documento(
    id_documento: int,
    body: DocumentoUpdate,
    conn: pyodbc.Connection = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    """
    Actualiza monto_pagado, estado y campos opcionales.
    El origen (reserva/hospedaje/conserjería) y número de documento son inmutables.
    Nota: para registrar pagos usa el endpoint /pagos, que actualiza monto_pagado automáticamente.
    """
    existing = get_documentos(conn, id_documento=id_documento)
    if not existing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Documento no encontrado.")
    update_documento(conn, id_documento, body.monto_pagado, body.estado_documento,
                     body.fecha_vencimiento, body.descripcion)
    return {"mensaje": "Documento actualizado correctamente."}


@router.delete("/{id_documento}", response_model=MensajeResponse)
def eliminar_documento(
    id_documento: int,
    conn: pyodbc.Connection = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    existing = get_documentos(conn, id_documento=id_documento)
    if not existing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Documento no encontrado.")
    delete_documento(conn, id_documento)
    return {"mensaje": "Documento eliminado correctamente."}