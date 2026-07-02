"""seed_usuarios_por_rol

Crea un usuario demo por rol operativo (Gerente, Almacén, Técnico, Operador,
Cliente) para poblar el KPI de usuarios y permitir probar el DSS con distintos
perfiles. Contraseña por defecto: demo1234.

Revision ID: c9e3f4a5b6c7
Revises: b8d2e3f4a5b6
Create Date: 2026-07-01 10:10:00.000000
"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy.orm import Session

import app.seed as seed_auth
from app.models.rol import Rol


# revision identifiers, used by Alembic.
revision: str = 'c9e3f4a5b6c7'
down_revision: Union[str, Sequence[str], None] = 'b8d2e3f4a5b6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

_EMAILS_DEMO = (
    "gerente@tecnorenta.com",
    "almacen@tecnorenta.com",
    "tecnico@tecnorenta.com",
    "operador@tecnorenta.com",
    "cliente@tecnorenta.com",
)


def upgrade() -> None:
    session = Session(bind=op.get_bind())
    roles_ids = {r.nombre: r.id for r in session.query(Rol).all()}
    seed_auth.seed_usuarios_demo(session, roles_ids)
    session.flush()


def downgrade() -> None:
    lista = ", ".join("'{}'".format(e) for e in _EMAILS_DEMO)
    op.execute("DELETE FROM usuarios WHERE email IN ({})".format(lista))
