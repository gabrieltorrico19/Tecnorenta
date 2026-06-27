# SIGTAR — Sistema de Gestión y Trazabilidad de Activos Rentados

## Objetivo

Plataforma web diseñada para **TecnoRenta Latam**, PYME dedicada al alquiler de equipos tecnológicos. Centraliza la operación actual en una sola plataforma con:

- Gestión de inventario con estados y categorías
- Contratos digitales con alertas de vencimiento
- Asignación de activos con checklist fotográfico
- Mapa de trazabilidad GPS + historial por equipo
- Dashboard con KPIs en tiempo real
- Reportes de incidencias y mantenimiento
- Control de pagos

## Stack tecnológico

| Capa | Tecnología |
|---|---|
| Backend | Python 3.14+, FastAPI, SQLAlchemy 2.0, Alembic, PyMySQL, Pydantic v2 |
| Base de datos | MySQL (MariaDB) |
| Autenticación | JWT + bcrypt |
| Mapas | Leaflet.js + OpenStreetMap |

## Módulos del sistema

1. **Usuarios y roles** — autenticación JWT, roles (Administrador/Operador/Cliente), auditoría
2. **Activos** — catálogo con códigos de inventario, estados fijos (disponible/rentado/mantenimiento/baja), categorías jerárquicas, fotos múltiples
3. **Clientes** — registro con NIT único
4. **Contratos** — contratos digitales con cliente y activos asociados, alertas de vencimiento, documento adjunto
5. **Pagos** — control de pagos por contrato, detección de vencidos y próximos
6. **Asignaciones** — entrega/devolución con ubicación GPS, checklist fotográfico
7. **Incidencias** — reportes con gravedad (leve/moderado/grave), ciclo de vida
8. **Mantenimiento** — preventivo programado, correctivo vinculado a incidencias
9. **Dashboard** — panel con KPIs, gráficos, alertas de contratos próximos a vencer

## Estructura del backend

```
Tecnorenta_Backend/
├── app/
│   ├── core/          # Config, database, security
│   ├── models/        # SQLAlchemy models (15 tablas)
│   ├── schemas/       # Pydantic request/response
│   ├── repositories/  # Acceso a datos (queries)
│   ├── services/      # Lógica de negocio + validaciones
│   ├── routers/       # Endpoints REST (API prefix /api/v1)
│   └── dependencies/  # Inyección de dependencias
├── alembic/           # Migraciones DB
│   └── versions/
└── .env.example       # Template de configuración
```

## Endpoints destacados (API v1)

- `GET /api/v1/dashboard/stats` — KPIs generales (conteos, ingresos, alertas)
- `GET /api/v1/dashboard/contratos-proximos-vencer?dias=30` — contratos por vencer
- `GET /api/v1/activos/exportar/formato-csv` — exportar activos a CSV
- `GET /api/v1/pagos/vencidos` — pagos vencidos
- `GET /api/v1/pagos/proximos` — pagos próximos (pendientes)
- `POST /api/v1/contratos/{id}/documento` — subir documento a contrato
- CRUD completo para: usuarios, roles, activos, categorías, clientes, contratos, pagos, asignaciones, incidencias, mantenimiento, checklist, historial ubicación

## Cómo ejecutar

```bash
# Backend
cd Tecnorenta_Backend
python -m venv venv
venv\Scripts\activate    # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# Migraciones
alembic upgrade head

# Frontend
cd ../Tecnorenta_Frontend
npm install
npm run dev
```

## Configuración

Copiar `.env.example` a `.env` y ajustar:

- `DATABASE_URL` — conexión MySQL (ej: `mysql+pymysql://root:root@localhost:3306/tecnorenta?charset=utf8mb4`)
- `SECRET_KEY` — clave para JWT

## Convenciones

| Regla | Estándar |
|---|---|
| Idioma | Español (tablas, columnas, endpoints) |
| Python | snake_case, PEP 8 |
| API prefix | `/api/v1/...` |
| Estados | ENUMs de SQLAlchemy |
| Arquitectura | Router → Service → Repository → Model |
| DI | `Depends(get_db)` |
| Validaciones | En servicios (no en routers) |
| Auditoría | `creado_por`, `fecha_creacion`, `modificado_por`, `fecha_modificacion` |
