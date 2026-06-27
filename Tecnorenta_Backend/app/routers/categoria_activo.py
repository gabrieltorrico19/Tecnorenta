from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.categoria_activo import CategoriaActivoRepository
from app.services.categoria_activo import CategoriaActivoService
from app.schemas.categoria_activo import CategoriaActivoCreate, CategoriaActivoUpdate, CategoriaActivoOut

router = APIRouter(prefix="/categorias-activo", tags=["Categorías de Activo"])


@router.get("/", response_model=list[CategoriaActivoOut])
def listar(db: Session = Depends(get_db)):
    return CategoriaActivoService(CategoriaActivoRepository(db)).listar()


@router.get("/{categoria_id}", response_model=CategoriaActivoOut)
def obtener(categoria_id: int, db: Session = Depends(get_db)):
    return CategoriaActivoService(CategoriaActivoRepository(db)).obtener(categoria_id)


@router.post("/", response_model=CategoriaActivoOut, status_code=201)
def crear(data: CategoriaActivoCreate, db: Session = Depends(get_db)):
    return CategoriaActivoService(CategoriaActivoRepository(db)).crear(data)


@router.patch("/{categoria_id}", response_model=CategoriaActivoOut)
def actualizar(categoria_id: int, data: CategoriaActivoUpdate, db: Session = Depends(get_db)):
    return CategoriaActivoService(CategoriaActivoRepository(db)).actualizar(categoria_id, data)


@router.delete("/{categoria_id}", status_code=204)
def eliminar(categoria_id: int, db: Session = Depends(get_db)):
    CategoriaActivoService(CategoriaActivoRepository(db), db=db).eliminar(categoria_id)
