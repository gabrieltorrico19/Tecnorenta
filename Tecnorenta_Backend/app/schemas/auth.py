from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class RegisterRequest(BaseModel):
    nombre: str
    email: EmailStr
    password: str
    telefono: str | None = None


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str


class UserMeResponse(BaseModel):
    id: int
    nombre: str
    email: str
    telefono: str | None
    activo: bool
    id_rol: int | None
    rol_nombre: str | None = None

    model_config = {"from_attributes": True}
