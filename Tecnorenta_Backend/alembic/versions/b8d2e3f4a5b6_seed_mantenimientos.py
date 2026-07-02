"""seed_mantenimientos

Siembra mantenimientos preventivos y correctivos (con costo) para alimentar
los KPIs de costo de mantenimiento, split preventivo/correctivo y
mantenimientos programados. Los correctivos se ligan a incidencias
graves/moderadas existentes.

Revision ID: b8d2e3f4a5b6
Revises: a7c1d2e3f4a5
Create Date: 2026-07-01 10:05:00.000000
"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy.orm import Session

import app.seed_data as seed_demo
from app.models.activo import Activo
from app.models.reporte_incidencia import ReporteIncidencia


# revision identifiers, used by Alembic.
revision: str = 'b8d2e3f4a5b6'
down_revision: Union[str, Sequence[str], None] = 'a7c1d2e3f4a5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    session = Session(bind=op.get_bind())
    activos = session.query(Activo).order_by(Activo.id).all()
    reportes = session.query(ReporteIncidencia).order_by(ReporteIncidencia.id).all()
    seed_demo.seed_mantenimientos(session, activos, reportes)
    session.flush()


def downgrade() -> None:
    # Elimina únicamente los mantenimientos sembrados por el demo (etiquetados).
    op.execute(
        "DELETE FROM mantenimientos WHERE descripcion LIKE '{}%'".format(seed_demo.SEED_TAG)
    )
