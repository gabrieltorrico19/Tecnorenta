from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.activo import ActivoRepository
from app.repositories.activo_foto import ActivoFotoRepository
from app.services.activo_foto import ActivoFotoService
from app.schemas.activo_foto import ActivoFotoOut

router = APIRouter(prefix="/activos", tags=["Fotos de Activos"])


@router.get("/{activo_id}/fotos", response_model=list[ActivoFotoOut])
def listar_fotos(activo_id: int, db: Session = Depends(get_db)):
    return ActivoFotoService(ActivoFotoRepository(db), ActivoRepository(db)).listar(activo_id)


@router.post("/{activo_id}/fotos", response_model=ActivoFotoOut, status_code=201)
def subir_foto(activo_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    return ActivoFotoService(ActivoFotoRepository(db), ActivoRepository(db)).subir(activo_id, file)


@router.delete("/{activo_id}/fotos/{foto_id}", status_code=204)
def eliminar_foto(activo_id: int, foto_id: int, db: Session = Depends(get_db)):
    ActivoFotoService(ActivoFotoRepository(db), ActivoRepository(db)).eliminar(activo_id, foto_id)
