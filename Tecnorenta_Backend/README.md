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

1. **Usuarios y roles** — autenticación JWT + bcrypt, roles (Administrador/Gerente/Almacén/Técnico/Operador/Cliente), 33 permisos asignables, auditoría
2. **Clientes** — registro con NIT único, dirección, geolocalización con mapa Leaflet
3. **Activos** — catálogo con códigos de inventario únicos, estados fijos (disponible/rentado/mantenimiento/baja), categorías jerárquicas, fotos múltiples (cámara/archivo), exportación CSV, geoposicionamiento GPS
4. **Categorías** — jerarquía auto-referenciada (padre → hijo), niveles
5. **Contratos** — contratos digitales con cliente, montos mensuales, alertas de vencimiento, documento adjunto (PDF/doc)
6. **Pagos** — control de pagos por contrato, detección de vencidos y próximos, conceptos
7. **Asignaciones** — entrega/devolución con ubicación GPS, vincula activo ↔ contrato
8. **Checklist Estado** — evaluación de componentes en entrega y devolución (pantalla, teclado, carcasa, cargador), con fotos
9. **Historial Ubicación** — registro de coordenadas GPS por asignación con timestamp
10. **Reportes de Incidencia** — reportes con gravedad (leve/moderado/grave), ciclo de vida (abierto/en_atencion/cerrado), foto adjunta
11. **Mantenimiento** — preventivo programado (frecuencia en días), correctivo vinculado a incidencias, con costo y tiempo de reparación
12. **Dashboard** — panel con 7 KPIs (usuarios, clientes, activos, contratos, ingresos mensuales, próximos a vencer, incidencias), 2 gráficos Recharts (barras + pastel), 6 consultas SQL complejas

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

## Documentación del proyecto

| Recurso | Ubicación |
|---------|-----------|
| Informe Sprint 2 (APA 7) | `informe/Sprint2/SIGTAR_Sprint2_Informe_APA7.docx` |
| Presentación Sprint 1+2 | `informe/Sprint2/SIGTAR_Sprint1_Sprint2_Presentacion.pptx` |
| Especificación OpenAPI | `informe/Sprint2/tecnorenta_openapi.json` (importable a Postman) |
| Capturas del sistema | `informe/Sprint2/capturas/` (16 capturas) |
| Dump de base de datos | `informe/Sprint2/tecnorenta.sql` |

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
