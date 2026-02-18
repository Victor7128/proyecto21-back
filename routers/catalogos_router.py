"""
Router para todas las tablas catálogo (lookup tables).
Requiere autenticación en todos los endpoints de escritura.
"""
from fastapi import APIRouter, Depends, HTTPException, status
import pyodbc

from dependencies import get_db, get_current_user
from schemas.Catalogos import (
    TipoDocumentoCreate, TipoDocumentoUpdate, TipoDocumentoResponse,
    EstadoReservaCreate, EstadoReservaUpdate, EstadoReservaResponse,
    EstadoHabitacionCreate, EstadoHabitacionUpdate, EstadoHabitacionResponse,
    EstadoOrdenConserjeriaCreate, EstadoOrdenConserjeriaUpdate, EstadoOrdenConserjeriaResponse,
    EstadoOrdenHospedajeCreate, EstadoOrdenHospedajeUpdate, EstadoOrdenHospedajeResponse,
    EstadoPagoCreate, EstadoPagoUpdate, EstadoPagoResponse,
    EstadoDocumentoCreate, EstadoDocumentoUpdate, EstadoDocumentoResponse,
    MetodoPagoCreate, MetodoPagoUpdate, MetodoPagoResponse,
    RolCreate, RolUpdate, RolResponse,
    TipoDocumentoCobroCreate, TipoDocumentoCobroUpdate, TipoDocumentoCobroResponse,
    TipoHabitacionCreate, TipoHabitacionUpdate, TipoHabitacionResponse,
)
from schemas.common import MensajeResponse
from services import catalogo_service

router = APIRouter(prefix="/catalogos", tags=["Catálogos"])


# ── TipoDocumento ──────────────────────────────────────────────────────────────

@router.get("/tipo-documento", response_model=list[TipoDocumentoResponse])
def listar_tipo_documento(
    id_tipo_documento: int | None = None,
    conn: pyodbc.Connection = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    return catalogo_service.get_tipo_documento(conn, id_tipo_documento)


@router.post("/tipo-documento", response_model=TipoDocumentoResponse, status_code=status.HTTP_201_CREATED)
def crear_tipo_documento(
    body: TipoDocumentoCreate,
    conn: pyodbc.Connection = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    result = catalogo_service.create_tipo_documento(conn, body.codigo, body.descripcion)
    if not result:
        raise HTTPException(status_code=500, detail="Error al crear el tipo de documento.")
    return catalogo_service.get_tipo_documento(conn, result["id_tipo_documento"])[0]


@router.put("/tipo-documento/{id_tipo_documento}", response_model=MensajeResponse)
def actualizar_tipo_documento(
    id_tipo_documento: int,
    body: TipoDocumentoUpdate,
    conn: pyodbc.Connection = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    catalogo_service.update_tipo_documento(conn, id_tipo_documento, body.codigo, body.descripcion)
    return {"mensaje": "Tipo de documento actualizado correctamente."}


@router.delete("/tipo-documento/{id_tipo_documento}", response_model=MensajeResponse)
def eliminar_tipo_documento(
    id_tipo_documento: int,
    conn: pyodbc.Connection = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    catalogo_service.delete_tipo_documento(conn, id_tipo_documento)
    return {"mensaje": "Tipo de documento eliminado correctamente."}


# ── EstadoReserva ──────────────────────────────────────────────────────────────

@router.get("/estado-reserva", response_model=list[EstadoReservaResponse])
def listar_estado_reserva(
    id_estado_reserva: int | None = None,
    conn: pyodbc.Connection = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    return catalogo_service.get_estado_reserva(conn, id_estado_reserva)


@router.post("/estado-reserva", response_model=EstadoReservaResponse, status_code=status.HTTP_201_CREATED)
def crear_estado_reserva(
    body: EstadoReservaCreate,
    conn: pyodbc.Connection = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    result = catalogo_service.create_estado_reserva(conn, body.nombre)
    if not result:
        raise HTTPException(status_code=500, detail="Error al crear el estado de reserva.")
    return catalogo_service.get_estado_reserva(conn, result["id_estado_reserva"])[0]


@router.put("/estado-reserva/{id_estado_reserva}", response_model=MensajeResponse)
def actualizar_estado_reserva(
    id_estado_reserva: int,
    body: EstadoReservaUpdate,
    conn: pyodbc.Connection = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    catalogo_service.update_estado_reserva(conn, id_estado_reserva, body.nombre)
    return {"mensaje": "Estado de reserva actualizado correctamente."}


@router.delete("/estado-reserva/{id_estado_reserva}", response_model=MensajeResponse)
def eliminar_estado_reserva(
    id_estado_reserva: int,
    conn: pyodbc.Connection = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    catalogo_service.delete_estado_reserva(conn, id_estado_reserva)
    return {"mensaje": "Estado de reserva eliminado correctamente."}


# ── EstadoHabitacion ───────────────────────────────────────────────────────────

@router.get("/estado-habitacion", response_model=list[EstadoHabitacionResponse])
def listar_estado_habitacion(
    id_estado_habitacion: int | None = None,
    conn: pyodbc.Connection = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    return catalogo_service.get_estado_habitacion(conn, id_estado_habitacion)


@router.post("/estado-habitacion", response_model=EstadoHabitacionResponse, status_code=status.HTTP_201_CREATED)
def crear_estado_habitacion(
    body: EstadoHabitacionCreate,
    conn: pyodbc.Connection = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    result = catalogo_service.create_estado_habitacion(conn, body.nombre)
    if not result:
        raise HTTPException(status_code=500, detail="Error al crear el estado de habitación.")
    return catalogo_service.get_estado_habitacion(conn, result["id_estado_habitacion"])[0]


@router.put("/estado-habitacion/{id_estado_habitacion}", response_model=MensajeResponse)
def actualizar_estado_habitacion(
    id_estado_habitacion: int,
    body: EstadoHabitacionUpdate,
    conn: pyodbc.Connection = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    catalogo_service.update_estado_habitacion(conn, id_estado_habitacion, body.nombre)
    return {"mensaje": "Estado de habitación actualizado correctamente."}


@router.delete("/estado-habitacion/{id_estado_habitacion}", response_model=MensajeResponse)
def eliminar_estado_habitacion(
    id_estado_habitacion: int,
    conn: pyodbc.Connection = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    catalogo_service.delete_estado_habitacion(conn, id_estado_habitacion)
    return {"mensaje": "Estado de habitación eliminado correctamente."}


# ── EstadoOrdenConserjeria ─────────────────────────────────────────────────────

@router.get("/estado-orden-conserjeria", response_model=list[EstadoOrdenConserjeriaResponse])
def listar_estado_orden_conserjeria(
    id_estado_orden_conserj: int | None = None,
    conn: pyodbc.Connection = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    return catalogo_service.get_estado_orden_conserjeria(conn, id_estado_orden_conserj)


@router.post("/estado-orden-conserjeria", response_model=EstadoOrdenConserjeriaResponse, status_code=status.HTTP_201_CREATED)
def crear_estado_orden_conserjeria(
    body: EstadoOrdenConserjeriaCreate,
    conn: pyodbc.Connection = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    result = catalogo_service.create_estado_orden_conserjeria(conn, body.nombre)
    if not result:
        raise HTTPException(status_code=500, detail="Error al crear el estado.")
    return catalogo_service.get_estado_orden_conserjeria(conn, result["id_estado_orden_conserj"])[0]


@router.put("/estado-orden-conserjeria/{id_estado_orden_conserj}", response_model=MensajeResponse)
def actualizar_estado_orden_conserjeria(
    id_estado_orden_conserj: int,
    body: EstadoOrdenConserjeriaUpdate,
    conn: pyodbc.Connection = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    catalogo_service.update_estado_orden_conserjeria(conn, id_estado_orden_conserj, body.nombre)
    return {"mensaje": "Estado actualizado correctamente."}


@router.delete("/estado-orden-conserjeria/{id_estado_orden_conserj}", response_model=MensajeResponse)
def eliminar_estado_orden_conserjeria(
    id_estado_orden_conserj: int,
    conn: pyodbc.Connection = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    catalogo_service.delete_estado_orden_conserjeria(conn, id_estado_orden_conserj)
    return {"mensaje": "Estado eliminado correctamente."}


# ── EstadoOrdenHospedaje ───────────────────────────────────────────────────────

@router.get("/estado-orden-hospedaje", response_model=list[EstadoOrdenHospedajeResponse])
def listar_estado_orden_hospedaje(
    id_estado_orden_hosp: int | None = None,
    conn: pyodbc.Connection = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    return catalogo_service.get_estado_orden_hospedaje(conn, id_estado_orden_hosp)


@router.post("/estado-orden-hospedaje", response_model=EstadoOrdenHospedajeResponse, status_code=status.HTTP_201_CREATED)
def crear_estado_orden_hospedaje(
    body: EstadoOrdenHospedajeCreate,
    conn: pyodbc.Connection = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    result = catalogo_service.create_estado_orden_hospedaje(conn, body.nombre)
    if not result:
        raise HTTPException(status_code=500, detail="Error al crear el estado.")
    return catalogo_service.get_estado_orden_hospedaje(conn, result["id_estado_orden_hosp"])[0]


@router.put("/estado-orden-hospedaje/{id_estado_orden_hosp}", response_model=MensajeResponse)
def actualizar_estado_orden_hospedaje(
    id_estado_orden_hosp: int,
    body: EstadoOrdenHospedajeUpdate,
    conn: pyodbc.Connection = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    catalogo_service.update_estado_orden_hospedaje(conn, id_estado_orden_hosp, body.nombre)
    return {"mensaje": "Estado actualizado correctamente."}


@router.delete("/estado-orden-hospedaje/{id_estado_orden_hosp}", response_model=MensajeResponse)
def eliminar_estado_orden_hospedaje(
    id_estado_orden_hosp: int,
    conn: pyodbc.Connection = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    catalogo_service.delete_estado_orden_hospedaje(conn, id_estado_orden_hosp)
    return {"mensaje": "Estado eliminado correctamente."}


# ── EstadoPago ─────────────────────────────────────────────────────────────────

@router.get("/estado-pago", response_model=list[EstadoPagoResponse])
def listar_estado_pago(
    id_estado_pago: int | None = None,
    conn: pyodbc.Connection = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    return catalogo_service.get_estado_pago(conn, id_estado_pago)


@router.post("/estado-pago", response_model=EstadoPagoResponse, status_code=status.HTTP_201_CREATED)
def crear_estado_pago(
    body: EstadoPagoCreate,
    conn: pyodbc.Connection = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    result = catalogo_service.create_estado_pago(conn, body.nombre)
    if not result:
        raise HTTPException(status_code=500, detail="Error al crear el estado de pago.")
    return catalogo_service.get_estado_pago(conn, result["id_estado_pago"])[0]


@router.put("/estado-pago/{id_estado_pago}", response_model=MensajeResponse)
def actualizar_estado_pago(
    id_estado_pago: int,
    body: EstadoPagoUpdate,
    conn: pyodbc.Connection = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    catalogo_service.update_estado_pago(conn, id_estado_pago, body.nombre)
    return {"mensaje": "Estado de pago actualizado correctamente."}


@router.delete("/estado-pago/{id_estado_pago}", response_model=MensajeResponse)
def eliminar_estado_pago(
    id_estado_pago: int,
    conn: pyodbc.Connection = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    catalogo_service.delete_estado_pago(conn, id_estado_pago)
    return {"mensaje": "Estado de pago eliminado correctamente."}


# ── EstadoDocumento ────────────────────────────────────────────────────────────

@router.get("/estado-documento", response_model=list[EstadoDocumentoResponse])
def listar_estado_documento(
    id_estado_documento: int | None = None,
    conn: pyodbc.Connection = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    return catalogo_service.get_estado_documento(conn, id_estado_documento)


@router.post("/estado-documento", response_model=EstadoDocumentoResponse, status_code=status.HTTP_201_CREATED)
def crear_estado_documento(
    body: EstadoDocumentoCreate,
    conn: pyodbc.Connection = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    result = catalogo_service.create_estado_documento(conn, body.nombre)
    if not result:
        raise HTTPException(status_code=500, detail="Error al crear el estado de documento.")
    return catalogo_service.get_estado_documento(conn, result["id_estado_documento"])[0]


@router.put("/estado-documento/{id_estado_documento}", response_model=MensajeResponse)
def actualizar_estado_documento(
    id_estado_documento: int,
    body: EstadoDocumentoUpdate,
    conn: pyodbc.Connection = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    catalogo_service.update_estado_documento(conn, id_estado_documento, body.nombre)
    return {"mensaje": "Estado de documento actualizado correctamente."}


@router.delete("/estado-documento/{id_estado_documento}", response_model=MensajeResponse)
def eliminar_estado_documento(
    id_estado_documento: int,
    conn: pyodbc.Connection = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    catalogo_service.delete_estado_documento(conn, id_estado_documento)
    return {"mensaje": "Estado de documento eliminado correctamente."}


# ── MetodoPago ─────────────────────────────────────────────────────────────────

@router.get("/metodo-pago", response_model=list[MetodoPagoResponse])
def listar_metodo_pago(
    id_metodo_pago: int | None = None,
    conn: pyodbc.Connection = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    return catalogo_service.get_metodo_pago(conn, id_metodo_pago)


@router.post("/metodo-pago", response_model=MetodoPagoResponse, status_code=status.HTTP_201_CREATED)
def crear_metodo_pago(
    body: MetodoPagoCreate,
    conn: pyodbc.Connection = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    result = catalogo_service.create_metodo_pago(conn, body.nombre)
    if not result:
        raise HTTPException(status_code=500, detail="Error al crear el método de pago.")
    return catalogo_service.get_metodo_pago(conn, result["id_metodo_pago"])[0]


@router.put("/metodo-pago/{id_metodo_pago}", response_model=MensajeResponse)
def actualizar_metodo_pago(
    id_metodo_pago: int,
    body: MetodoPagoUpdate,
    conn: pyodbc.Connection = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    catalogo_service.update_metodo_pago(conn, id_metodo_pago, body.nombre)
    return {"mensaje": "Método de pago actualizado correctamente."}


@router.delete("/metodo-pago/{id_metodo_pago}", response_model=MensajeResponse)
def eliminar_metodo_pago(
    id_metodo_pago: int,
    conn: pyodbc.Connection = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    catalogo_service.delete_metodo_pago(conn, id_metodo_pago)
    return {"mensaje": "Método de pago eliminado correctamente."}


# ── Rol ────────────────────────────────────────────────────────────────────────

@router.get("/rol", response_model=list[RolResponse])
def listar_roles(
    id_rol: int | None = None,
    conn: pyodbc.Connection = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    return catalogo_service.get_rol(conn, id_rol)


@router.post("/rol", response_model=RolResponse, status_code=status.HTTP_201_CREATED)
def crear_rol(
    body: RolCreate,
    conn: pyodbc.Connection = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    result = catalogo_service.create_rol(conn, body.nombre, body.descripcion)
    if not result:
        raise HTTPException(status_code=500, detail="Error al crear el rol.")
    return catalogo_service.get_rol(conn, result["id_rol"])[0]


@router.put("/rol/{id_rol}", response_model=MensajeResponse)
def actualizar_rol(
    id_rol: int,
    body: RolUpdate,
    conn: pyodbc.Connection = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    catalogo_service.update_rol(conn, id_rol, body.nombre, body.descripcion)
    return {"mensaje": "Rol actualizado correctamente."}


@router.delete("/rol/{id_rol}", response_model=MensajeResponse)
def eliminar_rol(
    id_rol: int,
    conn: pyodbc.Connection = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    catalogo_service.delete_rol(conn, id_rol)
    return {"mensaje": "Rol eliminado correctamente."}


# ── TipoDocumentoCobro ─────────────────────────────────────────────────────────

@router.get("/tipo-documento-cobro", response_model=list[TipoDocumentoCobroResponse])
def listar_tipo_documento_cobro(
    id_tipo_doc_cobro: int | None = None,
    conn: pyodbc.Connection = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    return catalogo_service.get_tipo_documento_cobro(conn, id_tipo_doc_cobro)


@router.post("/tipo-documento-cobro", response_model=TipoDocumentoCobroResponse, status_code=status.HTTP_201_CREATED)
def crear_tipo_documento_cobro(
    body: TipoDocumentoCobroCreate,
    conn: pyodbc.Connection = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    result = catalogo_service.create_tipo_documento_cobro(conn, body.nombre, body.descripcion)
    if not result:
        raise HTTPException(status_code=500, detail="Error al crear el tipo de documento de cobro.")
    return catalogo_service.get_tipo_documento_cobro(conn, result["id_tipo_doc_cobro"])[0]


@router.put("/tipo-documento-cobro/{id_tipo_doc_cobro}", response_model=MensajeResponse)
def actualizar_tipo_documento_cobro(
    id_tipo_doc_cobro: int,
    body: TipoDocumentoCobroUpdate,
    conn: pyodbc.Connection = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    catalogo_service.update_tipo_documento_cobro(conn, id_tipo_doc_cobro, body.nombre, body.descripcion)
    return {"mensaje": "Tipo de documento de cobro actualizado correctamente."}


@router.delete("/tipo-documento-cobro/{id_tipo_doc_cobro}", response_model=MensajeResponse)
def eliminar_tipo_documento_cobro(
    id_tipo_doc_cobro: int,
    conn: pyodbc.Connection = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    catalogo_service.delete_tipo_documento_cobro(conn, id_tipo_doc_cobro)
    return {"mensaje": "Tipo de documento de cobro eliminado correctamente."}


# ── TipoHabitacion ─────────────────────────────────────────────────────────────

@router.get("/tipo-habitacion", response_model=list[TipoHabitacionResponse])
def listar_tipo_habitacion(
    id_tipo_habitacion: int | None = None,
    nombre: str | None = None,
    conn: pyodbc.Connection = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    return catalogo_service.get_tipo_habitacion(conn, id_tipo_habitacion, nombre)


@router.post("/tipo-habitacion", response_model=TipoHabitacionResponse, status_code=status.HTTP_201_CREATED)
def crear_tipo_habitacion(
    body: TipoHabitacionCreate,
    conn: pyodbc.Connection = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    result = catalogo_service.create_tipo_habitacion(
        conn, body.nombre, body.descripcion, body.capacidad_personas, body.tarifa_base
    )
    if not result:
        raise HTTPException(status_code=500, detail="Error al crear el tipo de habitación.")
    return catalogo_service.get_tipo_habitacion(conn, result["id_tipo_habitacion"])[0]


@router.put("/tipo-habitacion/{id_tipo_habitacion}", response_model=MensajeResponse)
def actualizar_tipo_habitacion(
    id_tipo_habitacion: int,
    body: TipoHabitacionUpdate,
    conn: pyodbc.Connection = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    catalogo_service.update_tipo_habitacion(
        conn, id_tipo_habitacion, body.nombre, body.descripcion,
        body.capacidad_personas, body.tarifa_base
    )
    return {"mensaje": "Tipo de habitación actualizado correctamente."}


@router.delete("/tipo-habitacion/{id_tipo_habitacion}", response_model=MensajeResponse)
def eliminar_tipo_habitacion(
    id_tipo_habitacion: int,
    conn: pyodbc.Connection = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    catalogo_service.delete_tipo_habitacion(conn, id_tipo_habitacion)
    return {"mensaje": "Tipo de habitación eliminado correctamente."}