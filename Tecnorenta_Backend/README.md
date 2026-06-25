# SIGTAR — Sistema de Gestión y Trazabilidad de Activos Rentados

## Objetivo

Plataforma web diseñada para **TecnoRenta Latam**, PYME dedicada al alquiler de laptops a domicilio. El sistema centraliza la operación actual (inventario en Excel, entregas por WhatsApp, checklists en papel) en una sola plataforma con:

- Mapa de trazabilidad GPS
- Historial por equipo
- Contratos digitales
- Control de mantenimiento
- Dashboard con KPIs

## Usuarios del sistema

| Rol | Acceso |
|---|---|
| **Administrador** | Total: inventario, contratos, reportes, dashboard KPIs |
| **Operador / Repartidor** | Móvil: checklists de entrega/devolución, fotos, GPS |
| **Cliente** | Solo lectura: contrato activo, estado del equipo, historial de pagos |

## Stack tecnológico

| Capa | Tecnología |
|---|---|
| Backend | Python 3.14+, FastAPI, SQLAlchemy 2.0, Alembic, PyMySQL |
| Frontend | React 19, TypeScript, Vite, Axios, React Router DOM |
| Base de datos | MySQL (local) / Railway (producción) |
| Autenticación | JWT + bcrypt |
| Mapas | Leaflet.js + OpenStreetMap |

## Módulos del sistema

1. **Gestión de usuarios y roles** — registro, permisos, autenticación JWT, auditoría
2. **Inventario de activos** — catálogo de laptops con estados fijos y categorías jerárquicas
3. **Clientes y contratos** — registro con NIT único, contratos digitales, alertas de vencimiento, pagos
4. **Asignación y checklist** — entrega/devolución con checklist fotográfico, comparación automática, cargos por daño
5. **Mapa de trazabilidad** — ubicación actual + historial GPS por equipo, mapa de calor de entregas
6. **Reportes de incidencia** — reportes con gravedad (leve, moderado, grave), ciclo de vida, escalado a correctivo
7. **Mantenimiento** — preventivo programado por frecuencia, correctivo vinculado a incidencias, costos por equipo

## Estructura del backend

```
Tecnorenta_Backend/
├── app/
│   ├── core/          # Config, database, security
│   ├── models/        # SQLAlchemy models (14 tablas)
│   ├── schemas/       # Pydantic request/response
│   ├── repositories/  # Acceso a datos
│   ├── services/      # Lógica de negocio
│   ├── routers/       # Endpoints API REST
│   └── dependencies/  # Inyección de dependencias
├── alembic/           # Migraciones
│   └── versions/
└── requirements.txt
```

## Convenciones de desarrollo

| Regla | Estándar |
|---|---|
| Idioma en código | Español (tablas, columnas, endpoints) |
| Python | snake_case, PEP 8 |
| API prefix | `/api/v1/...` |
| Estados fijos | ENUMs de SQLAlchemy |
| Arquitectura | Router → Service → Repository → Model |
| Auditoría | `creado_por`, `fecha_creacion`, `modificado_por`, `fecha_modificacion` en tablas críticas |
| Herencia | Single table inheritance (Mantenimiento) |

## Cómo ejecutar

```bash
# Backend
cd Tecnorenta_Backend
venv\Scripts\activate
uvicorn app.main:app --reload

# Migraciones (cuando MySQL esté corriendo)
alembic upgrade head

# Frontend
cd Tecnorenta_Frontend
npm run dev
```

## Vinculación con ODS

- **ODS 8** — Trabajo decente y crecimiento económico
- **ODS 9** — Industria, innovación e infraestructura
- **ODS 12** — Producción y consumo responsables

## Fases del proyecto

| Fase | Semanas | Módulos |
|---|---|---|
| 1 | 1-2 | Base de datos, autenticación, roles |
| 2 | 3-4 | Inventario, clientes, contratos |
| 3 | 5-6 | Asignación y checklist |
| 4 | 7-8 | Mapa y trazabilidad |
| 5 | 9-10 | Incidencias y mantenimiento |
| 6 | 11-12 | Dashboard, pruebas, documentación |
