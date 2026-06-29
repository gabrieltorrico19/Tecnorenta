import os
import shutil
from datetime import date

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.contrato import Contrato

router = APIRouter(prefix="/documentos", tags=["Documentos"])

UPLOAD_DIR = "uploads/contratos"
os.makedirs(UPLOAD_DIR, exist_ok=True)
ALLOWED_TYPES = {"application/pdf", "image/jpeg", "image/png"}
MAX_SIZE_MB = 10


# US-21: Adjuntar documento escaneado al contrato
@router.post("/contratos/{contrato_id}")
def adjuntar_documento_contrato(
    contrato_id: int,
    archivo: UploadFile = File(..., description="Archivo PDF o imagen del contrato escaneado"),
    db: Session = Depends(get_db),
):
    contrato = db.query(Contrato).filter(Contrato.id == contrato_id).first()
    if not contrato:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contrato no encontrado")

    if archivo.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Tipo de archivo no permitido. Se aceptan: PDF, JPG, PNG",
        )

    contenido = archivo.file.read()
    if len(contenido) > MAX_SIZE_MB * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El archivo supera el límite de {MAX_SIZE_MB} MB",
        )

    extension = archivo.filename.split(".")[-1].lower()
    nombre_archivo = f"contrato_{contrato_id}_{date.today()}.{extension}"
    ruta = os.path.join(UPLOAD_DIR, nombre_archivo)

    with open(ruta, "wb") as f:
        f.write(contenido)

    # Borrar archivo anterior si existía
    if contrato.url_documento and os.path.exists(contrato.url_documento):
        os.remove(contrato.url_documento)

    contrato.url_documento = ruta
    db.commit()

    return {
        "success": True,
        "errors": [],
        "mensaje": "Documento adjuntado correctamente",
        "url_documento": ruta,
        "contrato_id": contrato_id,
    }


@router.get("/contratos/{contrato_id}")
def obtener_documento_contrato(contrato_id: int, db: Session = Depends(get_db)):
    contrato = db.query(Contrato).filter(Contrato.id == contrato_id).first()
    if not contrato:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contrato no encontrado")
    if not contrato.url_documento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Este contrato no tiene documento adjunto")

    return {
        "success": True,
        "errors": [],
        "contrato_id": contrato_id,
        "url_documento": contrato.url_documento,
    }
