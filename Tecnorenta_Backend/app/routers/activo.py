from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_current_user, require_role
from app.models.usuario import Usuario
from app.repositories.activo import ActivoRepository
from app.services.activo import ActivoService
from app.schemas.activo import ActivoCreate, ActivoUpdate, ActivoOut

router = APIRouter(prefix="/activos", tags=["Activos"])


@router.get("/", response_model=list[ActivoOut])
def listar(db: Session = Depends(get_db)):
    return ActivoService(ActivoRepository(db)).listar()


@router.get("/{activo_id}", response_model=ActivoOut)
def obtener(activo_id: int, db: Session = Depends(get_db)):
    return ActivoService(ActivoRepository(db)).obtener(activo_id)


@router.post("/", response_model=ActivoOut, status_code=201)
def crear(data: ActivoCreate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    return ActivoService(ActivoRepository(db)).crear(data)


@router.patch("/{activo_id}", response_model=ActivoOut)
def actualizar(activo_id: int, data: ActivoUpdate, db: Session = Depends(get_db)):
    return ActivoService(ActivoRepository(db)).actualizar(activo_id, data)


@router.delete("/{activo_id}", status_code=204, dependencies=[Depends(require_role("Administrador"))])
def eliminar(activo_id: int, db: Session = Depends(get_db)):
    ActivoService(ActivoRepository(db)).eliminar(activo_id)
