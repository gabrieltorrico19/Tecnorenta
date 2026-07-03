import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, UploadFile, File, Query
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.models.contrato import EstadoContrato
from app.repositories.contrato import ContratoRepository
from app.services.contrato import ContratoService
from app.schemas.contrato import ContratoCreate, ContratoUpdate, ContratoOut
from app.schemas.common import Page, paginate
from app.dependencies.pagination import PaginationParams

router = APIRouter(prefix="/contratos", tags=["Contratos"])


@router.get("/", response_model=Page[ContratoOut])
def listar(
    pagination: PaginationParams = Depends(),
    estado: EstadoContrato | None = Query(None, description="Filtrar por estado"),
    id_cliente: int | None = Query(None, description="Filtrar por cliente"),
    db: Session = Depends(get_db),
):
    items, total = ContratoService(ContratoRepository(db)).listar(
        pagination.skip, pagination.limit, estado=estado, id_cliente=id_cliente
    )
    return paginate(items, total, pagination.page, pagination.page_size)


@router.get("/{contrato_id}", response_model=ContratoOut)
def obtener(contrato_id: int, db: Session = Depends(get_db)):
    return ContratoService(ContratoRepository(db)).obtener(contrato_id)


@router.post("/", response_model=ContratoOut, status_code=201)
def crear(data: ContratoCreate, db: Session = Depends(get_db)):
    return ContratoService(ContratoRepository(db)).crear(data)


@router.patch("/{contrato_id}", response_model=ContratoOut)
def actualizar(contrato_id: int, data: ContratoUpdate, db: Session = Depends(get_db)):
    return ContratoService(ContratoRepository(db)).actualizar(contrato_id, data)


@router.post("/{contrato_id}/documento", response_model=ContratoOut)
async def subir_documento(contrato_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    service = ContratoService(ContratoRepository(db))
    contrato = service.obtener(contrato_id)
    ext = Path(file.filename or "doc.pdf").suffix or ".pdf"
    filename = f"contrato_{contrato_id}_{uuid.uuid4().hex}{ext}"
    subdir = Path(settings.UPLOAD_DIR) / "contratos"
    subdir.mkdir(parents=True, exist_ok=True)
    filepath = subdir / filename
    filepath.write_bytes(await file.read())
    contrato.url_documento = f"contratos/{filename}"
    return service.repo.update(contrato)


@router.delete("/{contrato_id}", status_code=204)
def eliminar(contrato_id: int, db: Session = Depends(get_db)):
    ContratoService(ContratoRepository(db)).eliminar(contrato_id)


@router.post("/{contrato_id}/restaurar")
def restaurar(contrato_id: int, db: Session = Depends(get_db)):
    ContratoService(ContratoRepository(db)).restaurar(contrato_id)
    return {"message": "Contrato restaurado exitosamente"}
