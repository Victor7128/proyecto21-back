from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class PersonalCreate(BaseModel):
    """
    Mapea a sp_InsertPersonal.
    El password llega como texto plano; el service lo hashea antes de llamar al SP.
    """
    nombre: str                      # max 100
    tipo_documento: int              # FK → TipoDocumento.id_tipo_documento
    num_documento: str               # max 50
    email: Optional[EmailStr] = None
    password: str                    # texto plano — service convierte a password_hash
    id_rol: int                      # FK → Rol.id_rol
    activo: bool = True


class PersonalUpdate(BaseModel):
    """
    Mapea a sp_UpdatePersonal.
    No incluye password (usa un endpoint separado para cambio de contraseña).
    """
    nombre: str
    tipo_documento: int
    num_documento: str
    email: Optional[EmailStr] = None
    id_rol: int
    activo: bool


class PersonalCambioPassword(BaseModel):
    """Endpoint dedicado para cambiar contraseña."""
    password_actual: str
    password_nuevo: str


class PersonalResponse(BaseModel):
    """
    Mapea el SELECT de sp_GetPersonal.
    No expone password_hash nunca.
    """
    id_personal: int
    nombre: str
    tipo_documento: str              # descripcion del join con TipoDocumento
    num_documento: str
    email: Optional[str]
    rol: str 
    activo: bool
    fecha_creacion: datetime


class PersonalFilter(BaseModel):
    """Query params opcionales para sp_GetPersonal."""
    id_personal: Optional[int] = None
    nombre: Optional[str] = None
    id_rol: Optional[int] = None
    activo: Optional[bool] = None