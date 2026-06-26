import uuid
from pathlib import Path

from fastapi import HTTPException, UploadFile, status

from app.core.config import settings
from app.models.activo import Activo
from app.models.activo_foto import ActivoFoto
from app.repositories.activo_foto import ActivoFotoRepository
from app.repositories.activo import ActivoRepository


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

    def subir(self, activo_id: int, file: UploadFile) -> ActivoFoto:
        self._get_activo(activo_id)

        ext = Path(file.filename or "foto.jpg").suffix or ".jpg"
        filename = f"{uuid.uuid4().hex}{ext}"
        subdir = Path(settings.UPLOAD_DIR) / "activos"
        subdir.mkdir(parents=True, exist_ok=True)
        filepath = subdir / filename

        content = file.read()
        filepath.write_bytes(content)

        rel_path = f"activos/{filename}"
        fotos = self.repo.get_by_activo(activo_id)
        orden = max((f.orden for f in fotos), default=-1) + 1

        foto = ActivoFoto(id_activo=activo_id, url=rel_path, orden=orden)
        return self.repo.create(foto)

    def eliminar(self, activo_id: int, foto_id: int) -> None:
        self._get_activo(activo_id)
        foto = self.repo.get_by_id(foto_id)
        if not foto or foto.id_activo != activo_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Foto no encontrada")

        filepath = Path(settings.UPLOAD_DIR) / "activos" / Path(foto.url).name
        if filepath.exists():
            filepath.unlink()

        self.repo.delete(foto)
