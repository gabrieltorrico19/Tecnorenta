from datetime import date
from typing import Optional

from sqlalchemy import text
from sqlalchemy.orm import Session


class ReportesService:
    def __init__(self, db: Session):
        self.db = db

    def top_activos_rentados(self, fecha_inicio: date, fecha_fin: date, limit: int = 10) -> list[dict]:
        """Top activos más rentados en un rango de fechas, con ingresos generados."""
        sql = text("""
            SELECT
                a.id,
                a.codigo_inventario,
                a.modelo,
                COUNT(aa.id)          AS total_asignaciones,
                SUM(c.monto_mensual)  AS ingreso_total
            FROM activos a
            JOIN asignaciones_activo aa ON aa.id_activo = a.id
            JOIN contratos c            ON c.id = aa.id_contrato
            WHERE aa.fecha_asignacion BETWEEN :fi AND :ff
            GROUP BY a.id, a.codigo_inventario, a.modelo
            ORDER BY ingreso_total DESC
            LIMIT :lim
        """)
        rows = self.db.execute(sql, {"fi": fecha_inicio, "ff": fecha_fin, "lim": limit}).mappings().all()
        return [dict(r) for r in rows]

    def activos_bajo_stock_disponible(self, umbral: int = 5) -> list[dict]:
        """Activos disponibles cuyo conteo total de unidades del mismo modelo es menor al umbral."""
        sql = text("""
            SELECT
                a.modelo,
                ca.nombre                         AS categoria,
                COUNT(a.id)                       AS unidades_disponibles,
                SUM(CASE WHEN aa.fecha_devolucion IS NULL AND aa.id IS NOT NULL THEN 1 ELSE 0 END) AS unidades_rentadas
            FROM activos a
            LEFT JOIN categorias_activo ca ON ca.id = a.id_categoria
            LEFT JOIN asignaciones_activo aa ON aa.id_activo = a.id AND aa.fecha_devolucion IS NULL
            WHERE a.estado != 'baja'
            GROUP BY a.modelo, ca.nombre
            HAVING COUNT(CASE WHEN a.estado = 'disponible' THEN 1 END) < :umbral
            ORDER BY unidades_disponibles ASC
        """)
        rows = self.db.execute(sql, {"umbral": umbral}).mappings().all()
        return [dict(r) for r in rows]

    def resumen_pagos_por_estado(self, fecha_inicio: Optional[date] = None, fecha_fin: Optional[date] = None) -> list[dict]:
        """Totales de pagos agrupados por estado (pendiente/pagado/vencido)."""
        filtro = ""
        params: dict = {}
        if fecha_inicio and fecha_fin:
            filtro = "WHERE p.fecha BETWEEN :fi AND :ff"
            params = {"fi": fecha_inicio, "ff": fecha_fin}

        sql = text(f"""
            SELECT
                p.estado,
                COUNT(p.id)   AS cantidad,
                SUM(p.monto)  AS total_monto
            FROM pagos p
            {filtro}
            GROUP BY p.estado
            ORDER BY total_monto DESC
        """)
        rows = self.db.execute(sql, params).mappings().all()
        return [dict(r) for r in rows]

    def contratos_proximos_a_vencer(self, dias: int = 30) -> list[dict]:
        """Contratos activos que vencen dentro de los próximos N días."""
        sql = text("""
            SELECT
                c.id,
                cl.razon_social  AS cliente,
                cl.nit,
                c.fecha_fin,
                c.monto_mensual,
                DATEDIFF(c.fecha_fin, CURDATE()) AS dias_restantes
            FROM contratos c
            JOIN clientes cl ON cl.id = c.id_cliente
            WHERE c.estado = 'activo'
              AND c.fecha_fin BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL :dias DAY)
            ORDER BY c.fecha_fin ASC
        """)
        rows = self.db.execute(sql, {"dias": dias}).mappings().all()
        return [dict(r) for r in rows]

    def incidencias_por_gravedad(self) -> list[dict]:
        """Conteo de incidencias abiertas y en atención agrupadas por gravedad."""
        sql = text("""
            SELECT
                ri.gravedad,
                COUNT(ri.id)  AS total,
                SUM(CASE WHEN ri.estado = 'en_atencion' THEN 1 ELSE 0 END) AS en_atencion
            FROM reportes_incidencia ri
            WHERE ri.estado != 'cerrado'
            GROUP BY ri.gravedad
            ORDER BY FIELD(ri.gravedad, 'grave', 'moderado', 'leve')
        """)
        rows = self.db.execute(sql).mappings().all()
        return [dict(r) for r in rows]

    def costo_mantenimientos_por_mes(self) -> list[dict]:
        """Costo total de mantenimientos agrupado por año/mes."""
        sql = text("""
            SELECT
                YEAR(m.fecha)  AS anio,
                MONTH(m.fecha) AS mes,
                m.tipo,
                COUNT(m.id)    AS cantidad,
                SUM(m.costo)   AS costo_total
            FROM mantenimientos m
            GROUP BY anio, mes, m.tipo
            ORDER BY anio DESC, mes DESC
        """)
        rows = self.db.execute(sql).mappings().all()
        return [dict(r) for r in rows]
