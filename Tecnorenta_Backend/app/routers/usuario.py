from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.usuario import UsuarioRepository
from app.services.usuario import UsuarioService
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate, UsuarioOut
from app.schemas.common import Page, paginate
from app.dependencies.pagination import PaginationParams

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


def get_service(db: Session = Depends(get_db)) -> UsuarioService:
    return UsuarioService(UsuarioRepository(db))


@router.get("/", response_model=Page[UsuarioOut])
def listar(pagination: PaginationParams = Depends(), db: Session = Depends(get_db)):
    items, total = get_service(db).listar(pagination.skip, pagination.limit)
    return paginate(items, total, pagination.page, pagination.page_size)


@router.get("/{usuario_id}", response_model=UsuarioOut)
def obtener(usuario_id: int, db: Session = Depends(get_db)):
    service = get_service(db)
    return service.obtener(usuario_id)


@router.post("/", response_model=UsuarioOut, status_code=201)
def crear(data: UsuarioCreate, db: Session = Depends(get_db)):
    service = get_service(db)
    return service.crear(data)


@router.patch("/{usuario_id}", response_model=UsuarioOut)
def actualizar(usuario_id: int, data: UsuarioUpdate, db: Session = Depends(get_db)):
    service = get_service(db)
    return service.actualizar(usuario_id, data)


@router.delete("/{usuario_id}", status_code=204)
def eliminar(usuario_id: int, db: Session = Depends(get_db)):
    service = get_service(db)
    return service.eliminar(usuario_id)


@router.post("/{usuario_id}/restaurar")
def restaurar(usuario_id: int, db: Session = Depends(get_db)):
    get_service(db).restaurar(usuario_id)
    return {"message": "Usuario restaurado exitosamente"}
