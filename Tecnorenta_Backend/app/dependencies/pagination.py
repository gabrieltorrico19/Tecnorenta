from fastapi import Query


class PaginationParams:
    """Parámetros de paginación del lado del servidor (page/page_size)."""

    def __init__(
        self,
        page: int = Query(1, ge=1, description="Número de página (1-indexado)"),
        page_size: int = Query(20, ge=1, le=100, description="Registros por página"),
    ):
        self.page = page
        self.page_size = page_size
        self.skip = (page - 1) * page_size
        self.limit = page_size
