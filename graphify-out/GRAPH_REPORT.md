# Graph Report - .  (2026-06-30)

## Corpus Check
- Corpus is ~30,295 words - fits in a single context window. You may not need a graph.

## Summary
- 1104 nodes · 2051 edges · 88 communities (80 shown, 8 thin omitted)
- Extraction: 82% EXTRACTED · 18% INFERRED · 0% AMBIGUOUS · INFERRED: 372 edges (avg confidence: 0.59)
- Token cost: 83,600 input · 7,000 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Database Seed Scripts|Database Seed Scripts]]
- [[_COMMUNITY_Roles & Permissions (Backend)|Roles & Permissions (Backend)]]
- [[_COMMUNITY_Auth & Security|Auth & Security]]
- [[_COMMUNITY_Maintenance Module (Backend)|Maintenance Module (Backend)]]
- [[_COMMUNITY_Location History (Backend)|Location History (Backend)]]
- [[_COMMUNITY_Contracts Module (Backend)|Contracts Module (Backend)]]
- [[_COMMUNITY_Shared UI Components|Shared UI Components]]
- [[_COMMUNITY_Clients & Contracts (Frontend)|Clients & Contracts (Frontend)]]
- [[_COMMUNITY_Checklist State (Backend)|Checklist State (Backend)]]
- [[_COMMUNITY_Asset Photos (Backend)|Asset Photos (Backend)]]
- [[_COMMUNITY_Auth Context & Dashboard (Frontend)|Auth Context & Dashboard (Frontend)]]
- [[_COMMUNITY_Frontend Dependencies|Frontend Dependencies]]
- [[_COMMUNITY_Payments Service (Backend)|Payments Service (Backend)]]
- [[_COMMUNITY_Checklist State (Frontend)|Checklist State (Frontend)]]
- [[_COMMUNITY_Frontend API Client Layer|Frontend API Client Layer]]
- [[_COMMUNITY_Clients Service (Backend)|Clients Service (Backend)]]
- [[_COMMUNITY_Incident Reports Service (Backend)|Incident Reports Service (Backend)]]
- [[_COMMUNITY_Assets Module (Frontend)|Assets Module (Frontend)]]
- [[_COMMUNITY_Assets Service (Backend)|Assets Service (Backend)]]
- [[_COMMUNITY_Categories Service (Backend)|Categories Service (Backend)]]
- [[_COMMUNITY_TS App Config|TS App Config]]
- [[_COMMUNITY_Assignments & Map Picker (Frontend)|Assignments & Map Picker (Frontend)]]
- [[_COMMUNITY_App Shell & Toasts (Frontend)|App Shell & Toasts (Frontend)]]
- [[_COMMUNITY_TS Node Config|TS Node Config]]
- [[_COMMUNITY_Maintenance Module (Frontend)|Maintenance Module (Frontend)]]
- [[_COMMUNITY_Payments Module (Frontend)|Payments Module (Frontend)]]
- [[_COMMUNITY_Incident Reports (Frontend)|Incident Reports (Frontend)]]
- [[_COMMUNITY_API Docs & Modules|API Docs & Modules]]
- [[_COMMUNITY_Categories Module (Frontend)|Categories Module (Frontend)]]
- [[_COMMUNITY_Backend Setup Docs|Backend Setup Docs]]
- [[_COMMUNITY_Tech Stack & Skills Docs|Tech Stack & Skills Docs]]
- [[_COMMUNITY_Users Module (Frontend)|Users Module (Frontend)]]
- [[_COMMUNITY_Auth & Dashboard Schemas|Auth & Dashboard Schemas]]
- [[_COMMUNITY_Assets Repository|Assets Repository]]
- [[_COMMUNITY_Roles Module (Frontend)|Roles Module (Frontend)]]
- [[_COMMUNITY_Frontend Structure Docs|Frontend Structure Docs]]
- [[_COMMUNITY_Clients Repository|Clients Repository]]
- [[_COMMUNITY_Payments Repository|Payments Repository]]
- [[_COMMUNITY_Users Service (Backend)|Users Service (Backend)]]
- [[_COMMUNITY_Camera Capture Component|Camera Capture Component]]
- [[_COMMUNITY_Assignments Repository|Assignments Repository]]
- [[_COMMUNITY_Categories Repository|Categories Repository]]
- [[_COMMUNITY_Incident Reports Repository|Incident Reports Repository]]
- [[_COMMUNITY_Roles & Permissions Schemas|Roles & Permissions Schemas]]
- [[_COMMUNITY_Searchable Select Component|Searchable Select Component]]
- [[_COMMUNITY_Project State & Sprints Docs|Project State & Sprints Docs]]
- [[_COMMUNITY_Oxlint Config|Oxlint Config]]
- [[_COMMUNITY_Alembic Migration Env|Alembic Migration Env]]
- [[_COMMUNITY_Assets Schema|Assets Schema]]
- [[_COMMUNITY_Assignments Schema|Assignments Schema]]
- [[_COMMUNITY_Categories Schema|Categories Schema]]
- [[_COMMUNITY_Checklist Schema|Checklist Schema]]
- [[_COMMUNITY_Clients Schema|Clients Schema]]
- [[_COMMUNITY_Contracts Schema|Contracts Schema]]
- [[_COMMUNITY_Location History Schema|Location History Schema]]
- [[_COMMUNITY_Maintenance Schema|Maintenance Schema]]
- [[_COMMUNITY_Payments Schema|Payments Schema]]
- [[_COMMUNITY_Incident Reports Schema|Incident Reports Schema]]
- [[_COMMUNITY_Users Schema|Users Schema]]
- [[_COMMUNITY_Auth Conventions & Deps|Auth Conventions & Deps]]
- [[_COMMUNITY_Dashboard Endpoints Docs|Dashboard Endpoints Docs]]
- [[_COMMUNITY_Payments Endpoints Docs|Payments Endpoints Docs]]
- [[_COMMUNITY_Placeholder Asset Photos|Placeholder Asset Photos]]
- [[_COMMUNITY_App Settings|App Settings]]
- [[_COMMUNITY_TS Root Config|TS Root Config]]
- [[_COMMUNITY_Vite & Favicon Logos|Vite & Favicon Logos]]
- [[_COMMUNITY_Laptop Icon Placeholder|Laptop Icon Placeholder]]
- [[_COMMUNITY_UI Icon Sprite Sheet|UI Icon Sprite Sheet]]
- [[_COMMUNITY_Pydantic Email Dep|Pydantic Email Dep]]
- [[_COMMUNITY_Dotenv Dep|Dotenv Dep]]
- [[_COMMUNITY_Uvicorn Dep|Uvicorn Dep]]

## God Nodes (most connected - your core abstractions)
1. `Activo` - 37 edges
2. `Usuario` - 35 edges
3. `useToast()` - 31 edges
4. `Rol` - 22 edges
5. `AsignacionActivo` - 21 edges
6. `Pago` - 21 edges
7. `SIGTAR — Sistema de Gestión y Trazabilidad de Activos Rentados` - 19 edges
8. `Cliente` - 18 edges
9. `Contrato` - 18 edges
10. `ReporteIncidencia` - 18 edges

## Surprising Connections (you probably didn't know these)
- `sql-pro skill` --semantically_similar_to--> `Módulo Dashboard (7 KPIs, Recharts)`  [INFERRED] [semantically similar]
  SKILLS.md → Tecnorenta_Backend/README.md
- `tecnorenta project skill` --semantically_similar_to--> `MySQL local vía DATABASE_URL (.env)`  [INFERRED] [semantically similar]
  SKILLS.md → Tecnorenta_Backend/AGENTS.md
- `security-reviewer skill` --conceptually_related_to--> `AuthContext con localStorage + JWT`  [INFERRED]
  SKILLS.md → Tecnorenta_Backend/AGENTS.md
- `SIGTAR project state v2.0.0` --conceptually_related_to--> `SIGTAR — Sistema de Gestión y Trazabilidad de Activos Rentados`  [INFERRED]
  SKILLS.md → Tecnorenta_Backend/README.md
- `Session` --uses--> `Activo`  [INFERRED]
  Tecnorenta_Backend/app/repositories/activo.py → Tecnorenta_Backend/app/models/activo.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Trazabilidad GPS compartida entre Activos, Asignaciones e Historial Ubicación** — readme_modulo_activos, readme_modulo_asignaciones, readme_modulo_historial_ubicacion, readme_modulo_clientes [EXTRACTED 0.90]
- **Patrón de arquitectura en capas Router-Service-Repository-Model aplicado a todo el backend** — agents_arquitectura_backend, readme_estructura_backend, readme_convenciones_backend, backend_agents_md [EXTRACTED 0.95]
- **Entregables de documentación técnica generados en Sprint 2** — skills_sprint2_informe, skills_sprint_presentacion, skills_tecnorenta_openapi_json, skills_sigtar_project_state_v2 [EXTRACTED 0.90]

## Communities (88 total, 8 thin omitted)

### Community 0 - "Database Seed Scripts"
Cohesion: 0.06
Nodes (61): main(), seed_activos(), seed_asignaciones(), seed_categorias(), seed_clientes(), seed_contratos(), seed_pagos(), seed_reportes() (+53 more)

### Community 1 - "Roles & Permissions (Backend)"
Cohesion: 0.08
Nodes (27): Permiso, Rol, PermisoRepository, PermisoRepository, RolRepository, RolAsignarPermiso, RolRepository, actualizar() (+19 more)

### Community 2 - "Auth & Security"
Cohesion: 0.07
Nodes (29): Any, create_access_token(), hash_password(), verify_password(), get_current_user(), ForgotPasswordRequest, HTTPAuthorizationCredentials, LoginRequest (+21 more)

### Community 3 - "Maintenance Module (Backend)"
Cohesion: 0.09
Nodes (21): MantenimientoRepository, Mantenimiento, MantenimientoCorrectivo, MantenimientoPreventivo, TipoMantenimiento, MantenimientoRepository, actualizar(), crear() (+13 more)

### Community 4 - "Location History (Backend)"
Cohesion: 0.10
Nodes (18): HistorialUbicacionRepository, HistorialUbicacion, HistorialUbicacionRepository, actualizar(), crear(), eliminar(), listar(), listar_por_asignacion() (+10 more)

### Community 5 - "Contracts Module (Backend)"
Cohesion: 0.10
Nodes (19): ContratoRepository, Contrato, ContratoRepository, actualizar(), crear(), eliminar(), listar(), obtener() (+11 more)

### Community 6 - "Shared UI Components"
Cohesion: 0.08
Nodes (24): HistorialUbicacion, historialUbicacionApi, Rol, rolesApi, baseStyle, ButtonProps, iconStyle, variantStyles (+16 more)

### Community 7 - "Clients & Contracts (Frontend)"
Cohesion: 0.09
Nodes (22): Cliente, ClienteCreate, clientesApi, ClienteUpdate, Contrato, ContratoCreate, contratosApi, ContratoUpdate (+14 more)

### Community 8 - "Checklist State (Backend)"
Cohesion: 0.11
Nodes (17): ChecklistEstadoRepository, ChecklistEstado, ChecklistEstadoRepository, actualizar(), crear(), eliminar(), listar_por_asignacion(), obtener() (+9 more)

### Community 9 - "Asset Photos (Backend)"
Cohesion: 0.11
Nodes (16): ActivoFotoRepository, ActivoFoto, ActivoFotoRepository, eliminar_foto(), listar_fotos(), subir_foto(), ActivoFotoService, ActivoFoto (+8 more)

### Community 10 - "Auth Context & Dashboard (Frontend)"
Cohesion: 0.10
Nodes (22): authApi, UserProfile, ContratoProximoVencer, dashboardApi, DashboardStats, Card(), CardProps, styles (+14 more)

### Community 11 - "Frontend Dependencies"
Cohesion: 0.07
Nodes (27): dependencies, axios, leaflet, lucide-react, react, react-dom, react-leaflet, react-router-dom (+19 more)

### Community 12 - "Payments Service (Backend)"
Cohesion: 0.14
Nodes (16): PagoRepository, actualizar(), crear(), eliminar(), listar(), listar_por_contrato(), listar_proximos(), listar_vencidos() (+8 more)

### Community 13 - "Checklist State (Frontend)"
Cohesion: 0.13
Nodes (19): ChecklistEstado, checklistEstadoApi, ChecklistEstadoCreate, ChecklistEstadoUpdate, actionsStyle, estadosComponente, FormularioChecklistEstado(), inputStyle (+11 more)

### Community 14 - "Frontend API Client Layer"
Cohesion: 0.18
Nodes (11): Asignacion, asignacionesApi, LoginRequest, LoginResponse, api, ENDPOINTS, HistorialUbicacionCreate, HistorialUbicacionUpdate (+3 more)

### Community 15 - "Clients Service (Backend)"
Cohesion: 0.16
Nodes (13): ClienteRepository, actualizar(), crear(), eliminar(), listar(), obtener(), ClienteService, ClienteCreate (+5 more)

### Community 16 - "Incident Reports Service (Backend)"
Cohesion: 0.16
Nodes (13): ReporteIncidenciaRepository, actualizar(), crear(), eliminar(), listar(), obtener(), ReporteIncidenciaService, ReporteIncidenciaCreate (+5 more)

### Community 17 - "Assets Module (Frontend)"
Cohesion: 0.13
Nodes (17): actionsStyle, deleteFotoBtn, ESTADOS, FormularioActivo(), fotosGrid, fotoThumb, inputStyle, thumbImg (+9 more)

### Community 18 - "Assets Service (Backend)"
Cohesion: 0.20
Nodes (12): actualizar(), crear(), eliminar(), exportar_csv(), listar(), obtener(), ActivoService, ActivoCreate (+4 more)

### Community 19 - "Categories Service (Backend)"
Cohesion: 0.18
Nodes (12): actualizar(), crear(), eliminar(), listar(), obtener(), CategoriaActivoService, CategoriaActivoCreate, CategoriaActivoUpdate (+4 more)

### Community 20 - "TS App Config"
Cohesion: 0.11
Nodes (18): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection, moduleResolution (+10 more)

### Community 21 - "Assignments & Map Picker (Frontend)"
Cohesion: 0.12
Nodes (13): AsignacionCreate, AsignacionUpdate, actionsStyle, FormularioAsignacion(), inputStyle, FormSection(), FormSectionProps, grid (+5 more)

### Community 22 - "App Shell & Toasts (Frontend)"
Cohesion: 0.13
Nodes (14): FormularioCategoria(), closeBtnStyle, colorMap, containerStyle, iconMap, Toast, ToastContext, ToastContextType (+6 more)

### Community 23 - "TS Node Config"
Cohesion: 0.12
Nodes (16): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+8 more)

### Community 24 - "Maintenance Module (Frontend)"
Cohesion: 0.16
Nodes (12): Mantenimiento, MantenimientoCreate, mantenimientosApi, MantenimientoUpdate, actionsStyle, estadoOpciones, FormularioMantenimiento(), inputStyle (+4 more)

### Community 25 - "Payments Module (Frontend)"
Cohesion: 0.15
Nodes (11): Pago, PagoCreate, pagosApi, PagoUpdate, actionsStyle, estados, FormularioPago(), inputStyle (+3 more)

### Community 26 - "Incident Reports (Frontend)"
Cohesion: 0.17
Nodes (12): Reporte, ReporteCreate, reportesApi, ReporteUpdate, actionsStyle, ESTADOS, FormularioReporte(), inputStyle (+4 more)

### Community 27 - "API Docs & Modules"
Cohesion: 0.16
Nodes (16): SIGTAR — Sistema de Gestión y Trazabilidad de Activos Rentados, /activos, /asignaciones, /contratos, /historial-ubicacion, GET /api/v1/activos/exportar/formato-csv, POST /api/v1/contratos/{id}/documento, Módulo Activos (+8 more)

### Community 28 - "Categories Module (Frontend)"
Cohesion: 0.22
Nodes (11): Categoria, CategoriaCreate, categoriasApi, CategoriaUpdate, actionsStyle, formStyle, inputStyle, columns (+3 more)

### Community 29 - "Backend Setup Docs"
Cohesion: 0.17
Nodes (13): Arquitectura Backend: Router → Service → Repository → Model, Auditoría: creado_por, fecha_creacion, modificado_por, fecha_modificacion, Convenciones de código backend, Herencia single table inheritance (Mantenimiento, columna tipo), Reglas generales del agente (no README no solicitado, no comentarios innecesarios), AGENTS.md — Instrucciones para el agente, Convenciones backend (idioma español, snake_case, prefix, ENUMs), Estructura de carpetas Tecnorenta_Backend (core/models/schemas/repositories/services/routers/dependencies) (+5 more)

### Community 30 - "Tech Stack & Skills Docs"
Cohesion: 0.21
Nodes (13): MySQL local vía DATABASE_URL (.env), Backend stack (Python 3.14+, FastAPI, SQLAlchemy 2.0, Alembic, PyMySQL, Pydantic v2), Frontend stack (React 19 + TypeScript + Vite + Axios + React Router DOM), VITE_API_URL env var, Frontend stack (React 19 + TypeScript + Vite + Axios + React Router DOM + Recharts + Leaflet + Lucide icons), .env.example (DATABASE_URL, SECRET_KEY), fastapi-expert skill, github.com/farmage/opencode-skills (+5 more)

### Community 31 - "Users Module (Frontend)"
Cohesion: 0.27
Nodes (7): Usuario, usuarioApi, UsuarioCreate, UsuarioUpdate, actionsStyle, inputStyle, styles

### Community 32 - "Auth & Dashboard Schemas"
Cohesion: 0.23
Nodes (10): BaseModel, ActivoFotoOut, ForgotPasswordRequest, LoginRequest, RegisterRequest, ResetPasswordRequest, TokenResponse, ActivoReporte (+2 more)

### Community 33 - "Assets Repository"
Cohesion: 0.26
Nodes (3): ActivoRepository, Activo, Session

### Community 34 - "Roles Module (Frontend)"
Cohesion: 0.20
Nodes (8): RolCreate, RolUpdate, FormField(), FormFieldProps, styles, actionsStyle, formStyle, inputStyle

### Community 35 - "Frontend Structure Docs"
Cohesion: 0.22
Nodes (11): Estructura src/ (api, components, context, pages, styles), SIGTAR — Frontend README, /checklist, /login, /mantenimientos, /reportes-incidencia, index.html (Vite entry, root SIGTAR), src/main.tsx entry script (+3 more)

### Community 36 - "Clients Repository"
Cohesion: 0.27
Nodes (3): ClienteRepository, Cliente, Session

### Community 37 - "Payments Repository"
Cohesion: 0.27
Nodes (3): PagoRepository, Pago, Session

### Community 38 - "Users Service (Backend)"
Cohesion: 0.36
Nodes (10): actualizar(), crear(), eliminar(), get_service(), listar(), obtener(), Session, UsuarioCreate (+2 more)

### Community 39 - "Camera Capture Component"
Cohesion: 0.20
Nodes (8): actions, camActions, CameraCaptureProps, container, errorStyle, imgPreview, previewBox, videoStyle

### Community 40 - "Assignments Repository"
Cohesion: 0.29
Nodes (3): AsignacionActivoRepository, AsignacionActivo, Session

### Community 41 - "Categories Repository"
Cohesion: 0.29
Nodes (3): CategoriaActivoRepository, CategoriaActivo, Session

### Community 42 - "Incident Reports Repository"
Cohesion: 0.29
Nodes (3): ReporteIncidenciaRepository, ReporteIncidencia, Session

### Community 43 - "Roles & Permissions Schemas"
Cohesion: 0.33
Nodes (8): PermisoBase, PermisoCreate, PermisoOut, RolAsignarPermiso, RolBase, RolCreate, RolOut, RolUpdate

### Community 44 - "Searchable Select Component"
Cohesion: 0.25
Nodes (6): dropdown, inputStyle, itemStyle, msgStyle, Option, SearchableSelectProps

### Community 45 - "Project State & Sprints Docs"
Cohesion: 0.33
Nodes (6): Endpoints destacados API v1, SIGTAR project state v2.0.0, SIGTAR Sprint2 Informe APA7 (docx), Sprint 3 planeado, SIGTAR Sprint1+2 Presentacion (pptx), tecnorenta_openapi.json

### Community 46 - "Oxlint Config"
Cohesion: 0.33
Nodes (5): plugins, rules, react/only-export-components, react/rules-of-hooks, $schema

### Community 47 - "Alembic Migration Env"
Cohesion: 0.40
Nodes (4): Run migrations in 'offline' mode.      This configures the context with just a, Run migrations in 'online' mode.      In this scenario we need to create an En, run_migrations_offline(), run_migrations_online()

### Community 48 - "Assets Schema"
Cohesion: 0.60
Nodes (4): ActivoBase, ActivoCreate, ActivoOut, ActivoUpdate

### Community 49 - "Assignments Schema"
Cohesion: 0.60
Nodes (4): AsignacionActivoBase, AsignacionActivoCreate, AsignacionActivoOut, AsignacionActivoUpdate

### Community 50 - "Categories Schema"
Cohesion: 0.60
Nodes (4): CategoriaActivoBase, CategoriaActivoCreate, CategoriaActivoOut, CategoriaActivoUpdate

### Community 51 - "Checklist Schema"
Cohesion: 0.60
Nodes (4): ChecklistEstadoBase, ChecklistEstadoCreate, ChecklistEstadoOut, ChecklistEstadoUpdate

### Community 52 - "Clients Schema"
Cohesion: 0.60
Nodes (4): ClienteBase, ClienteCreate, ClienteOut, ClienteUpdate

### Community 53 - "Contracts Schema"
Cohesion: 0.60
Nodes (4): ContratoBase, ContratoCreate, ContratoOut, ContratoUpdate

### Community 54 - "Location History Schema"
Cohesion: 0.60
Nodes (4): HistorialUbicacionBase, HistorialUbicacionCreate, HistorialUbicacionOut, HistorialUbicacionUpdate

### Community 55 - "Maintenance Schema"
Cohesion: 0.60
Nodes (4): MantenimientoBase, MantenimientoCreate, MantenimientoOut, MantenimientoUpdate

### Community 56 - "Payments Schema"
Cohesion: 0.60
Nodes (4): PagoBase, PagoCreate, PagoOut, PagoUpdate

### Community 57 - "Incident Reports Schema"
Cohesion: 0.60
Nodes (4): ReporteIncidenciaBase, ReporteIncidenciaCreate, ReporteIncidenciaOut, ReporteIncidenciaUpdate

### Community 58 - "Users Schema"
Cohesion: 0.60
Nodes (4): UsuarioBase, UsuarioCreate, UsuarioOut, UsuarioUpdate

### Community 59 - "Auth Conventions & Deps"
Cohesion: 0.50
Nodes (4): AuthContext con localStorage + JWT, Convenciones Frontend, bcrypt>=4.2.0, python-jose[cryptography]>=3.3.0

### Community 60 - "Dashboard Endpoints Docs"
Cohesion: 0.50
Nodes (4): /dashboard, GET /api/v1/dashboard/contratos-proximos-vencer, GET /api/v1/dashboard/stats, Módulo Dashboard (7 KPIs, Recharts)

### Community 61 - "Payments Endpoints Docs"
Cohesion: 0.50
Nodes (4): /pagos, GET /api/v1/pagos/proximos, GET /api/v1/pagos/vencidos, Módulo Pagos

### Community 62 - "Placeholder Asset Photos"
Cohesion: 1.00
Nodes (3): Blank Red Placeholder Image (Unreadable Asset Photo), Blank Red Placeholder Image (Unreadable Asset Photo), Blank Red Placeholder Image (Unreadable Asset Photo)

## Knowledge Gaps
- **241 isolated node(s):** `Any`, `AsignacionActivoCreate`, `AsignacionActivoUpdate`, `CategoriaActivoCreate`, `CategoriaActivoUpdate` (+236 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **8 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Usuario` connect `Auth & Security` to `Database Seed Scripts`, `Asset Photos (Backend)`, `Assets Service (Backend)`?**
  _High betweenness centrality (0.102) - this node is a cross-community bridge._
- **Why does `Cliente` connect `Database Seed Scripts` to `Clients Repository`, `Clients Service (Backend)`?**
  _High betweenness centrality (0.060) - this node is a cross-community bridge._
- **Why does `Activo` connect `Database Seed Scripts` to `Asset Photos (Backend)`, `Assets Service (Backend)`, `Categories Service (Backend)`, `Assets Repository`?**
  _High betweenness centrality (0.054) - this node is a cross-community bridge._
- **Are the 35 inferred relationships involving `Activo` (e.g. with `ActivoFotoRepository` and `AsignacionActivoRepository`) actually correct?**
  _`Activo` has 35 INFERRED edges - model-reasoned connections that need verification._
- **Are the 33 inferred relationships involving `Usuario` (e.g. with `ContratoProximoVencer` and `DashboardStats`) actually correct?**
  _`Usuario` has 33 INFERRED edges - model-reasoned connections that need verification._
- **Are the 20 inferred relationships involving `Rol` (e.g. with `ForgotPasswordRequest` and `LoginRequest`) actually correct?**
  _`Rol` has 20 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Run migrations in 'offline' mode.      This configures the context with just a`, `Run migrations in 'online' mode.      In this scenario we need to create an En`, `Any` to the rest of the system?**
  _244 weakly-connected nodes found - possible documentation gaps or missing edges._