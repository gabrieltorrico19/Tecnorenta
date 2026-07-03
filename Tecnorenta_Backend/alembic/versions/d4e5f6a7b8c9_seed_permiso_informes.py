"""seed_permiso_informes

Registra el permiso `informes.ver` (generador de informes del sistema) y lo
asigna a los roles Gerente y Operador (el Administrador recibe todos los
permisos automáticamente). Idempotente: reutiliza los seeders de app.seed.

Revision ID: d4e5f6a7b8c9
Revises: c9e3f4a5b6c7
Create Date: 2026-07-02 19:30:00.000000
"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy.orm import Session

import app.seed as seed_auth


# revision identifiers, used by Alembic.
revision: str = 'd4e5f6a7b8c9'
down_revision: Union[str, Sequence[str], None] = 'c9e3f4a5b6c7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    session = Session(bind=op.get_bind())
    roles_ids = seed_auth.seed_roles(session)
    seed_auth.seed_permisos(session)
    session.flush()
    seed_auth.seed_permisos_asignacion(session, roles_ids)
    session.flush()


def downgrade() -> None:
    op.execute(
        "DELETE FROM roles_permisos WHERE id_permiso IN "
        "(SELECT id FROM permisos WHERE nombre = 'informes.ver')"
    )
    op.execute("DELETE FROM permisos WHERE nombre = 'informes.ver'")
