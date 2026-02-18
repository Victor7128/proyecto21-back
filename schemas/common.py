from pydantic import BaseModel


class MensajeResponse(BaseModel):
    mensaje: str