"""seed_demo_base_data

Siembra el dataset base de demostración necesario para el DSS:
roles/permisos/admin y los datos comerciales (clientes, categorías, activos,
contratos, pagos —incluyendo cuotas vencidas—, asignaciones e incidencias).

Reutiliza las funciones idempotentes de app.seed y app.seed_data, ejecutadas
sobre una sesión ligada a la conexión de la migración (la serialización de
enums queda idéntica a la de la aplicación). No hace commit: Alembic confirma
la transacción al finalizar el upgrade.

Revision ID: a7c1d2e3f4a5
Revises: fea5c70ae009
Create Date: 2026-07-01 10:00:00.000000
"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy.orm import Session

import app.seed as seed_auth
import app.seed_data as seed_demo


# revision identifiers, used by Alembic.
revision: str = 'a7c1d2e3f4a5'
down_revision: Union[str, Sequence[str], None] = 'fea5c70ae009'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    session = Session(bind=op.get_bind())

    # --- roles, permisos y usuario administrador ---
    roles_ids = seed_auth.seed_roles(session)
    seed_auth.seed_permisos(session)
    seed_auth.seed_permisos_asignacion(session, roles_ids)
    seed_auth.seed_admin(session, roles_ids)

    # --- datos comerciales base (idempotentes) ---
    clientes = seed_demo.seed_clientes(session)
    cats = seed_demo.seed_categorias(session)
    activos = seed_demo.seed_activos(session, cats)
    contratos = seed_demo.seed_contratos(session, clientes)
    seed_demo.seed_pagos(session, contratos)          # incluye cuotas 'vencido'
    seed_demo.seed_asignaciones(session, contratos, activos)
    seed_demo.seed_reportes(session, activos)

    session.flush()


def downgrade() -> None:
    # Los seeds de datos base no se revierten automáticamente: eliminar clientes,
    # activos y contratos rompería registros que el usuario pudo haber vinculado
    # (pagos, asignaciones, checklists). Revertir el esquema, si se necesita, se
    # hace con las migraciones estructurales previas.
    pass
