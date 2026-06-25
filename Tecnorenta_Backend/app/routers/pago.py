from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.pago import PagoRepository
from app.services.pago import PagoService
from app.schemas.pago import PagoCreate, PagoOut

router = APIRouter(prefix="/pagos", tags=["Pagos"])


@router.get("/", response_model=list[PagoOut])
def listar(db: Session = Depends(get_db)):
    return PagoService(PagoRepository(db)).listar()


@router.get("/contrato/{contrato_id}", response_model=list[PagoOut])
def listar_por_contrato(contrato_id: int, db: Session = Depends(get_db)):
    return PagoService(PagoRepository(db)).listar_por_contrato(contrato_id)


@router.get("/{pago_id}", response_model=PagoOut)
def obtener(pago_id: int, db: Session = Depends(get_db)):
    return PagoService(PagoRepository(db)).obtener(pago_id)


@router.post("/", response_model=PagoOut, status_code=201)
def crear(data: PagoCreate, db: Session = Depends(get_db)):
    return PagoService(PagoRepository(db)).crear(data)


@router.delete("/{pago_id}", status_code=204)
def eliminar(pago_id: int, db: Session = Depends(get_db)):
    PagoService(PagoRepository(db)).eliminar(pago_id)
