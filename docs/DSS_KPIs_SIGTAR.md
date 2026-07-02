# SIGTAR → Sistema de Apoyo a la Toma de Decisiones (DSS)

**Tecnorenta** · Gestión y trazabilidad de activos tecnológicos rentados (laptops).
Este documento cubre los cuatro entregables: (1) **Dossier de KPIs**, (2) **Diseño del DSS**,
(3) **KPIs actuales + nuevos**, (4) **Plan de implementación** y **Verificación**.

> Todos los valores "demo" se calculan sobre el seed determinista
> (`app/seed_data.py` + `app/seed.py`), anclado a `date.today()`. Los importes
> están en **Bs** (bolivianos). Los KPIs sensibles a la fecha (tendencias, edad
> de flota) se recalculan en cada ejecución.

---

## Entregable 1 — Dossier de KPIs

### 1.1 Tabla maestra

Categorías: **F**inanciero · **O**perativo · **R**iesgo · **C**omercial. Semáforo por defecto:
🟢 verde (sano) · 🟡 ámbar (vigilar) · 🔴 rojo (actuar) · 🔵 info (contexto).

| # | KPI | Cat | Fórmula (negocio → datos) | Valor demo | Meta | Umbral (🟢/🟡/🔴) | Semáforo demo | Decisión que apoya |
|---|-----|-----|---------------------------|-----------|------|-------------------|:---:|--------------------|
| 1 | Usuarios | O | `COUNT(usuarios.id)` | **6** | — | info | 🔵 | Dimensiona el equipo con acceso al sistema |
| 2 | Clientes | C | `COUNT(clientes.id)` | **10** | crecer | info | 🔵 | Base comercial instalada |
| 3 | Activos | O | `COUNT(activos.id)` | **20** | — | info | 🔵 | Tamaño de flota |
| 4 | Activos por estado | O | `COUNT(activos) GROUP BY estado` | rentado 11 · disponible 4 · mantenimiento 3 · baja 2 | — | info | 🔵 | Composición de inventario |
| 5 | Contratos | C | `COUNT(contratos.id)` | **8** | — | info | 🔵 | Volumen contractual |
| 6 | Contratos por estado | C | `COUNT(contratos) GROUP BY estado` | activo 6 · vencido 1 · cancelado 1 | — | info | 🔵 | Salud de la cartera contractual |
| 7 | Contratos próximos a vencer | R | `COUNT(contratos WHERE estado=ACTIVO AND fecha_fin ∈ [hoy, hoy+30d])` | **3** | 0 pendientes | 0 / 1-2 / ≥3 | 🔴 | Gatillo de renovación anticipada |
| 8 | Mantenimientos programados (30d) *(corregido)* | O | `COUNT(mantenimientos WHERE proxima_fecha ∈ [hoy, hoy+30d])` | **2** | — | info | 🔵 | Agenda preventiva del técnico |
| 9 | Incidencias abiertas | R | `COUNT(reportes_incidencia WHERE estado ≠ CERRADO)` | **3** (1 grave) | 0 graves | 0 / >0 / grave>0 | 🔴 | Atención técnica prioritaria |
| 10 | Pagos vencidos *(corregido)* | R | `COUNT(pagos WHERE estado=VENCIDO)` | **6** | 0 | 0 / 1-3 / >3 | 🔴 | Gestión de cobranza |
| 11 | Ingresos mensuales (MRR) | F | `SUM(contratos.monto_mensual WHERE estado ∈ {ACTIVO, RENOVADO})` | **Bs 17.800** | ≥ mes anterior | Δ≥0 / Δ∈[-5,0) / Δ<-5% | según tendencia | Foco comercial y de renovación |
| 12 | **Ocupación de flota** | O | `rentados / (total − baja) ×100` = 11/18 | **61,1 %** | 70 % | ≥70 / 55-69 / <55 | 🟡 | Campaña comercial / revisar precios |
| 13 | **MRR / ARR** | F | `MRR = SUM(monto_mensual WHERE estado ∈ {ACTIVO, RENOVADO})`; `ARR = MRR×12` | **Bs 17.800 / Bs 213.600** | crecer | Δ tendencia | según tendencia | Proyección de ingresos |
| 14 | **Tasa de cobro** | F | `pagado / (pagado + vencido) ×100` = 59.000/79.200 | **74,5 %** | 90 % | ≥90 / 75-89 / <75 | 🔴 | Intensificar cobranza |
| 15 | **Cartera vencida (ingreso en riesgo)** | R | `SUM(pagos.monto WHERE estado=VENCIDO)` | **Bs 20.200** (3 contratos) | Bs 0 | 0 / ≤10 % fact. / >10 % | 🔴 | Priorizar cobranza morosos |
| 16 | **Morosidad %** | R | `COUNT(vencido) / COUNT(pagos) ×100` = 6/30 | **20,0 %** | 10 % | ≤10 / 10-20 / >20 | 🟡 | Recordatorios y política de cobro |
| 17 | **Churn de contratos** | C | `cancelados / total ×100` = 1/8 | **12,5 %** | 10 % | ≤10 / 10-15 / >15 | 🟡 | Plan de retención |
| 18 | **Costo de mantenimiento total** | O | `SUM(mantenimientos.costo)` | **Bs 2.760** | — | info | 🔵 | Presupuesto de soporte |
| 19 | **Costo por activo** | O | `costo_total / COUNT(activos)` = 2.760/20 | **Bs 138** | — | info | 🔵 | Costo unitario de sostener flota |
| 20 | **Split correctivo vs. preventivo** | O | `costo_correctivo / costo_total ×100` = 1.850/2.760 | **67 %** (correctivo) | ≤40 % | ≤40 / 40-60 / >60 | 🔴 | Reforzar plan preventivo |
| 21 | **Ingreso en riesgo por vencimientos** | R | `SUM(monto_mensual) de contratos próximos a vencer` | **Bs 9.700** | Bs 0 | 0 / ≤20 % MRR / >20 % | 🔴 | Contactar para renovación |
| 22 | **Revenue per asset (utilización)** | C | Por activo: `COUNT(DISTINCT contratos)` y `SUM(monto_mensual de contratos distintos)` vía `asignaciones_activo` | Top: **LPT-GAM-001** Bs 7.500 (2 contratos) | — | info | 🔵 | Priorizar reposición de equipos rentables |
| 23 | **Valor depreciado de flota** | F | `SUM(activos.valor_depreciado WHERE estado≠BAJA)` | **Bs 28.170** | — | info | 🔵 | Base para renovación/reposición |
| 24 | **Edad promedio de flota** | O | `AVG(hoy − fecha_compra)` en años (operativos) | **≈ 3,0 años** *(runtime)* | ≤3 años | ≤3 / 3-4 / >4 | según runtime | Planificar reposición |

**Umbral de referencia**: "≤10 % fact." = cartera vencida menor al 10 % de lo facturado; "≤20 % MRR" = ingreso en riesgo menor al 20 % del MRR.

### 1.2 Fichas ampliadas (KPIs críticos)

#### 🟡 Ocupación de flota — 61,1 % (meta 70 %)
- **Fórmula**: `activos_rentados / activos_operativos`, donde `operativos = total − baja`. Datos: `activos.estado` (RENTADO / DISPONIBLE / MANTENIMIENTO / BAJA). Demo: 11 / (20 − 2) = 11/18 = **61,1 %**.
- **Interpretación**: 7 equipos operativos no están generando ingreso. Sano ≥70 %; por debajo hay capacidad ociosa que igual se deprecia.
- **Decisión**: 🟡 → *activar campaña comercial* sobre los 4 disponibles y/o *revisar precios*. Regla del panel: `ocupacion < 70 → recomendación media`.

#### 🔴 Tasa de cobro — 74,5 % (meta 90 %)
- **Fórmula**: `monto_pagado / (monto_pagado + monto_vencido)`. Se excluyen las cuotas **pendientes aún no vencidas** para no castigar artificialmente el indicador. Datos: `pagos.monto`, `pagos.estado`. Demo: 59.000 / (59.000 + 20.200) = **74,5 %**.
- **Interpretación**: de cada Bs 100 exigibles se cobran ~74. Bajo la meta de 90 %.
- **Decisión**: 🔴 → gestión de cobranza inmediata; ver ficha de cartera vencida.

#### 🔴 Cartera vencida / Ingreso en riesgo — Bs 20.200
- **Fórmula**: `SUM(pagos.monto WHERE estado=VENCIDO)`; `contratos morosos = COUNT(DISTINCT pagos.id_contrato WHERE estado=VENCIDO)`. Demo: **Bs 20.200** en **3 contratos** (incluye el contrato expirado de Bs 5.500 con saldo).
- **Interpretación**: ingreso ya facturado y no cobrado = riesgo directo de caja. Sano = 0; ámbar si <10 % de lo facturado; rojo por encima (aquí 20 % de Bs 99.000).
- **Decisión**: 🔴 → *"Gestionar cobranza: Bs 20.200 en 3 contratos"*. Ruta sugerida `/pagos`.

#### 🔴 Ingreso en riesgo por vencimientos — Bs 9.700
- **Fórmula**: `SUM(contratos.monto_mensual)` de los contratos activos que vencen en ≤30 días. Demo: 4.000 + 2.500 + 3.200 = **Bs 9.700** en 3 contratos (≈54 % del MRR).
- **Decisión**: 🔴 → *"3 contratos vencen en 30 días (MRR en riesgo Bs 9.700) → contactar para renovación"*. Ruta `/contratos`.

#### 🔴 Split correctivo vs. preventivo — 67 % correctivo
- **Fórmula**: `costo_correctivo / costo_total`. Datos: `mantenimientos.tipo`, `mantenimientos.costo`. Demo: 1.850 / 2.760 = **67 %** (preventivo Bs 910, correctivo Bs 1.850).
- **Interpretación**: predominio de mantenimiento reactivo = flota gestionada "apagando incendios". Sano ≤40 %.
- **Decisión**: 🔴 → *"Reforzar plan preventivo"*. Regla: `costo_correctivo > costo_preventivo → recomendación media`.

#### 🟡 Churn de contratos — 12,5 % (meta 10 %)
- **Fórmula**: `contratos_cancelados / contratos_total`. Demo: 1/8 = **12,5 %**.
- **Decisión**: 🟡 → analizar causa de la cancelación y activar retención.

#### MRR / ARR + tendencia
- **Fórmula**: `MRR = SUM(monto_mensual WHERE estado ∈ {ACTIVO, RENOVADO})` = **Bs 17.800**; `ARR = MRR×12` = **Bs 213.600**. La **tendencia** se reconstruye mes a mes desde la vigencia de los contratos (`fecha_inicio..fecha_fin` que solapan cada mes, misma definición de estado que el MRR actual) en `/dashboard/tendencias`.
- **Decisión**: si `Δ MRR < 0` respecto al mes previo → revisar renovaciones y nuevas altas.

---

## Entregable 2 — Diseño del DSS ("rundown" de negocio)

Al abrir el panel, el gerente obtiene en ~10 s: **cómo va el negocio (arriba)**, **dónde están los riesgos (medio)** y **qué hacer hoy (abajo)**.

### Wireframe textual

```
┌───────────────────────────────────────────────────────────────────────────┐
│ Panel de decisión                                   Actualizado: 1 jul 2026 │
│ ⚠ 3 contratos vencen en 30 días · Ingreso en riesgo Bs 9.700  [Ver contratos]│
├───────────────────────────────────────────────────────────────────────────┤
│ FRANJA 1 · SALUD DEL NEGOCIO  (indicadores financieros/estratégicos)        │
│ ┌─────────┐┌─────────┐┌─────────┐┌─────────┐┌─────────┐┌─────────┐          │
│ │ MRR     ││Ocupación││Tasa     ││Cartera  ││Ingreso  ││Churn    │          │
│ │17.800 ▲ ││ 61,1% 🟡││cobro🔴  ││vencida🔴││riesgo🔴 ││12,5% 🟡 │          │
│ │Meta:ant.││Meta:70% ││74,5%    ││20.200   ││9.700    ││Meta:10% │          │
│ └─────────┘└─────────┘└─────────┘└─────────┘└─────────┘└─────────┘          │
├───────────────────────────────────────────────────────────────────────────┤
│ FRANJA 2 · OPERACIÓN Y RIESGOS                                              │
│ [Morosidad 20%🟡][Correctivo 67%🔴][Incid. abiertas 3🔴][Mant.prog. 2][Edad]│
│ ┌── MRR vs Cobrado (línea 6m) ──┐┌ Activos x estado (pie) ┐┌ Contratos (bar)┐│
│ ┌── Pagos x estado (pie) ───────┐┌ Incidencias x gravedad ┐┌ Mant. costo pie┐│
├───────────────────────────────────────────────────────────────────────────┤
│ FRANJA 3 · DECISIONES RECOMENDADAS  (generadas por reglas sobre los KPIs)   │
│ 🔴 ALTA  Cartera vencida Bs 20.200 → gestionar cobranza      [Actuar →/pagos]│
│ 🔴 ALTA  1 incidencia grave abierta → técnico inmediato    [Actuar →/reportes]│
│ 🔴 ALTA  3 contratos vencen (Bs 9.700) → renovar         [Actuar →/contratos]│
│ 🟡 MEDIA Ocupación 61,1% < 70% → campaña/precios          [Actuar →/activos]│
│ 🟡 MEDIA Correctivo>preventivo → reforzar preventivo [Actuar →/mantenimientos]│
│ 🟡 MEDIA Churn 12,5% > 10% → plan de retención          [Actuar →/contratos]│
│ 🔵 BAJA  2 preventivos por ejecutar (30d) → agendar  [Actuar →/mantenimientos]│
└───────────────────────────────────────────────────────────────────────────┘
```

### Reglas del motor de recomendaciones (`DashboardService.get_recomendaciones`)

| Regla | Condición | Severidad | Acción | Ruta |
|-------|-----------|-----------|--------|------|
| Incidencias graves | `incidencias_graves_abiertas > 0` | alta | Asignar técnico / abrir correctivo | `/reportes` |
| Cartera vencida | `cartera_vencida > 0` | alta | Gestionar cobranza de morosos | `/pagos` |
| Vencimientos | `contratos_proximos_vencer > 0` | alta si `ingreso_riesgo > 15% MRR`, si no media | Contactar para renovación | `/contratos` |
| Ocupación | `ocupacion_flota < 70` | media | Campaña comercial / revisar precios | `/activos` |
| Preventivo | `costo_correctivo > costo_preventivo` | media | Reforzar plan preventivo | `/mantenimientos` |
| Churn | `churn_pct > 10` | media | Plan de retención | `/contratos` |
| Preventivos programados | `mantenimientos_pendientes > 0` | baja | Agendar técnico | `/mantenimientos` |
| Sin alertas | (ninguna anterior) | baja | Mantener seguimiento | `/` |

Las recomendaciones se ordenan por severidad (alta → media → baja).

---

## Entregable 3 — KPIs actuales (fórmulas reales + correcciones)

Los 11 KPIs de `DashboardStats` original se conservan (retrocompatibilidad). Correcciones aplicadas:

1. **`mantenimientos_pendientes`** — *antes* `COUNT(fecha ≥ hoy)` (contaba cualquier mantenimiento futuro y daba **0** porque no se sembraban mantenimientos). *Ahora* mide **preventivos accionables**: `COUNT(proxima_fecha ∈ [hoy, hoy+30d])` → demo **2**.
2. **`pagos_vencidos`** — *antes* **0** porque `seed_pagos` solo generaba `pagado`/`pendiente`. *Ahora* el seed genera cuotas `VENCIDO` → demo **6**.
3. **`total_ingresos_mensuales`** — definición como ingreso recurrente en vigor: `SUM(monto_mensual WHERE estado ∈ {ACTIVO, RENOVADO})` = **17.800** (sin contratos renovados en demo). Se usa la MISMA definición en la serie de tendencias para que el MRR actual coincida con el último punto del gráfico. Se expone además como `mrr` y se añade `arr`.

---

## Entregable 3b — KPIs nuevos de decisión

Añadidos a `DashboardStats` y expuestos como fichas en `/dashboard/kpis`:
`ocupacion_flota`, `activos_operativos`, `activos_rentados`, `mrr`, `arr`,
`ingreso_en_riesgo_vencimientos`, `monto_facturado`, `monto_pagado`, `cartera_vencida`,
`monto_pendiente`, `tasa_cobro`, `morosidad_pct`, `pagos_totales`,
`contratos_con_cartera_vencida`, `pagos_por_estado`, `contratos_cancelados`, `churn_pct`,
`costo_mantenimiento_total/preventivo/correctivo/por_activo`, `mantenimientos_preventivos/correctivos`,
`mantenimientos_por_tipo`, `incidencias_por_gravedad`, `incidencias_graves_abiertas`,
`valor_flota_depreciado`, `edad_promedio_flota_anios`. Revenue-per-asset vive en `/dashboard/activos-reporte`
(schema `ActivoReporte` reutilizado). Tendencias en `/dashboard/tendencias`.

---

## Entregable 4 — Plan / mapa de implementación por archivo

### Backend (patrón Router → Service → Repository, Pydantic v2)

| Archivo | Cambio |
|---------|--------|
| `app/schemas/dashboard.py` | `DashboardStats` extendido + nuevos modelos: `KpiCard`, `KpisResponse`, `Recomendacion`, `PuntoTendencia`, `TendenciasResponse`. `ActivoReporte`/`ContratoProximoVencer` conservados. |
| `app/repositories/dashboard.py` **(nuevo)** | Capa de agregaciones (solo lectura): flota, contratos, pagos, mantenimiento, incidencias, MRR mes a mes, cobrado mes a mes, revenue-per-asset. |
| `app/services/dashboard.py` | Orquesta KPIs con semáforo/meta/tendencia (`get_kpis`), reglas de recomendación (`get_recomendaciones`), tendencias (`get_tendencias`), `get_stats` extendido, `get_activos_reporte`, `get_contratos_proximos_vencer`. |
| `app/routers/dashboard.py` | Nuevos endpoints: `/kpis`, `/recomendaciones`, `/tendencias`, `/activos-reporte` (+ `/stats` y `/contratos-proximos-vencer`). |

### Datos demo — seeders (idempotentes/deterministas) + migraciones Alembic

| Archivo | Cambio |
|---------|--------|
| `app/seed_data.py` | Reescrito determinista y anclado a `date.today()`: distribución fija de activos, contratos con vencimientos relativos, **cuotas `VENCIDO`**, `seed_mantenimientos` (preventivos + correctivos ligados a incidencias), `run(db)` reutilizable. |
| `app/seed.py` | `seed_usuarios_demo` (1 usuario por rol) + `run(db)`. |
| `alembic/versions/a7c1d2e3f4a5_seed_demo_base_data.py` **(nuevo)** | Siembra base (roles/permisos/admin + comercial, incluye pagos vencidos) vía `Session(bind=op.get_bind())`. `down_revision = fea5c70ae009`. |
| `alembic/versions/b8d2e3f4a5b6_seed_mantenimientos.py` **(nuevo)** | Siembra mantenimientos. Downgrade borra filas etiquetadas `[demo]`. |
| `alembic/versions/c9e3f4a5b6c7_seed_usuarios_por_rol.py` **(nuevo)** | Usuarios demo. Downgrade borra por email. Head de la cadena. |

> Las migraciones **llaman a las funciones del seed** (fuente única de verdad), ejecutadas sobre la conexión de la migración → la serialización de enums es idéntica a la de la app y `alembic upgrade head` deja la BD lista para el DSS sin ejecutar los seeders por separado.

### Frontend (React 19 + Recharts, reutilizando Card/Badge/Button)

| Archivo | Cambio |
|---------|--------|
| `src/utils/helpers.ts` | `formatCurrency` (Bs), `formatNumber`, `formatPercent`, `formatDelta` (+ `formatDate` existente). |
| `src/api/endpoints.ts` | Endpoints `KPIS`, `RECOMENDACIONES`, `TENDENCIAS`, `ACTIVOS_REPORTE`. |
| `src/api/dashboard.api.ts` | Tipos e interfaces + métodos `kpis/recomendaciones/tendencias/activosReporte`; `DashboardStats` extendido. |
| `src/components/dashboard/KpiTile.tsx` **(nuevo)** | Tarjeta KPI: número + meta + delta de tendencia + color de semáforo (usa `Badge`/helpers). |
| `src/pages/Dashboard.tsx` | Rediseño en 3 franjas (salud / operación-riesgos / recomendaciones) + gráficos Recharts (línea MRR, pies, barras). |

---

## Verificación

### Ejecutada en esta entrega
- **Backend — sintaxis**: `python -m py_compile` sobre los 6 archivos backend + 3 migraciones → **OK**.
- **Backend — enums**: prueba aislada (SQLite en memoria) confirma que SQLAlchemy persiste el **nombre** del enum y que filtrar por value-string o miembro funciona → base de las migraciones/consultas.
- **Frontend — build**: `npm run build` (`tsc -b && vite build`) → **OK** (sin errores de tipos; solo aviso pre-existente de tamaño de chunk).
- **Revisión adversarial** multi-dimensión (agregaciones, migraciones, seed, frontend, regresión) con verificación independiente de cada hallazgo.

### Pendiente en el entorno del usuario (requiere MySQL; no ejecutable aquí)
```bash
# Backend
cd Tecnorenta_Backend
alembic upgrade head          # crea esquema + siembra datos demo del DSS
uvicorn app.main:app --reload
# GET /api/v1/dashboard/stats | /kpis | /recomendaciones | /tendencias | /activos-reporte
# Frontend
cd Tecnorenta_Frontend && npm run dev   # abrir el Panel de decisión
```

### Mapa criterio de evaluación → dónde se cumple

| Criterio del enunciado | Dónde se cumple |
|------------------------|-----------------|
| Ficha por KPI (nombre+cat, fórmula negocio+datos, valor demo, interpretación, decisión) | Dossier §1.1 (tabla) + §1.2 (fichas) |
| Semáforo con umbral por KPI | §1.1 columnas Umbral/Semáforo; backend `_semaforo` |
| Tendencia vs. período anterior | KPI MRR (`tendencia_pct`) + `/dashboard/tendencias` + gráfico de línea |
| Diseño DSS en 3 franjas | Entregable 2 (wireframe) + `Dashboard.tsx` |
| Recomendaciones automáticas por reglas | Entregable 2 (tabla de reglas) + `get_recomendaciones` + Franja 3 |
| Documentar 11 KPIs actuales con fórmulas reales | Entregable 3 |
| Corregir KPIs mal definidos | `mantenimientos_pendientes` y `pagos_vencidos` (Entregable 3) |
| KPIs nuevos (ocupación, MRR/ARR, cobro, cartera, morosidad, churn, mant., revenue/asset, riesgo, depreciación) | Entregable 3b + tabla §1.1 (#12-24) |
| Backend: ampliar Stats + nuevos endpoints, valor/meta/semáforo/tendencia | `schemas/services/repositories/routers` dashboard |
| Frontend: rediseño reutilizando Card/Badge/Button/Recharts + moneda/fecha | `Dashboard.tsx`, `KpiTile.tsx`, `helpers.ts` |
| Seed demo corregido (vencidos, mantenimientos, usuarios), idempotente | `seed_data.py`, `seed.py` |
| Un Alembic por seeder, flujo normal, listo para correr | 3 migraciones en `alembic/versions/` |
| No romper módulos/paginación, UI en español | `/stats` retrocompatible; sin tocar otros routers/listas; UI en español |
