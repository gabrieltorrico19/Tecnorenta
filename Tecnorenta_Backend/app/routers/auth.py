from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import hash_password, verify_password, create_access_token
from app.dependencies.auth import get_current_user
from app.models.usuario import Usuario
from app.models.rol import Rol
from app.repositories.usuario import UsuarioRepository
from app.schemas.auth import (
    LoginRequest,
    TokenResponse,
    RegisterRequest,
    ForgotPasswordRequest,
    ResetPasswordRequest,
    UserMeResponse,
)
from app.schemas.usuario import UsuarioCreate

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    repo = UsuarioRepository(db)
    user = repo.get_by_email(data.email)
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")
    if not user.activo:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Usuario inactivo")
    token = create_access_token(subject=str(user.id))
    return TokenResponse(access_token=token)


@router.post("/register", response_model=UserMeResponse, status_code=201)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    repo = UsuarioRepository(db)
    existing = repo.get_by_email(data.email)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El email ya está registrado")

    rol_cliente = db.query(Rol).filter(Rol.nombre == "Cliente").first()

    user_data = UsuarioCreate(
        nombre=data.nombre,
        email=data.email,
        password=data.password,
        telefono=data.telefono,
    )
    user = repo.create(Usuario(
        nombre=user_data.nombre,
        email=user_data.email,
        password_hash=hash_password(user_data.password),
        telefono=user_data.telefono,
        id_rol=rol_cliente.id if rol_cliente else None,
    ))

    return UserMeResponse(
        id=user.id,
        nombre=user.nombre,
        email=user.email,
        telefono=user.telefono,
        activo=user.activo,
        id_rol=user.id_rol,
        rol_nombre=user.rol.nombre if user.rol else None,
    )


@router.get("/me", response_model=UserMeResponse)
def me(current_user: Usuario = Depends(get_current_user)):
    return UserMeResponse(
        id=current_user.id,
        nombre=current_user.nombre,
        email=current_user.email,
        telefono=current_user.telefono,
        activo=current_user.activo,
        id_rol=current_user.id_rol,
        rol_nombre=current_user.rol.nombre if current_user.rol else None,
    )


@router.post("/forgot-password")
def forgot_password(data: ForgotPasswordRequest, db: Session = Depends(get_db)):
    repo = UsuarioRepository(db)
    user = repo.get_by_email(data.email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Email no registrado")
    # En producción esto enviaría un email con el token de reseteo
    reset_token = create_access_token(subject=str(user.id), expires_delta=timedelta(hours=1))
    return {"message": "Si el email existe, recibirás instrucciones para recuperar tu contraseña", "reset_token": reset_token}


@router.post("/reset-password")
def reset_password(data: ResetPasswordRequest, db: Session = Depends(get_db)):
    from jose import jwt, JWTError
    try:
        payload = jwt.decode(data.token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id = int(payload.get("sub"))
    except JWTError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token inválido o expirado")

    repo = UsuarioRepository(db)
    user = repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")

    user.password_hash = hash_password(data.new_password)
    repo.update(user)
    return {"message": "Contraseña actualizada exitosamente"}
