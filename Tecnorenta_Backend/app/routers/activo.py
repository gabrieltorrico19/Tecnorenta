import csv
import io

from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_current_user, require_role
from app.models.activo import EstadoActivo
from app.models.usuario import Usuario
from app.repositories.activo import ActivoRepository
from app.services.activo import ActivoService
from app.schemas.activo import ActivoCreate, ActivoUpdate, ActivoOut
from app.schemas.common import Page, paginate
from app.dependencies.pagination import PaginationParams

router = APIRouter(prefix="/activos", tags=["Activos"])


@router.get("/", response_model=Page[ActivoOut])
def listar(
    pagination: PaginationParams = Depends(),
    estado: EstadoActivo | None = Query(None, description="Filtrar por estado"),
    id_categoria: int | None = Query(None, description="Filtrar por categoría"),
    q: str | None = Query(None, max_length=100, description="Buscar por código, modelo o serie"),
    db: Session = Depends(get_db),
):
    items, total = ActivoService(ActivoRepository(db)).listar(
        pagination.skip, pagination.limit, estado=estado, id_categoria=id_categoria, q=q
    )
    return paginate(items, total, pagination.page, pagination.page_size)


@router.get("/{activo_id}", response_model=ActivoOut)
def obtener(activo_id: int, db: Session = Depends(get_db)):
    return ActivoService(ActivoRepository(db)).obtener(activo_id)


@router.post("/", response_model=ActivoOut, status_code=201)
def crear(data: ActivoCreate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    return ActivoService(ActivoRepository(db)).crear(data)


@router.patch("/{activo_id}", response_model=ActivoOut)
def actualizar(activo_id: int, data: ActivoUpdate, db: Session = Depends(get_db)):
    return ActivoService(ActivoRepository(db)).actualizar(activo_id, data)


@router.get("/exportar/formato-csv")
def exportar_csv(db: Session = Depends(get_db)):
    activos = ActivoService(ActivoRepository(db)).listar_todos()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "Codigo Inventario", "Modelo", "Numero Serie", "Estado", "Categoria", "Valor Depreciado", "Fecha Compra"])
    for a in activos:
        cat = a.categoria.nombre if a.categoria else ""
        writer.writerow([a.id, a.codigo_inventario, a.modelo, a.numero_serie,
                        a.estado.value if hasattr(a.estado, "value") else a.estado,
                        cat, a.valor_depreciado, a.fecha_compra])
    output.seek(0)
    return StreamingResponse(iter([output.getvalue()]), media_type="text/csv",
                             headers={"Content-Disposition": "attachment; filename=activos.csv"})


@router.delete("/{activo_id}", status_code=204, dependencies=[Depends(require_role("Administrador"))])
def eliminar(activo_id: int, db: Session = Depends(get_db)):
    ActivoService(ActivoRepository(db), db=db).eliminar(activo_id)


@router.post("/{activo_id}/restaurar")
def restaurar(activo_id: int, db: Session = Depends(get_db)):
    ActivoService(ActivoRepository(db)).restaurar(activo_id)
    return {"message": "Activo restaurado exitosamente"}
