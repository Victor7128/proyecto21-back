from fastapi import APIRouter, Depends, HTTPException, status
import pyodbc

from dependencies import get_db, get_current_user
from schemas.pago import PagoCreate, PagoUpdate, PagoResponse
from schemas.common import MensajeResponse
from services.pago_service import get_pagos, create_pago, update_pago, delete_pago

router = APIRouter(prefix="/pagos", tags=["Pagos"])


@router.get("", response_model=list[PagoResponse])
def listar_pagos(
    id_pago: int | None = None,
    id_documento: int | None = None,
    estado_pago: int | None = None,
    metodo: int | None = None,
    conn: pyodbc.Connection = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    return get_pagos(conn, id_pago, id_documento, estado_pago, metodo)


@router.get("/{id_pago}", response_model=PagoResponse)
def obtener_pago(
    id_pago: int,
    conn: pyodbc.Connection = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    result = get_pagos(conn, id_pago=id_pago)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pago no encontrado.")
    return result[0]


@router.post("", response_model=PagoResponse, status_code=status.HTTP_201_CREATED)
def crear_pago(
    body: PagoCreate,
    conn: pyodbc.Connection = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Registra un pago sobre un documento.
    El SP valida que el monto no exceda el saldo pendiente y actualiza
    automáticamente monto_pagado y estado_documento en la tabla Documento.
    Si no se especifica id_personal, se usa el usuario autenticado.
    """
    id_personal = body.id_personal if body.id_personal is not None else current_user["id_personal"]
    result = create_pago(
        conn, body.id_documento, body.monto_pagado, body.metodo, body.estado_pago,
        body.numero_comprobante, body.numero_operacion, body.observaciones, id_personal
    )
    if not result:
        raise HTTPException(status_code=500, detail="Error al registrar el pago.")
    return get_pagos(conn, id_pago=result["id_pago"])[0]


@router.put("/{id_pago}", response_model=MensajeResponse)
def actualizar_pago(
    id_pago: int,
    body: PagoUpdate,
    conn: pyodbc.Connection = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    """
    Actualiza solo datos administrativos del pago (estado, comprobante, operación, observaciones).
    El monto es inmutable una vez registrado.
    """
    existing = get_pagos(conn, id_pago=id_pago)
    if not existing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pago no encontrado.")
    update_pago(conn, id_pago, body.estado_pago, body.numero_comprobante,
                body.numero_operacion, body.observaciones)
    return {"mensaje": "Pago actualizado correctamente."}


@router.delete("/{id_pago}", response_model=MensajeResponse)
def eliminar_pago(
    id_pago: int,
    conn: pyodbc.Connection = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    """
    Elimina el pago y revierte el monto en el Documento (manejado en transacción por el SP).
    """
    existing = get_pagos(conn, id_pago=id_pago)
    if not existing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pago no encontrado.")
    delete_pago(conn, id_pago)
    return {"mensaje": "Pago eliminado y monto revertido en el documento correctamente."}