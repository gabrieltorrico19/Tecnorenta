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

- `/login` — autenticación
- `/dashboard` — panel con KPIs, alertas de contratos próximos a vencer
- `/activos` — listado, creación, edición con fotos
- `/contratos` — gestión de contratos con documento adjunto
- `/pagos` — control de pagos (vencidos, próximos)
- `/asignaciones` — asignación con checklist y mapa GPS
- `/mantenimientos` — preventivo y correctivo
- `/reportes-incidencia` — reportes con gravedad
- `/usuarios`, `/roles`, `/clientes`, `/categorias`, `/checklist`, `/historial-ubicacion`

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
