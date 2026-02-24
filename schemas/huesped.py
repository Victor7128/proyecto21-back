from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class HuespedCreate(BaseModel):
    """
    Mapea a sp_InsertHuesped.
    Usado por recepción para registrar huéspedes manualmente.
    Las credenciales (email_login / password) son opcionales:
    si no se proveen, el huésped no tendrá acceso al portal.
    Ambos deben venir juntos o ninguno (validado en el SP).
    """
    nombres: str                            # max 100
    apellidos: str                          # max 100
    tipo_documento: int                     # FK → TipoDocumento
    num_documento: str                      # max 50
    telefono: Optional[str] = None          # max 20
    correo: Optional[EmailStr] = None
    # Credenciales opcionales para dar acceso al portal
    email_login: Optional[EmailStr] = None
    password: Optional[str] = None          # texto plano → service hashea antes de llamar al SP


class HuespedRegistro(BaseModel):
    """
    Mapea a sp_RegistrarHuesped.
    Auto-registro desde el portal web/móvil.
    Las credenciales son OBLIGATORIAS (el huésped se crea con cuenta propia).
    """
    nombres: str
    apellidos: str
    tipo_documento: int
    num_documento: str
    email_login: EmailStr
    password: str                           # texto plano → service hashea antes de llamar al SP
    telefono: Optional[str] = None
    correo: Optional[EmailStr] = None


class HuespedUpdate(BaseModel):
    """
    Mapea a sp_UpdateHuesped.
    No incluye credenciales: email_login y password se gestionan
    exclusivamente con el endpoint dedicado de cambio de contraseña.
    """
    nombres: str
    apellidos: str
    tipo_documento: int
    num_documento: str
    telefono: Optional[str] = None
    correo: Optional[EmailStr] = None


class HuespedCambioPassword(BaseModel):
    """
    Mapea a sp_CambiarPasswordHuesped.
    La verificación de password_actual se hace en el service (bcrypt.checkpw)
    antes de llamar al SP.
    """
    password_actual: str
    password_nuevo: str


class HuespedResponse(BaseModel):
    """
    Mapea el SELECT de sp_GetHuesped.
    - tipo_documento llega como string (descripcion del join).
    - email_login y activo son nuevos campos del esquema actualizado.
    - password_hash nunca se expone.
    """
    id_huesped: int
    nombres: str
    apellidos: str
    tipo_documento: str                     # descripcion del join con TipoDocumento
    num_documento: str
    telefono: Optional[str]
    correo: Optional[str]
    email_login: Optional[str]              # None si fue registrado manualmente sin cuenta
    activo: bool                            # False si fue dado de baja (borrado lógico)
    fecha_creacion: datetime


class HuespedFilter(BaseModel):
    """Query params opcionales para sp_GetHuesped."""
    id_huesped: Optional[int] = None
    num_documento: Optional[str] = None
    nombre: Optional[str] = None            # busca en nombres + apellidos