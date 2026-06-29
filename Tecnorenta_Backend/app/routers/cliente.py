from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.cliente import ClienteRepository
from app.services.cliente import ClienteService
from app.schemas.cliente import ClienteCreate, ClienteUpdate, ClienteOut

router = APIRouter(prefix="/clientes", tags=["Clientes"])


def get_service(db: Session = Depends(get_db)) -> ClienteService:
    return ClienteService(ClienteRepository(db))


@router.get("/", response_model=list[ClienteOut])
def listar(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=500), db: Session = Depends(get_db)):
    return get_service(db).listar(skip=skip, limit=limit)


@router.get("/{cliente_id}", response_model=ClienteOut)
def obtener(cliente_id: int, db: Session = Depends(get_db)):
    return get_service(db).obtener(cliente_id)


@router.post("/", response_model=ClienteOut, status_code=201)
def crear(data: ClienteCreate, db: Session = Depends(get_db)):
    return get_service(db).crear(data)


@router.put("/{cliente_id}", response_model=ClienteOut)
def actualizar(cliente_id: int, data: ClienteUpdate, db: Session = Depends(get_db)):
    return get_service(db).actualizar(cliente_id, data)


@router.delete("/{cliente_id}", status_code=204)
def eliminar(cliente_id: int, db: Session = Depends(get_db)):
    get_service(db).eliminar(cliente_id)
