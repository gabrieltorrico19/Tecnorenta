from pydantic import BaseModel


class DashboardStats(BaseModel):
    usuarios_count: int = 0
    clientes_count: int = 0
    activos_count: int = 0
    activos_por_estado: dict[str, int] = {}
    contratos_count: int = 0
    contratos_por_estado: dict[str, int] = {}
    contratos_proximos_vencer: int = 0
    mantenimientos_pendientes: int = 0
    incidencias_abiertas: int = 0
    pagos_vencidos: int = 0
    total_ingresos_mensuales: float = 0.0


class ActivoReporte(BaseModel):
    id: int
    modelo: str
    codigo_inventario: str
    estado: str
    total_contratos: int = 0
    ingresos_generados: float = 0.0


class ContratoProximoVencer(BaseModel):
    id: int
    cliente: str
    fecha_inicio: str
    fecha_fin: str
    monto_mensual: float
    estado: str
    dias_restantes: int
