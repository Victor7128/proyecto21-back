"""
Schemas para las tablas catálogo (lookup tables).
Todas comparten el mismo patrón: Create, Update y Response.
"""
from pydantic import BaseModel
from typing import Optional


# ── TipoDocumento ──────────────────────────────────────────────────────────────

class TipoDocumentoCreate(BaseModel):
    codigo: str          # max 20 chars
    descripcion: str     # max 100 chars


class TipoDocumentoUpdate(BaseModel):
    codigo: str
    descripcion: str


class TipoDocumentoResponse(BaseModel):
    id_tipo_documento: int
    codigo: str
    descripcion: str


# ── EstadoReserva ──────────────────────────────────────────────────────────────

class EstadoReservaCreate(BaseModel):
    nombre: str          # max 50 chars


class EstadoReservaUpdate(BaseModel):
    nombre: str


class EstadoReservaResponse(BaseModel):
    id_estado_reserva: int
    nombre: str


# ── EstadoHabitacion ───────────────────────────────────────────────────────────

class EstadoHabitacionCreate(BaseModel):
    nombre: str


class EstadoHabitacionUpdate(BaseModel):
    nombre: str


class EstadoHabitacionResponse(BaseModel):
    id_estado_habitacion: int
    nombre: str


# ── EstadoOrdenConserjeria ─────────────────────────────────────────────────────

class EstadoOrdenConserjeriaCreate(BaseModel):
    nombre: str


class EstadoOrdenConserjeriaUpdate(BaseModel):
    nombre: str


class EstadoOrdenConserjeriaResponse(BaseModel):
    id_estado_orden_conserj: int
    nombre: str


# ── EstadoOrdenHospedaje ───────────────────────────────────────────────────────

class EstadoOrdenHospedajeCreate(BaseModel):
    nombre: str


class EstadoOrdenHospedajeUpdate(BaseModel):
    nombre: str


class EstadoOrdenHospedajeResponse(BaseModel):
    id_estado_orden_hosp: int
    nombre: str


# ── EstadoPago ─────────────────────────────────────────────────────────────────

class EstadoPagoCreate(BaseModel):
    nombre: str


class EstadoPagoUpdate(BaseModel):
    nombre: str


class EstadoPagoResponse(BaseModel):
    id_estado_pago: int
    nombre: str


# ── EstadoDocumento ────────────────────────────────────────────────────────────

class EstadoDocumentoCreate(BaseModel):
    nombre: str


class EstadoDocumentoUpdate(BaseModel):
    nombre: str


class EstadoDocumentoResponse(BaseModel):
    id_estado_documento: int
    nombre: str


# ── MetodoPago ─────────────────────────────────────────────────────────────────

class MetodoPagoCreate(BaseModel):
    nombre: str


class MetodoPagoUpdate(BaseModel):
    nombre: str


class MetodoPagoResponse(BaseModel):
    id_metodo_pago: int
    nombre: str


# ── Rol ────────────────────────────────────────────────────────────────────────

class RolCreate(BaseModel):
    nombre: str
    descripcion: Optional[str] = None


class RolUpdate(BaseModel):
    nombre: str
    descripcion: Optional[str] = None


class RolResponse(BaseModel):
    id_rol: int
    nombre: str
    descripcion: Optional[str]


# ── TipoDocumentoCobro ─────────────────────────────────────────────────────────

class TipoDocumentoCobroCreate(BaseModel):
    nombre: str
    descripcion: Optional[str] = None


class TipoDocumentoCobroUpdate(BaseModel):
    nombre: str
    descripcion: Optional[str] = None


class TipoDocumentoCobroResponse(BaseModel):
    id_tipo_doc_cobro: int
    nombre: str
    descripcion: Optional[str]


# ── TipoHabitacion ─────────────────────────────────────────────────────────────
# Se incluye aquí por ser un catálogo maestro de habitaciones.

class TipoHabitacionCreate(BaseModel):
    nombre: str                      # max 100 chars
    descripcion: Optional[str] = None
    capacidad_personas: int          # > 0
    tarifa_base: float               # >= 0


class TipoHabitacionUpdate(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    capacidad_personas: int
    tarifa_base: float


class TipoHabitacionResponse(BaseModel):
    id_tipo_habitacion: int
    nombre: str
    descripcion: Optional[str]
    capacidad_personas: int
    tarifa_base: float