from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.contrato import ContratoRepository
from app.repositories.cliente import ClienteRepository
from app.services.contrato import ContratoService
from app.schemas.contrato import ContratoCreate, ContratoUpdate, ContratoOut

router = APIRouter(prefix="/contratos", tags=["Contratos"])


def get_service(db: Session = Depends(get_db)) -> ContratoService:
    return ContratoService(ContratoRepository(db), ClienteRepository(db))


@router.get("/", response_model=list[ContratoOut])
def listar(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=500), db: Session = Depends(get_db)):
    return get_service(db).listar(skip=skip, limit=limit)


@router.get("/{contrato_id}", response_model=ContratoOut)
def obtener(contrato_id: int, db: Session = Depends(get_db)):
    return get_service(db).obtener(contrato_id)


@router.get("/cliente/{id_cliente}", response_model=list[ContratoOut])
def listar_por_cliente(id_cliente: int, db: Session = Depends(get_db)):
    return get_service(db).listar_por_cliente(id_cliente)


@router.post("/", response_model=ContratoOut, status_code=201)
def crear(data: ContratoCreate, db: Session = Depends(get_db)):
    return get_service(db).crear(data)


@router.put("/{contrato_id}", response_model=ContratoOut)
def actualizar(contrato_id: int, data: ContratoUpdate, db: Session = Depends(get_db)):
    return get_service(db).actualizar(contrato_id, data)


@router.delete("/{contrato_id}", response_model=ContratoOut)
def eliminar(contrato_id: int, db: Session = Depends(get_db)):
    return get_service(db).eliminar(contrato_id)
