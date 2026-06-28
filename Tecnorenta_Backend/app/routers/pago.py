from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.pago import PagoRepository
from app.repositories.contrato import ContratoRepository
from app.services.pago import PagoService
from app.schemas.pago import PagoCreate, PagoUpdate, PagoOut

router = APIRouter(prefix="/pagos", tags=["Pagos"])


def get_service(db: Session = Depends(get_db)) -> PagoService:
    return PagoService(PagoRepository(db), ContratoRepository(db))


@router.get("/", response_model=list[PagoOut])
def listar(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=500), db: Session = Depends(get_db)):
    return get_service(db).listar(skip=skip, limit=limit)


@router.get("/{pago_id}", response_model=PagoOut)
def obtener(pago_id: int, db: Session = Depends(get_db)):
    return get_service(db).obtener(pago_id)


@router.get("/contrato/{id_contrato}", response_model=list[PagoOut])
def listar_por_contrato(id_contrato: int, db: Session = Depends(get_db)):
    return get_service(db).listar_por_contrato(id_contrato)


@router.post("/", response_model=PagoOut, status_code=201)
def crear(data: PagoCreate, db: Session = Depends(get_db)):
    return get_service(db).crear(data)


@router.put("/{pago_id}", response_model=PagoOut)
def actualizar(pago_id: int, data: PagoUpdate, db: Session = Depends(get_db)):
    return get_service(db).actualizar(pago_id, data)


@router.delete("/{pago_id}", status_code=204)
def eliminar(pago_id: int, db: Session = Depends(get_db)):
    get_service(db).eliminar(pago_id)
