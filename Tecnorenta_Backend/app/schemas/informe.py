"""Schemas del generador de informes del sistema.

Un informe es una vista tabular parametrizable (filtros) con un resumen de
agregados, al estilo de los KPIs del dashboard. Las columnas se describen con
metadatos (`unidad`) para que el frontend formatee moneda/fecha/porcentaje/badge
sin conocer cada informe.
"""
from typing import Any, Literal

from pydantic import BaseModel

Unidad = Literal["texto", "numero", "moneda", "porcentaje", "fecha", "badge"]


class OpcionFiltro(BaseModel):
    value: str
    label: str


class FiltroInforme(BaseModel):
    key: str
    label: str
    tipo: Literal["select", "date"]
    opciones: list[OpcionFiltro] = []


class TipoInformeOut(BaseModel):
    tipo: str
    nombre: str
    descripcion: str
    filtros: list[FiltroInforme] = []


class ResumenItem(BaseModel):
    etiqueta: str
    valor: str | float | int
    unidad: Unidad = "numero"


class ColumnaInforme(BaseModel):
    key: str
    label: str
    unidad: Unidad = "texto"


class InformeOut(BaseModel):
    tipo: str
    titulo: str
    generado: str                                # fecha ISO de generación
    filtros_aplicados: dict[str, str] = {}
    resumen: list[ResumenItem] = []
    columnas: list[ColumnaInforme] = []
    filas: list[dict[str, Any]] = []
    total_filas: int = 0
