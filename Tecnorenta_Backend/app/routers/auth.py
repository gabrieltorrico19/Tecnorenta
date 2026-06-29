import secrets
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.usuario import Usuario

router = APIRouter(prefix="/auth", tags=["Autenticación"])

# Almacenamiento temporal de tokens de reset (en producción usar Redis o tabla BD)
_reset_tokens: dict[str, dict] = {}


class SolicitudReset(BaseModel):
    email: EmailStr


class ResetPassword(BaseModel):
    token: str
    nueva_password: str


# US-19: Recuperar contraseña por correo
@router.post("/forgot-password")
def solicitar_reset_password(data: SolicitudReset, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == data.email).first()

    # Siempre responder igual para no revelar si el email existe (seguridad)
    if not usuario:
        return {
            "success": True,
            "errors": [],
            "mensaje": "Si el correo existe en el sistema, recibirás un enlace de recuperación.",
        }

    token = secrets.token_urlsafe(32)
    expira = datetime.utcnow() + timedelta(hours=1)
    _reset_tokens[token] = {"id_usuario": usuario.id, "expira": expira}

    # TODO: cuando tengas BD + SMTP configurado, enviar el email aquí:
    # send_email(
    #     to=usuario.email,
    #     subject="Recuperación de contraseña - SIGTAR",
    #     body=f"Tu enlace de recuperación: http://localhost:5173/reset-password?token={token}"
    # )

    # Por ahora retornamos el token en la respuesta (solo para desarrollo)
    return {
        "success": True,
        "errors": [],
        "mensaje": "Si el correo existe en el sistema, recibirás un enlace de recuperación.",
        "dev_token": token,  # ELIMINAR en producción
    }


@router.post("/reset-password")
def reset_password(data: ResetPassword, db: Session = Depends(get_db)):
    from app.core.security import hash_password

    registro = _reset_tokens.get(data.token)
    if not registro:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token inválido o inexistente",
        )

    if datetime.utcnow() > registro["expira"]:
        _reset_tokens.pop(data.token, None)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El token ha expirado. Solicita uno nuevo.",
        )

    if len(data.nueva_password) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La contraseña debe tener al menos 6 caracteres",
        )

    usuario = db.query(Usuario).filter(Usuario.id == registro["id_usuario"]).first()
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")

    usuario.password_hash = hash_password(data.nueva_password)
    db.commit()
    _reset_tokens.pop(data.token, None)

    return {"success": True, "errors": [], "mensaje": "Contraseña actualizada correctamente"}
