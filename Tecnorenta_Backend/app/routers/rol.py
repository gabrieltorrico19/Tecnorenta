from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.rol import RolRepository
from app.services.rol import RolService
from app.schemas.rol import RolCreate, RolUpdate, RolOut

router = APIRouter(prefix="/roles", tags=["Roles"])


def get_service(db: Session = Depends(get_db)) -> RolService:
    return RolService(RolRepository(db))


@router.get("/", response_model=list[RolOut])
def listar(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=500), db: Session = Depends(get_db)):
    return get_service(db).listar(skip=skip, limit=limit)


@router.get("/{rol_id}", response_model=RolOut)
def obtener(rol_id: int, db: Session = Depends(get_db)):
    return get_service(db).obtener(rol_id)


@router.post("/", response_model=RolOut, status_code=201)
def crear(data: RolCreate, db: Session = Depends(get_db)):
    return get_service(db).crear(data)


@router.put("/{rol_id}", response_model=RolOut)
def actualizar(rol_id: int, data: RolUpdate, db: Session = Depends(get_db)):
    return get_service(db).actualizar(rol_id, data)


@router.delete("/{rol_id}", status_code=204)
def eliminar(rol_id: int, db: Session = Depends(get_db)):
    get_service(db).eliminar(rol_id)
