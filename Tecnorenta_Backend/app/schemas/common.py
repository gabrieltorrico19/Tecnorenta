import math
from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class Page(BaseModel, Generic[T]):
    """Respuesta paginada estándar para los listados de colección."""

    items: list[T]
    total: int
    page: int
    page_size: int
    pages: int


def paginate(items: list, total: int, page: int, page_size: int) -> dict:
    """Construye el sobre de paginación a partir de los resultados y los parámetros."""
    pages = math.ceil(total / page_size) if page_size else 0
    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
        "pages": pages,
    }
