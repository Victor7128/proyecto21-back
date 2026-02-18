from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class HuespedCreate(BaseModel):
    """Mapea a sp_InsertHuesped."""
    nombres: str                     # max 100
    apellidos: str                   # max 100
    tipo_documento: int              # FK → TipoDocumento.id_tipo_documento
    num_documento: str               # max 50
    telefono: Optional[str] = None   # max 20
    correo: Optional[EmailStr] = None


class HuespedUpdate(BaseModel):
    """Mapea a sp_UpdateHuesped."""
    nombres: str
    apellidos: str
    tipo_documento: int
    num_documento: str
    telefono: Optional[str] = None
    correo: Optional[EmailStr] = None


class HuespedResponse(BaseModel):
    """
    Mapea el SELECT de sp_GetHuesped.
    Nota: tipo_documento llega como string (descripcion del join).
    """
    id_huesped: int
    nombres: str
    apellidos: str
    tipo_documento: str              # descripcion del join con TipoDocumento
    num_documento: str
    telefono: Optional[str]
    correo: Optional[str]
    fecha_creacion: datetime


class HuespedFilter(BaseModel):
    """Query params opcionales para sp_GetHuesped."""
    id_huesped: Optional[int] = None
    num_documento: Optional[str] = None
    nombre: Optional[str] = None     # busca en nombres + apellidos