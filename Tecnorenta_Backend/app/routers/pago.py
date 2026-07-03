from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.pagination import PaginationParams
from app.models.pago import Pago, EstadoPago
from app.repositories.pago import PagoRepository
from app.services.pago import PagoService
from app.schemas.common import Page, paginate
from app.schemas.pago import PagoCreate, PagoUpdate, PagoOut

router = APIRouter(prefix="/pagos", tags=["Pagos"])


@router.get("/", response_model=Page[PagoOut])
def listar(
    pagination: PaginationParams = Depends(),
    estado: EstadoPago | None = Query(None, description="Filtrar por estado"),
    id_contrato: int | None = Query(None, description="Filtrar por contrato"),
    fecha_desde: date | None = Query(None, description="Fecha de cuota desde"),
    fecha_hasta: date | None = Query(None, description="Fecha de cuota hasta"),
    db: Session = Depends(get_db),
):
    items, total = PagoService(PagoRepository(db)).listar(
        pagination.skip, pagination.limit,
        estado=estado, id_contrato=id_contrato,
        fecha_desde=fecha_desde, fecha_hasta=fecha_hasta,
    )
    return paginate(items, total, pagination.page, pagination.page_size)


@router.get("/vencidos", response_model=list[PagoOut])
def listar_vencidos(db: Session = Depends(get_db)):
    return db.query(Pago).filter(Pago.estado == "vencido").all()


@router.get("/proximos", response_model=list[PagoOut])
def listar_proximos(db: Session = Depends(get_db)):
    return db.query(Pago).filter(Pago.estado == "pendiente").all()


@router.get("/contrato/{contrato_id}", response_model=list[PagoOut])
def listar_por_contrato(contrato_id: int, db: Session = Depends(get_db)):
    return PagoService(PagoRepository(db)).listar_por_contrato(contrato_id)


@router.get("/{pago_id}", response_model=PagoOut)
def obtener(pago_id: int, db: Session = Depends(get_db)):
    return PagoService(PagoRepository(db)).obtener(pago_id)


@router.post("/", response_model=PagoOut, status_code=201)
def crear(data: PagoCreate, db: Session = Depends(get_db)):
    return PagoService(PagoRepository(db)).crear(data)


@router.patch("/{pago_id}", response_model=PagoOut)
def actualizar(pago_id: int, data: PagoUpdate, db: Session = Depends(get_db)):
    return PagoService(PagoRepository(db)).actualizar(pago_id, data)


@router.delete("/{pago_id}", status_code=204)
def eliminar(pago_id: int, db: Session = Depends(get_db)):
    PagoService(PagoRepository(db)).eliminar(pago_id)


@router.post("/{pago_id}/restaurar")
def restaurar(pago_id: int, db: Session = Depends(get_db)):
    PagoService(PagoRepository(db)).restaurar(pago_id)
    return {"message": "Pago restaurado exitosamente"}
