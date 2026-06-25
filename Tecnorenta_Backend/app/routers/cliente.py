from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.cliente import ClienteRepository
from app.services.cliente import ClienteService
from app.schemas.cliente import ClienteCreate, ClienteUpdate, ClienteOut

router = APIRouter(prefix="/clientes", tags=["Clientes"])


@router.get("/", response_model=list[ClienteOut])
def listar(db: Session = Depends(get_db)):
    return ClienteService(ClienteRepository(db)).listar()


@router.get("/{cliente_id}", response_model=ClienteOut)
def obtener(cliente_id: int, db: Session = Depends(get_db)):
    return ClienteService(ClienteRepository(db)).obtener(cliente_id)


@router.post("/", response_model=ClienteOut, status_code=201)
def crear(data: ClienteCreate, db: Session = Depends(get_db)):
    return ClienteService(ClienteRepository(db)).crear(data)


@router.patch("/{cliente_id}", response_model=ClienteOut)
def actualizar(cliente_id: int, data: ClienteUpdate, db: Session = Depends(get_db)):
    return ClienteService(ClienteRepository(db)).actualizar(cliente_id, data)


@router.delete("/{cliente_id}", status_code=204)
def eliminar(cliente_id: int, db: Session = Depends(get_db)):
    ClienteService(ClienteRepository(db)).eliminar(cliente_id)
