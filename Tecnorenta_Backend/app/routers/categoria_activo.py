from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.categoria_activo import CategoriaActivoRepository
from app.services.categoria_activo import CategoriaActivoService
from app.schemas.categoria_activo import CategoriaActivoCreate, CategoriaActivoUpdate, CategoriaActivoOut

router = APIRouter(prefix="/categorias-activo", tags=["Categorías de Activo"])


def get_service(db: Session = Depends(get_db)) -> CategoriaActivoService:
    return CategoriaActivoService(CategoriaActivoRepository(db))


@router.get("/", response_model=list[CategoriaActivoOut])
def listar(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=500), db: Session = Depends(get_db)):
    return get_service(db).listar(skip=skip, limit=limit)


@router.get("/{categoria_id}", response_model=CategoriaActivoOut)
def obtener(categoria_id: int, db: Session = Depends(get_db)):
    return get_service(db).obtener(categoria_id)


@router.post("/", response_model=CategoriaActivoOut, status_code=201)
def crear(data: CategoriaActivoCreate, db: Session = Depends(get_db)):
    return get_service(db).crear(data)


@router.put("/{categoria_id}", response_model=CategoriaActivoOut)
def actualizar(categoria_id: int, data: CategoriaActivoUpdate, db: Session = Depends(get_db)):
    return get_service(db).actualizar(categoria_id, data)


@router.delete("/{categoria_id}", status_code=204)
def eliminar(categoria_id: int, db: Session = Depends(get_db)):
    get_service(db).eliminar(categoria_id)
