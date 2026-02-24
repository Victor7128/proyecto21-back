from pydantic import BaseModel, EmailStr
from typing import Optional


class PersonalLoginRequest(BaseModel):
    email: EmailStr
    password: str                           

class HuespedLoginRequest(BaseModel):
    email_login: EmailStr
    password: str                          

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    tipo: str                               

class RegistroHuespedResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    tipo: str = "huesped"
    id_huesped: int
    nombres: str
    apellidos: str