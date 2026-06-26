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

## Estado del proyecto (v1.1.0)

### Backend
- 14 modelos SQLAlchemy con ENUMs, FKs e índices
- Seed con 6 roles (Administrador, Gerente, Almacén, Técnico, Operador, Cliente), 30 permisos con asignación granular
- Datos de prueba: 10 clientes, 6 categorías, 20 activos, 8 contratos
- Auth JWT con bcrypt + require_role middleware
- 13 routers CRUD completos (auto-documentados en Swagger /docs)
- Activo model con `latitud`/`longitud` para geolocalización

### Frontend
- 11 módulos CRUD completos (Lista + Formulario vía DataTable + FormField)
- Dashboard con bento-grid, PieChart (activos por estado), BarChart (contratos por estado)
- Mapa Leaflet con marcador arrastrable (MapPicker) en formulario de activos
- Sistema de diseño: variables de espaciado, tipografía, font-weight y line-height
- Tema oscuro consistente vía CSS variables
- Build limpio: 0 errores TypeScript, 560+ módulos

### Librerías agregadas
- `react-leaflet` + `leaflet` → mapas OpenStreetMap gratuitos
- `recharts` → gráficas reactivas

### Pendiente
- Sidebar responsive para tablets/móviles
- Carga con skeleton en DataTable
- Toast/notificaciones para operaciones CRUD

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
