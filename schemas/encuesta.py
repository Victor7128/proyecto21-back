from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class EncuestaCreate(BaseModel):
    """
    Mapea a sp_InsertEncuesta.
    El SP valida que no exista ya una encuesta para esa orden de hospedaje.
    """
    id_orden_hospedaje: int
    descripcion: Optional[str] = None              # max 500
    recomendacion: int = Field(..., ge=1, le=10)    # NPS: 1-10
    lugar_origen: Optional[str] = None             # max 100
    motivo_viaje: Optional[str] = None             # max 100
    calificacion_limpieza: Optional[int] = Field(default=None, ge=1, le=5)
    calificacion_servicio: Optional[int] = Field(default=None, ge=1, le=5)
    calificacion_ubicacion: Optional[int] = Field(default=None, ge=1, le=5)
    calificacion_precio: Optional[int] = Field(default=None, ge=1, le=5)
    comentarios: Optional[str] = None              # max 1000


class EncuestaUpdate(BaseModel):
    """
    Mapea a sp_UpdateEncuesta.
    id_orden_hospedaje no se puede cambiar.
    """
    descripcion: Optional[str] = None
    recomendacion: int = Field(..., ge=1, le=10)
    lugar_origen: Optional[str] = None
    motivo_viaje: Optional[str] = None
    calificacion_limpieza: Optional[int] = Field(default=None, ge=1, le=5)
    calificacion_servicio: Optional[int] = Field(default=None, ge=1, le=5)
    calificacion_ubicacion: Optional[int] = Field(default=None, ge=1, le=5)
    calificacion_precio: Optional[int] = Field(default=None, ge=1, le=5)
    comentarios: Optional[str] = None


class EncuestaResponse(BaseModel):
    """Mapea el SELECT de sp_GetEncuesta."""
    id_encuesta: int
    id_orden_hospedaje: int
    huesped: str                                   # nombres + apellidos del join
    recomendacion: int
    lugar_origen: Optional[str]
    motivo_viaje: Optional[str]
    calificacion_limpieza: Optional[int]
    calificacion_servicio: Optional[int]
    calificacion_ubicacion: Optional[int]
    calificacion_precio: Optional[int]
    comentarios: Optional[str]
    descripcion: Optional[str]
    fecha_encuesta: datetime


class EncuestaFilter(BaseModel):
    """Query params opcionales para sp_GetEncuesta."""
    id_encuesta: Optional[int] = None
    id_orden_hospedaje: Optional[int] = None
    motivo_viaje: Optional[str] = None