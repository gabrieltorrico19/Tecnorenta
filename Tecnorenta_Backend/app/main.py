from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.config import settings
from app.routers import (
    usuario,
    rol,
    cliente,
    categoria_activo,
    activo,
    contrato,
    pago,
    asignacion_activo,
    checklist_estado,
    reporte_incidencia,
    mantenimiento,
    reportes,
    exportar,
    auth,
    documentos,
)

app = FastAPI(title=settings.APP_NAME, version=settings.VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for error in exc.errors():
        field = " -> ".join(str(loc) for loc in error["loc"] if loc != "body")
        errors.append({"campo": field, "mensaje": error["msg"]})
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"success": False, "errors": errors},
    )


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "errors": [{"mensaje": exc.detail}]},
    )


PREFIX = "/api/v1"

app.include_router(usuario.router, prefix=PREFIX)
app.include_router(rol.router, prefix=PREFIX)
app.include_router(cliente.router, prefix=PREFIX)
app.include_router(categoria_activo.router, prefix=PREFIX)
app.include_router(activo.router, prefix=PREFIX)
app.include_router(contrato.router, prefix=PREFIX)
app.include_router(pago.router, prefix=PREFIX)
app.include_router(asignacion_activo.router, prefix=PREFIX)
app.include_router(checklist_estado.router, prefix=PREFIX)
app.include_router(reporte_incidencia.router, prefix=PREFIX)
app.include_router(mantenimiento.router, prefix=PREFIX)
app.include_router(reportes.router, prefix=PREFIX)
app.include_router(exportar.router, prefix=PREFIX)
app.include_router(auth.router, prefix=PREFIX)
app.include_router(documentos.router, prefix=PREFIX)


@app.get(f"{PREFIX}/health")
def health():
    return {"success": True, "data": {"status": "ok", "version": settings.VERSION}}
