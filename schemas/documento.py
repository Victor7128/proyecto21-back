from pydantic import BaseModel, model_validator
from typing import Optional
from datetime import date, datetime


class DocumentoCreate(BaseModel):
    """
    Mapea a sp_InsertDocumento.
    Exactamente uno de los tres orígenes debe estar presente
    (la misma validación que hace el SP y el CHECK constraint de la BD).
    """
    numero_documento: str                       # max 50, único
    tipo_documento: int                         # FK → TipoDocumentoCobro
    id_reserva: Optional[int] = None
    id_orden_hospedaje: Optional[int] = None
    id_orden_conserjeria: Optional[int] = None
    monto_total: float                          # >= 0
    monto_pagado: float = 0.0
    fecha_vencimiento: Optional[date] = None
    descripcion: Optional[str] = None          # max 500
    estado_documento: int                       # FK → EstadoDocumento

    @model_validator(mode="after")
    def validar_un_solo_origen(self) -> "DocumentoCreate":
        origenes = sum([
            self.id_reserva is not None,
            self.id_orden_hospedaje is not None,
            self.id_orden_conserjeria is not None,
        ])
        if origenes != 1:
            raise ValueError(
                "Debe especificarse exactamente un origen: "
                "id_reserva, id_orden_hospedaje o id_orden_conserjeria."
            )
        return self


class DocumentoUpdate(BaseModel):
    """
    Mapea a sp_UpdateDocumento.
    Solo se permiten actualizar estos campos; el origen y número son inmutables.
    """
    monto_pagado: float
    fecha_vencimiento: Optional[date] = None
    descripcion: Optional[str] = None
    estado_documento: int


class DocumentoResponse(BaseModel):
    """Mapea el SELECT de sp_GetDocumento."""
    id_documento: int
    numero_documento: str
    tipo_documento: str                         # nombre del join con TipoDocumentoCobro
    monto_total: float
    monto_pagado: float
    saldo_pendiente: float                      # columna computada PERSISTED
    fecha_emision: datetime
    fecha_vencimiento: Optional[date]
    descripcion: Optional[str]
    estado: str                                 # nombre del join con EstadoDocumento
    id_reserva: Optional[int]
    id_orden_hospedaje: Optional[int]
    id_orden_conserjeria: Optional[int]


class DocumentoFilter(BaseModel):
    """Query params opcionales para sp_GetDocumento."""
    id_documento: Optional[int] = None
    numero_documento: Optional[str] = None
    estado_documento: Optional[int] = None
    tipo_documento: Optional[int] = None