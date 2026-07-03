import csv
import io
from datetime import date

from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.informe import InformeService
from app.schemas.informe import TipoInformeOut, InformeOut

router = APIRouter(prefix="/informes", tags=["Informes"])


# NOTA: /tipos debe declararse ANTES que /{tipo} para que la ruta literal
# tenga precedencia sobre el parámetro de path.
@router.get("/tipos", response_model=list[TipoInformeOut])
def tipos(db: Session = Depends(get_db)):
    """Catálogo de informes disponibles con sus filtros y opciones."""
    return InformeService(db).get_tipos()


@router.get("/{tipo}", response_model=InformeOut)
def generar(
    tipo: str,
    estado: str | None = Query(None, description="Estado (según el informe)"),
    gravedad: str | None = Query(None, description="Gravedad de incidencia"),
    tipo_mantenimiento: str | None = Query(None, description="preventivo | correctivo"),
    id_categoria: int | None = Query(None),
    id_cliente: int | None = Query(None),
    fecha_desde: date | None = Query(None),
    fecha_hasta: date | None = Query(None),
    db: Session = Depends(get_db),
):
    return InformeService(db).generar(
        tipo,
        estado=estado,
        gravedad=gravedad,
        tipo_mantenimiento=tipo_mantenimiento,
        id_categoria=id_categoria,
        id_cliente=id_cliente,
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta,
    )


@router.get("/{tipo}/csv")
def exportar_csv(
    tipo: str,
    estado: str | None = Query(None),
    gravedad: str | None = Query(None),
    tipo_mantenimiento: str | None = Query(None),
    id_categoria: int | None = Query(None),
    id_cliente: int | None = Query(None),
    fecha_desde: date | None = Query(None),
    fecha_hasta: date | None = Query(None),
    db: Session = Depends(get_db),
):
    informe = InformeService(db).generar(
        tipo,
        estado=estado,
        gravedad=gravedad,
        tipo_mantenimiento=tipo_mantenimiento,
        id_categoria=id_categoria,
        id_cliente=id_cliente,
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta,
        limite=None,
    )
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([c.label for c in informe.columnas])
    for fila in informe.filas:
        writer.writerow([fila.get(c.key, "") for c in informe.columnas])
    output.seek(0)
    # BOM UTF-8 al inicio para que Excel detecte los acentos correctamente.
    contenido = "﻿" + output.getvalue()
    return StreamingResponse(
        iter([contenido]),
        media_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": f"attachment; filename=informe_{tipo}_{informe.generado}.csv"},
    )
