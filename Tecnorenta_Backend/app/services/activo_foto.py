import io
import uuid
from pathlib import Path

import cloudinary
from cloudinary import uploader
from fastapi import HTTPException, UploadFile, status

from app.core.config import settings
from app.models.activo import Activo
from app.models.activo_foto import ActivoFoto
from app.repositories.activo_foto import ActivoFotoRepository
from app.repositories.activo import ActivoRepository

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
MAX_FILE_SIZE = 10 * 1024 * 1024

cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET,
)


class ActivoFotoService:
    def __init__(self, repo: ActivoFotoRepository, activo_repo: ActivoRepository):
        self.repo = repo
        self.activo_repo = activo_repo

    def _get_activo(self, activo_id: int) -> Activo:
        activo = self.activo_repo.get_by_id(activo_id)
        if not activo:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Activo no encontrado")
        return activo

    def listar(self, activo_id: int) -> list[ActivoFoto]:
        self._get_activo(activo_id)
        return self.repo.get_by_activo(activo_id)

    async def subir(self, activo_id: int, file: UploadFile) -> ActivoFoto:
        self._get_activo(activo_id)

        ext = (Path(file.filename or "foto.jpg").suffix or ".jpg").lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Formato de archivo no permitido: {ext}")

        content = await file.read()
        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail="Archivo demasiado grande (máx 10MB)")

        public_id = f"activos/{activo_id}/{uuid.uuid4().hex}"
        result = uploader.upload(
            io.BytesIO(content),
            public_id=public_id,
            overwrite=True,
        )

        url = result.get("secure_url")
        if not url:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al subir imagen a Cloudinary")

        fotos = self.repo.get_by_activo(activo_id)
        orden = max((f.orden for f in fotos), default=-1) + 1

        foto = ActivoFoto(id_activo=activo_id, url=url, orden=orden)
        return self.repo.create(foto)

    def eliminar(self, activo_id: int, foto_id: int) -> None:
        self._get_activo(activo_id)
        foto = self.repo.get_by_id(foto_id)
        if not foto or foto.id_activo != activo_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Foto no encontrada")

        if "/upload/" in foto.url:
            # Extract public_id from Cloudinary URL
            parts = foto.url.split("/upload/")
            if len(parts) > 1:
                path = parts[1].split("/", 1)[1] if "/" in parts[1] else parts[1]
                public_id = path.rsplit(".", 1)[0]  # remove extension
                # Remove version prefix (v1234567890/)
                if public_id.startswith("v") and "/" in public_id:
                    public_id = public_id.split("/", 1)[1]
                try:
                    uploader.destroy(public_id)
                except Exception:
                    pass

        self.repo.delete(foto)
