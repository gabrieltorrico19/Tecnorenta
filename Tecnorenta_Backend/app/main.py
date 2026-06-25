from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routers import usuario, auth, rol, categoria_activo, cliente

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


@app.get("/api/v1/health")
def health():
    return {"status": "ok", "version": settings.VERSION}
