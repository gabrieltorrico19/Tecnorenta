# Skills de OpenCode para Tecnorenta

## ¿Qué son los Skills?

Los skills son archivos `SKILL.md` que le dan al agente IA instrucciones especializadas para tareas específicas. OpenCode los carga bajo demanda cuando detecta que el contexto coincide con su descripción.

## Skills Instalados

### Backend

| Skill | Ubicación | Propósito |
|-------|-----------|-----------|
| **fastapi-expert** | `~/.config/opencode/skills/fastapi-expert/` | Endpoints REST, Pydantic V2, SQLAlchemy async, JWT, OpenAPI |
| **sql-pro** | `~/.config/opencode/skills/sql-pro/` | Optimización de queries, diseño de schemas, índices, EXPLAIN |
| **security-reviewer** | `~/.config/opencode/skills/security-reviewer/` | Auditoría de seguridad, SAST, vulnerabilidades, reportes |

### Frontend

| Skill | Ubicación | Propósito |
|-------|-----------|-----------|
| **react-expert** | `~/.config/opencode/skills/react-expert/` | Componentes React 19, hooks, TypeScript, Server Components, performance |

### Proyecto

| Skill | Ubicación | Propósito |
|-------|-----------|-----------|
| **tecnorenta** | `~/.config/opencode/skills/tecnorenta/` | Convenciones del proyecto: stack, BD, rutas, estilos, credenciales |

## ¿Cómo se activan?

Los skills se cargan automáticamente cuando el agente detecta palabras clave. Por ejemplo:

- "Crea un endpoint GET para activos" → carga `fastapi-expert`
- "Esta query SQL es lenta" → carga `sql-pro`
- "Revisa la seguridad del login" → carga `security-reviewer`
- "Agrega un botón en el formulario de contratos" → carga `react-expert`
- "Necesito migrar la BD" o "recordá que usamos XAMPP" → carga `tecnorenta`

## Estado del proyecto (v2.0.0)

### Backend
- 11 modelos SQLAlchemy con ENUMs, FKs e índices (usuarios, roles, clientes, activos, categorías, contratos, pagos, asignaciones, reportes, mantenimientos, checklist, historial ubicación, activos_fotos)
- Seed con 6 roles (Administrador, Gerente, Almacén, Técnico, Operador, Cliente), 33 permisos con asignación granular
- Datos de prueba: 10 clientes, 6 categorías jerárquicas, 20 activos, 8 contratos, 18 pagos, 10 asignaciones, 5 reportes
- Auth JWT con bcrypt + require_role middleware, forgot/reset password
- 15 routers CRUD con documentación Swagger automática en /docs (45 endpoints)
- Dashboard service con 6 consultas SQL complejas (GROUP BY, JOIN, SUM, COUNT, subconsultas)
- Fotos de activos con cámara/archivo, documentos adjuntos en contratos
- Geoposicionamiento: latitud/longitud en activos, clientes, asignaciones e historial
- Herencia single-table: Mantenimiento (preventivo + correctivo)
- Auditoría: creado_por, fecha_creacion, modificado_por, fecha_modificacion en tablas críticas
- 4 migraciones Alembic

### Frontend
- 12 módulos CRUD completos: Usuarios, Roles, Clientes, Activos, Categorías, Contratos, Pagos, Asignaciones, Reportes, Mantenimientos, Historial Ubicación, Checklist Estado
- Dashboard gerencial con 7 KPIs, PieChart (activos por estado), BarChart (contratos por estado)
- Mapa Leaflet con marcador arrastrable (MapPicker) en activos, clientes y asignaciones
- Captura de fotos vía cámara (getUserMedia) + upload de archivo
- Exportación de activos a CSV
- Sistema de diseño consistente con variables CSS
- Build limpio: 0 errores TypeScript

### Documentación generada
- `informe/Sprint2/SIGTAR_Sprint2_Informe_APA7.docx` — Informe técnico Sprint 2 en APA 7 (portada, resumen, marco teórico, desarrollo, resultados, scrum, conclusiones, referencias, anexos)
- `informe/Sprint2/SIGTAR_Sprint1_Sprint2_Presentacion.pptx` — Presentación ejecutiva Sprint 1+2 (15 slides con sprint goals visibles)
- `informe/Sprint2/tecnorenta_openapi.json` — Especificación OpenAPI (45 endpoints, importable a Postman)
- `informe/Sprint2/capturas/` — 16 capturas del sistema funcionando (dashboard, CRUDs, swagger, DER, burndown chart)

### Sprint 3 — Planeado
- Dashboard avanzado con filtros por rango de fechas
- 10+ pruebas de integración backend + frontend
- Preparación para despliegue en producción
- Notificaciones de contratos próximos a vencer
- Optimización de consultas SQL

## Referencias técnicas

Cada skill tiene un directorio `references/` con documentación detallada que se carga bajo demanda para no saturar el contexto:

- `fastapi-expert/references/` → pydantic-v2, async-sqlalchemy, authentication, testing-async
- `react-expert/references/` → server-components, react-19-features, state-management, hooks-patterns
- `sql-pro/references/` → query-patterns, window-functions, optimization, database-design
- `security-reviewer/references/` → sast-tools, vulnerability-patterns, secret-scanning, report-template

## Origen

- **fastapi-expert, react-expert, sql-pro, security-reviewer:** de [github.com/farmage/opencode-skills](https://github.com/farmage/opencode-skills) (MIT license)
- **tecnorenta:** skill personalizado creado para el proyecto

## Mantenimiento

Para actualizar los skills de farmage:

```bash
git clone --depth 1 https://github.com/farmage/opencode-skills.git /tmp/opencode-skills
cp -r /tmp/opencode-skills/skills/fastapi-expert ~/.config/opencode/skills/
cp -r /tmp/opencode-skills/skills/react-expert ~/.config/opencode/skills/
cp -r /tmp/opencode-skills/skills/sql-pro ~/.config/opencode/skills/
cp -r /tmp/opencode-skills/skills/security-reviewer ~/.config/opencode/skills/
rm -rf /tmp/opencode-skills
```

Para modificar el skill `tecnorenta`, editar directamente:
`~/.config/opencode/skills/tecnorenta/SKILL.md`
