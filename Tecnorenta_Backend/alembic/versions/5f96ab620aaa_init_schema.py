"""init_schema

Revision ID: 5f96ab620aaa
Revises: 
Create Date: 2026-06-24 21:23:27.384125

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5f96ab620aaa'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('categorias_activo',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nombre', sa.String(length=100), nullable=False),
        sa.Column('nivel', sa.String(length=50), nullable=True),
        sa.Column('descripcion', sa.String(length=255), nullable=True),
        sa.Column('id_categoria_padre', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_categorias_activo_id'), 'categorias_activo', ['id'], unique=False)
    op.create_foreign_key('fk_categoria_padre', 'categorias_activo',
                          'categorias_activo', ['id_categoria_padre'], ['id'])

    op.create_table('clientes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('razon_social', sa.String(length=150), nullable=False),
        sa.Column('nit', sa.String(length=50), nullable=False),
        sa.Column('direccion', sa.String(length=255), nullable=True),
        sa.Column('latitud', sa.Float(), nullable=True),
        sa.Column('longitud', sa.Float(), nullable=True),
        sa.Column('sector', sa.String(length=100), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_clientes_id'), 'clientes', ['id'], unique=False)
    op.create_index(op.f('ix_clientes_nit'), 'clientes', ['nit'], unique=True)

    op.create_table('permisos',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nombre', sa.String(length=100), nullable=False),
        sa.Column('descripcion', sa.String(length=255), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('nombre')
    )
    op.create_index(op.f('ix_permisos_id'), 'permisos', ['id'], unique=False)

    op.create_table('roles',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nombre', sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('nombre')
    )
    op.create_index(op.f('ix_roles_id'), 'roles', ['id'], unique=False)

    op.create_table('roles_permisos',
        sa.Column('id_rol', sa.Integer(), nullable=False),
        sa.Column('id_permiso', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['id_permiso'], ['permisos.id'], ),
        sa.ForeignKeyConstraint(['id_rol'], ['roles.id'], ),
        sa.PrimaryKeyConstraint('id_rol', 'id_permiso')
    )

    op.create_table('usuarios',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nombre', sa.String(length=100), nullable=False),
        sa.Column('email', sa.String(length=150), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('telefono', sa.String(length=20), nullable=True),
        sa.Column('activo', sa.Boolean(), nullable=True),
        sa.Column('id_rol', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.ForeignKeyConstraint(['id_rol'], ['roles.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_usuarios_email'), 'usuarios', ['email'], unique=True)
    op.create_index(op.f('ix_usuarios_id'), 'usuarios', ['id'], unique=False)

    op.create_table('activos',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('codigo_inventario', sa.String(length=50), nullable=False),
        sa.Column('modelo', sa.String(length=100), nullable=False),
        sa.Column('numero_serie', sa.String(length=100), nullable=False),
        sa.Column('estado', sa.Enum('DISPONIBLE', 'RENTADO', 'MANTENIMIENTO', 'BAJA', name='estadoactivo'), nullable=False),
        sa.Column('fecha_compra', sa.Date(), nullable=True),
        sa.Column('valor_depreciado', sa.Float(), nullable=True),
        sa.Column('id_categoria', sa.Integer(), nullable=True),
        sa.Column('creado_por', sa.Integer(), nullable=True),
        sa.Column('fecha_creacion', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.Column('modificado_por', sa.Integer(), nullable=True),
        sa.Column('fecha_modificacion', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.ForeignKeyConstraint(['creado_por'], ['usuarios.id'], ),
        sa.ForeignKeyConstraint(['id_categoria'], ['categorias_activo.id'], ),
        sa.ForeignKeyConstraint(['modificado_por'], ['usuarios.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('numero_serie')
    )
    op.create_index(op.f('ix_activos_codigo_inventario'), 'activos', ['codigo_inventario'], unique=True)
    op.create_index(op.f('ix_activos_id'), 'activos', ['id'], unique=False)

    op.create_table('contratos',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('fecha_inicio', sa.Date(), nullable=False),
        sa.Column('fecha_fin', sa.Date(), nullable=False),
        sa.Column('condiciones_uso', sa.String(length=500), nullable=True),
        sa.Column('estado', sa.Enum('ACTIVO', 'VENCIDO', 'CANCELADO', 'RENOVADO', name='estadocontrato'), nullable=False),
        sa.Column('monto_mensual', sa.Float(), nullable=False),
        sa.Column('id_cliente', sa.Integer(), nullable=False),
        sa.Column('creado_por', sa.Integer(), nullable=True),
        sa.Column('fecha_creacion', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.Column('modificado_por', sa.Integer(), nullable=True),
        sa.Column('fecha_modificacion', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.ForeignKeyConstraint(['creado_por'], ['usuarios.id'], ),
        sa.ForeignKeyConstraint(['id_cliente'], ['clientes.id'], ),
        sa.ForeignKeyConstraint(['modificado_por'], ['usuarios.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_contratos_id'), 'contratos', ['id'], unique=False)

    op.create_table('asignaciones_activo',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('fecha_asignacion', sa.Date(), nullable=False),
        sa.Column('fecha_devolucion', sa.Date(), nullable=True),
        sa.Column('latitud', sa.Float(), nullable=True),
        sa.Column('longitud', sa.Float(), nullable=True),
        sa.Column('id_contrato', sa.Integer(), nullable=False),
        sa.Column('id_activo', sa.Integer(), nullable=False),
        sa.Column('creado_por', sa.Integer(), nullable=True),
        sa.Column('fecha_creacion', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.Column('modificado_por', sa.Integer(), nullable=True),
        sa.Column('fecha_modificacion', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.ForeignKeyConstraint(['creado_por'], ['usuarios.id'], ),
        sa.ForeignKeyConstraint(['id_activo'], ['activos.id'], ),
        sa.ForeignKeyConstraint(['id_contrato'], ['contratos.id'], ),
        sa.ForeignKeyConstraint(['modificado_por'], ['usuarios.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_asignaciones_activo_id'), 'asignaciones_activo', ['id'], unique=False)

    op.create_table('pagos',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('id_contrato', sa.Integer(), nullable=False),
        sa.Column('concepto', sa.String(length=200), nullable=False),
        sa.Column('monto', sa.Float(), nullable=False),
        sa.Column('fecha', sa.Date(), nullable=False),
        sa.Column('estado', sa.Enum('PENDIENTE', 'PAGADO', 'VENCIDO', name='estadopago'), nullable=False),
        sa.ForeignKeyConstraint(['id_contrato'], ['contratos.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_pagos_id'), 'pagos', ['id'], unique=False)

    op.create_table('reportes_incidencia',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('fecha', sa.Date(), nullable=False),
        sa.Column('descripcion', sa.String(length=500), nullable=False),
        sa.Column('gravedad', sa.Enum('LEVE', 'MODERADO', 'GRAVE', name='gravedadincidencia'), nullable=False),
        sa.Column('url_foto', sa.String(length=500), nullable=True),
        sa.Column('estado', sa.Enum('ABIERTO', 'EN_ATENCION', 'CERRADO', name='estadoincidencia'), nullable=False),
        sa.Column('id_activo', sa.Integer(), nullable=False),
        sa.Column('creado_por', sa.Integer(), nullable=True),
        sa.Column('fecha_creacion', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.Column('modificado_por', sa.Integer(), nullable=True),
        sa.Column('fecha_modificacion', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.ForeignKeyConstraint(['creado_por'], ['usuarios.id'], ),
        sa.ForeignKeyConstraint(['id_activo'], ['activos.id'], ),
        sa.ForeignKeyConstraint(['modificado_por'], ['usuarios.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_reportes_incidencia_id'), 'reportes_incidencia', ['id'], unique=False)

    op.create_table('checklist_estado',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('id_asignacion', sa.Integer(), nullable=False),
        sa.Column('momento', sa.Enum('ENTREGA', 'DEVOLUCION', name='momentochecklist'), nullable=False),
        sa.Column('pantalla', sa.Enum('BIEN', 'RAYADO', 'ROTO', name='estadocomponente'), nullable=False),
        sa.Column('teclado', sa.Enum('BIEN', 'RAYADO', 'ROTO', name='estadocomponente'), nullable=False),
        sa.Column('carcasa', sa.Enum('BIEN', 'RAYADO', 'ROTO', name='estadocomponente'), nullable=False),
        sa.Column('cargador', sa.Boolean(), nullable=False),
        sa.Column('observaciones', sa.String(length=500), nullable=True),
        sa.Column('url_fotos', sa.String(length=500), nullable=True),
        sa.Column('id_usuario', sa.Integer(), nullable=False),
        sa.Column('fecha_registro', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.ForeignKeyConstraint(['id_asignacion'], ['asignaciones_activo.id'], ),
        sa.ForeignKeyConstraint(['id_usuario'], ['usuarios.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_checklist_estado_id'), 'checklist_estado', ['id'], unique=False)

    op.create_table('historial_ubicacion',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('id_asignacion', sa.Integer(), nullable=False),
        sa.Column('latitud', sa.Float(), nullable=False),
        sa.Column('longitud', sa.Float(), nullable=False),
        sa.Column('timestamp', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.ForeignKeyConstraint(['id_asignacion'], ['asignaciones_activo.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_historial_ubicacion_id'), 'historial_ubicacion', ['id'], unique=False)

    op.create_table('mantenimientos',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('tipo', sa.Enum('PREVENTIVO', 'CORRECTIVO', name='tipomantenimiento'), nullable=False),
        sa.Column('fecha', sa.Date(), nullable=False),
        sa.Column('costo', sa.Float(), nullable=True),
        sa.Column('descripcion', sa.String(length=500), nullable=True),
        sa.Column('url_foto', sa.String(length=500), nullable=True),
        sa.Column('id_activo', sa.Integer(), nullable=False),
        sa.Column('frecuencia_dias', sa.Integer(), nullable=True),
        sa.Column('proxima_fecha', sa.Date(), nullable=True),
        sa.Column('id_reporte_origen', sa.Integer(), nullable=True),
        sa.Column('tiempo_reparacion', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['id_activo'], ['activos.id'], ),
        sa.ForeignKeyConstraint(['id_reporte_origen'], ['reportes_incidencia.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_mantenimientos_id'), 'mantenimientos', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_mantenimientos_id'), table_name='mantenimientos')
    op.drop_table('mantenimientos')
    op.drop_index(op.f('ix_historial_ubicacion_id'), table_name='historial_ubicacion')
    op.drop_table('historial_ubicacion')
    op.drop_index(op.f('ix_checklist_estado_id'), table_name='checklist_estado')
    op.drop_table('checklist_estado')
    op.drop_index(op.f('ix_reportes_incidencia_id'), table_name='reportes_incidencia')
    op.drop_table('reportes_incidencia')
    op.drop_index(op.f('ix_pagos_id'), table_name='pagos')
    op.drop_table('pagos')
    op.drop_index(op.f('ix_asignaciones_activo_id'), table_name='asignaciones_activo')
    op.drop_table('asignaciones_activo')
    op.drop_index(op.f('ix_contratos_id'), table_name='contratos')
    op.drop_table('contratos')
    op.drop_index(op.f('ix_activos_id'), table_name='activos')
    op.drop_index(op.f('ix_activos_codigo_inventario'), table_name='activos')
    op.drop_table('activos')
    op.drop_index(op.f('ix_usuarios_id'), table_name='usuarios')
    op.drop_index(op.f('ix_usuarios_email'), table_name='usuarios')
    op.drop_table('usuarios')
    op.drop_table('roles_permisos')
    op.drop_index(op.f('ix_roles_id'), table_name='roles')
    op.drop_table('roles')
    op.drop_index(op.f('ix_permisos_id'), table_name='permisos')
    op.drop_table('permisos')
    op.drop_index(op.f('ix_clientes_nit'), table_name='clientes')
    op.drop_index(op.f('ix_clientes_id'), table_name='clientes')
    op.drop_table('clientes')
    op.drop_constraint('fk_categoria_padre', 'categorias_activo', type_='foreignkey')
    op.drop_index(op.f('ix_categorias_activo_id'), table_name='categorias_activo')
    op.drop_table('categorias_activo')
