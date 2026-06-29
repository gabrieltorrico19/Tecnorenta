# SIGTAR — Frontend

Interfaz de usuario del Sistema de Gestión y Trazabilidad de Activos Rentados.

## Stack

React 19 + TypeScript + Vite + Axios + React Router DOM + Recharts + Leaflet + Lucide icons

## Estructura

```
src/
├── api/          # Capa de comunicación con backend (axios + endpoints)
├── components/   # Componentes reutilizables (DataTable, Button, Card, etc.)
├── context/      # Contextos (AuthContext, ToastContext)
├── pages/        # Páginas por dominio (activos, contratos, dashboard, etc.)
└── styles/       # Estilos globales
```

## Rutas principales

- `/login` — autenticación JWT
- `/dashboard` — panel con 7 KPIs, gráficos Recharts (barras + pastel), alertas de contratos próximos a vencer
- `/activos` — listado, creación, edición con fotos (cámara/archivo), mapa GPS, exportación CSV
- `/contratos` — gestión de contratos con documento adjunto
- `/pagos` — control de pagos (vencidos, próximos), por contrato
- `/asignaciones` — vinculación activo ↔ contrato con mapa GPS
- `/mantenimientos` — preventivo programado y correctivo
- `/reportes-incidencia` — reportes con gravedad (leve/moderado/grave)
- `/checklist` — evaluación de componentes en entrega/devolución
- `/historial-ubicacion` — trazabilidad GPS por asignación
- `/usuarios`, `/roles`, `/clientes`, `/categorias`

## Cómo ejecutar

```bash
cd Tecnorenta_Frontend
npm install
npm run dev     # desarrollo en localhost:5173
npm run build   # producción
```

## Variables de entorno

Copiar `.env.example` a `.env`:

```
VITE_API_URL=http://localhost:8000/api/v1
```

## Documentación

Ver `informe/Sprint2/` para informes, presentación y capturas del sistema.
