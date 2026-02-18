from pydantic import BaseModel


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Datos decodificados del JWT. Uso interno en dependencies.py."""
    id_personal: int
    rol: str