from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime


class ReservaCreate(BaseModel):
    """Mapea a sp_InsertReserva."""
    id_huesped: int
    id_habitacion: int
    fecha_entrada: date
    fecha_salida: date               # debe ser > fecha_entrada (validado en SP)
    num_personas: int                # > 0
    monto_total: float               # >= 0
    estado: int                      # FK → EstadoReserva


class ReservaUpdate(BaseModel):
    """Mapea a sp_UpdateReserva."""
    id_huesped: int
    id_habitacion: int
    fecha_entrada: date
    fecha_salida: date
    num_personas: int
    monto_total: float
    estado: int


class ReservaResponse(BaseModel):
    """
    Mapea el SELECT de sp_GetReserva.
    El SP devuelve huesped y habitacion como strings compuestos.
    """
    id_reserva: int
    huesped: str                     # nombres + apellidos del join
    habitacion: str                  # numero + piso formateado
    fecha_entrada: date
    fecha_salida: date
    num_personas: int
    monto_total: float
    estado: str                      # nombre del join con EstadoReserva
    fecha_creacion: datetime


class ReservaFilter(BaseModel):
    """Query params opcionales para sp_GetReserva."""
    id_reserva: Optional[int] = None
    id_huesped: Optional[int] = None
    id_habitacion: Optional[int] = None
    estado: Optional[int] = None
    fecha_entrada: Optional[date] = None   # filtra reservas desde esta fecha
    fecha_salida: Optional[date] = None    # filtra reservas hasta esta fecha