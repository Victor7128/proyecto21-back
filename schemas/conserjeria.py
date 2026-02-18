from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class OrdenConserjeriaCreate(BaseModel):
    """Mapea a sp_InsertOrdenConserjeria."""
    id_personal: int
    id_habitacion: int
    id_reserva: Optional[int] = None       # puede ser sin reserva asociada
    fecha_inicio: datetime
    fecha_fin: Optional[datetime] = None   # debe ser >= fecha_inicio si se provee
    precio: float                          # >= 0
    estado: int                            # FK → EstadoOrdenConserjeria
    descripcion: Optional[str] = None      # max 500


class OrdenConserjeriaUpdate(BaseModel):
    """Mapea a sp_UpdateOrdenConserjeria."""
    id_personal: int
    id_habitacion: int
    id_reserva: Optional[int] = None
    fecha_inicio: datetime
    fecha_fin: Optional[datetime] = None
    precio: float
    estado: int
    descripcion: Optional[str] = None


class OrdenConserjeriaResponse(BaseModel):
    """Mapea el SELECT de sp_GetOrdenConserjeria."""
    id_orden_conserj: int
    personal: str                          # nombre del join con Personal
    habitacion: str                        # numero + piso formateado
    id_reserva: Optional[int]
    fecha_inicio: datetime
    fecha_fin: Optional[datetime]
    precio: float
    estado: str                            # nombre del join con EstadoOrdenConserjeria
    descripcion: Optional[str]


class OrdenConserjeriaFilter(BaseModel):
    """Query params opcionales para sp_GetOrdenConserjeria."""
    id_orden_conserj: Optional[int] = None
    id_habitacion: Optional[int] = None
    id_personal: Optional[int] = None
    estado: Optional[int] = None