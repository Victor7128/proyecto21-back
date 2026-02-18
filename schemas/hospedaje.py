from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class OrdenHospedajeCreate(BaseModel):
    """Mapea a sp_InsertOrdenHospedaje."""
    id_reserva: int
    estado: int                            # FK → EstadoOrdenHospedaje
    fecha_checkin: Optional[datetime] = None
    fecha_checkout: Optional[datetime] = None  # debe ser >= fecha_checkin (validado en SP)


class OrdenHospedajeUpdate(BaseModel):
    """
    Mapea a sp_UpdateOrdenHospedaje.
    id_reserva no se puede cambiar una vez creada la orden.
    """
    estado: int
    fecha_checkin: Optional[datetime] = None
    fecha_checkout: Optional[datetime] = None


class OrdenHospedajeResponse(BaseModel):
    """Mapea el SELECT de sp_GetOrdenHospedaje."""
    id_orden_hospedaje: int
    id_reserva: int
    huesped: str                           # nombres + apellidos del join
    habitacion: str                        # numero + piso formateado
    estado: str                            # nombre del join con EstadoOrdenHospedaje
    fecha_checkin: Optional[datetime]
    fecha_checkout: Optional[datetime]


class OrdenHospedajeFilter(BaseModel):
    """Query params opcionales para sp_GetOrdenHospedaje."""
    id_orden_hospedaje: Optional[int] = None
    id_reserva: Optional[int] = None
    estado: Optional[int] = None