from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.routers import (
    usuario,
    auth,
    rol,
    categoria_activo,
    cliente,
    activo,
    contrato,
    pago,
    asignacion_activo,
    historial_ubicacion,
    checklist_estado,
    reporte_incidencia,
    mantenimiento,
    activo_foto,
    dashboard,
    informe,
)

app = FastAPI(title=settings.APP_NAME, version=settings.VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(usuario.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1")
app.include_router(rol.router, prefix="/api/v1")
app.include_router(categoria_activo.router, prefix="/api/v1")
app.include_router(cliente.router, prefix="/api/v1")
app.include_router(activo.router, prefix="/api/v1")
app.include_router(contrato.router, prefix="/api/v1")
app.include_router(pago.router, prefix="/api/v1")
app.include_router(asignacion_activo.router, prefix="/api/v1")
app.include_router(historial_ubicacion.router, prefix="/api/v1")
app.include_router(checklist_estado.router, prefix="/api/v1")
app.include_router(reporte_incidencia.router, prefix="/api/v1")
app.include_router(mantenimiento.router, prefix="/api/v1")
app.include_router(activo_foto.router, prefix="/api/v1")
app.include_router(dashboard.router, prefix="/api/v1")
app.include_router(informe.router, prefix="/api/v1")

static_dir = Path(settings.UPLOAD_DIR).resolve()
static_dir.mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


@app.get("/api/v1/health")
def health():
    return {"status": "ok", "version": settings.VERSION}
