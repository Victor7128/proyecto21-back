from pydantic import BaseModel
from typing import Optional


class HabitacionCreate(BaseModel):
    """Mapea a sp_InsertHabitacion."""
    numero: str                      # max 20
    piso: int
    id_tipo_habitacion: int          # FK → TipoHabitacion
    estado: int                      # FK → EstadoHabitacion


class HabitacionUpdate(BaseModel):
    """Mapea a sp_UpdateHabitacion."""
    numero: str
    piso: int
    id_tipo_habitacion: int
    estado: int


class HabitacionResponse(BaseModel):
    """
    Mapea el SELECT de sp_GetHabitacion.
    El SP devuelve los nombres de tipo y estado en lugar de sus IDs.
    """
    id_habitacion: int
    numero: str
    piso: int
    tipo_habitacion: str             # nombre del join con TipoHabitacion
    tarifa_base: float               # viene del join con TipoHabitacion
    estado: str                      # nombre del join con EstadoHabitacion


class HabitacionFilter(BaseModel):
    """Query params opcionales para sp_GetHabitacion."""
    id_habitacion: Optional[int] = None
    piso: Optional[int] = None
    estado: Optional[int] = None             # ID del estado
    id_tipo_habitacion: Optional[int] = None