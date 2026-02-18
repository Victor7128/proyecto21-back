from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PagoCreate(BaseModel):
    """
    Mapea a sp_InsertPago.
    El SP valida que monto_pagado no exceda el saldo_pendiente del documento.
    También actualiza monto_pagado en Documento automáticamente.
    """
    id_documento: int
    monto_pagado: float                         # > 0
    metodo: int                                 # FK → MetodoPago
    estado_pago: int                            # FK → EstadoPago
    numero_comprobante: Optional[str] = None    # max 100
    numero_operacion: Optional[str] = None      # max 100
    observaciones: Optional[str] = None        # max 500
    id_personal: Optional[int] = None          # FK → Personal (quién registró el pago)


class PagoUpdate(BaseModel):
    """
    Mapea a sp_UpdatePago.
    Solo se pueden modificar datos administrativos; el monto es inmutable.
    """
    estado_pago: int
    numero_comprobante: Optional[str] = None
    numero_operacion: Optional[str] = None
    observaciones: Optional[str] = None


class PagoResponse(BaseModel):
    """Mapea el SELECT de sp_GetPago."""
    id_pago: int
    id_documento: int
    numero_documento: str                       # del join con Documento
    fecha_pago: datetime
    monto_pagado: float
    metodo: str                                 # nombre del join con MetodoPago
    estado_pago: str                            # nombre del join con EstadoPago
    numero_comprobante: Optional[str]
    numero_operacion: Optional[str]
    observaciones: Optional[str]
    personal: Optional[str]                     # nombre del join con Personal (nullable)


class PagoFilter(BaseModel):
    """Query params opcionales para sp_GetPago."""
    id_pago: Optional[int] = None
    id_documento: Optional[int] = None
    estado_pago: Optional[int] = None
    metodo: Optional[int] = None