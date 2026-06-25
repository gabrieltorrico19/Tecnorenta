from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import require_role
from app.repositories.rol import RolRepository, PermisoRepository
from app.services.rol import RolService, PermisoService
from app.schemas.rol import RolCreate, RolOut, PermisoOut, RolAsignarPermiso

router = APIRouter(prefix="/roles", tags=["Roles y Permisos"])


@router.get("/", response_model=list[RolOut])
def listar(db: Session = Depends(get_db)):
    return RolService(RolRepository(db)).listar()


@router.get("/{rol_id}", response_model=RolOut)
def obtener(rol_id: int, db: Session = Depends(get_db)):
    return RolService(RolRepository(db)).obtener(rol_id)


@router.post("/", response_model=RolOut, status_code=201, dependencies=[Depends(require_role("Administrador"))])
def crear(data: RolCreate, db: Session = Depends(get_db)):
    return RolService(RolRepository(db)).crear(data)


@router.delete("/{rol_id}", status_code=204, dependencies=[Depends(require_role("Administrador"))])
def eliminar(rol_id: int, db: Session = Depends(get_db)):
    RolService(RolRepository(db)).eliminar(rol_id)


@router.get("/permisos/all", response_model=list[PermisoOut])
def listar_permisos(db: Session = Depends(get_db)):
    return PermisoService(PermisoRepository(db), RolRepository(db)).listar_permisos()


@router.post("/{rol_id}/permisos", response_model=RolOut, dependencies=[Depends(require_role("Administrador"))])
def asignar_permiso(rol_id: int, data: RolAsignarPermiso, db: Session = Depends(get_db)):
    return PermisoService(PermisoRepository(db), RolRepository(db)).asignar_permiso(rol_id, data.id_permiso)


@router.delete("/{rol_id}/permisos/{permiso_id}", response_model=RolOut, dependencies=[Depends(require_role("Administrador"))])
def remover_permiso(rol_id: int, permiso_id: int, db: Session = Depends(get_db)):
    return PermisoService(PermisoRepository(db), RolRepository(db)).remover_permiso(rol_id, permiso_id)
