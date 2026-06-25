# AGENTS.md — Instrucciones para el agente

## Stack
- Python 3.14+, FastAPI, SQLAlchemy 2.0 (declarative), Alembic, PyMySQL, Pydantic v2
- React 19 + TypeScript + Vite + Axios + React Router DOM

## Arquitectura Backend
- Capas: Router → Service → Repository → Model
- Inyección de dependencias vía `Depends(get_db)`
- Repository solo hace queries; Service tiene la lógica de negocio
- Schemas Pydantic para request/response, separados de modelos

## Convenciones de código
- **Idioma**: español para nombres de tablas, columnas, endpoints (usuarios, activos, contratos)
- **Python**: snake_case, PEP 8
- **API prefix**: `/api/v1/...`
- **Estados fijos**: usar `Enum` de SQLAlchemy, no strings libres
- **Auditoría**: agregar `creado_por`, `fecha_creacion`, `modificado_por`, `fecha_modificacion` en tablas críticas (activos, contratos, asignaciones, reportes)
- **Herencia de modelos**: single table inheritance (ej: Mantenimiento con columna discriminadora `tipo`)
- **Configuración**: pydantic-settings + `.env`

## Convenciones Frontend
- **Componentes**: una carpeta por dominio/feature (usuarios/, contratos/, activos/)
- **API layer**: funciones separadas por recurso en `src/api/`
- **Estado**: hooks personalizados por dominio (`useUsuarios`, `useContratos`)
- **Autenticación**: AuthContext con localStorage + JWT
- **Ruteo**: React Router DOM con Layout anidado

## Base de datos
- MySQL local, configurado en `.env` como `DATABASE_URL`
- Migraciones con Alembic (autogenerate)
- No usar `*.db` (SQLite) — siempre MySQL

## Reglas generales
- No crear documentación tipo README a menos que el usuario lo pida explícitamente
- No agregar comentarios en código a menos que sea necesario para entender lógica compleja
- Seguir el patrón existente del proyecto para nuevos archivos
- AGENTS.md es solo para el agente; no modificarlo sin instrucción explícita
