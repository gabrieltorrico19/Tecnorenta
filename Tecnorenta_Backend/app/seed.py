from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.core.security import hash_password
from app.models.rol import Rol, Permiso
from app.models.usuario import Usuario
from app.models.contrato import EstadoContrato
from app.models.activo import EstadoActivo
from app.models.pago import EstadoPago
from app.models.reporte_incidencia import GravedadIncidencia, EstadoIncidencia
from app.models.checklist_estado import MomentoChecklist, EstadoComponente
from app.models.mantenimiento import TipoMantenimiento


def seed_roles(db: Session) -> dict[str, int]:
    roles_data = [
        {"nombre": "Administrador"},
        {"nombre": "Gerente"},
        {"nombre": "Almacén"},
        {"nombre": "Técnico"},
        {"nombre": "Operador"},
        {"nombre": "Cliente"},
    ]
    roles_ids = {}
    for r in roles_data:
        existing = db.query(Rol).filter(Rol.nombre == r["nombre"]).first()
        if not existing:
            rol = Rol(**r)
            db.add(rol)
            db.flush()
            roles_ids[r["nombre"]] = rol.id
        else:
            roles_ids[r["nombre"]] = existing.id
    return roles_ids


def seed_permisos(db: Session) -> None:
    permisos_data = [
        {"nombre": "usuarios.listar", "descripcion": "Listar usuarios"},
        {"nombre": "usuarios.crear", "descripcion": "Crear usuarios"},
        {"nombre": "usuarios.editar", "descripcion": "Editar usuarios"},
        {"nombre": "usuarios.eliminar", "descripcion": "Eliminar usuarios"},
        {"nombre": "activos.listar", "descripcion": "Listar activos"},
        {"nombre": "activos.crear", "descripcion": "Crear activos"},
        {"nombre": "activos.editar", "descripcion": "Editar activos"},
        {"nombre": "activos.eliminar", "descripcion": "Eliminar activos"},
        {"nombre": "contratos.listar", "descripcion": "Listar contratos"},
        {"nombre": "contratos.crear", "descripcion": "Crear contratos"},
        {"nombre": "contratos.editar", "descripcion": "Editar contratos"},
        {"nombre": "contratos.eliminar", "descripcion": "Eliminar contratos"},
        {"nombre": "reportes.listar", "descripcion": "Listar reportes/incidencias"},
        {"nombre": "reportes.crear", "descripcion": "Crear reportes/incidencias"},
        {"nombre": "reportes.editar", "descripcion": "Editar reportes/incidencias"},
        {"nombre": "reportes.eliminar", "descripcion": "Eliminar reportes/incidencias"},
        {"nombre": "clientes.listar", "descripcion": "Listar clientes"},
        {"nombre": "clientes.crear", "descripcion": "Crear clientes"},
        {"nombre": "clientes.editar", "descripcion": "Editar clientes"},
        {"nombre": "clientes.eliminar", "descripcion": "Eliminar clientes"},
        {"nombre": "categorias.listar", "descripcion": "Listar categorías"},
        {"nombre": "categorias.crear", "descripcion": "Crear categorías"},
        {"nombre": "categorias.editar", "descripcion": "Editar categorías"},
        {"nombre": "categorias.eliminar", "descripcion": "Eliminar categorías"},
        {"nombre": "pagos.listar", "descripcion": "Listar pagos"},
        {"nombre": "pagos.crear", "descripcion": "Registrar pagos"},
        {"nombre": "pagos.editar", "descripcion": "Editar pagos"},
        {"nombre": "asignaciones.listar", "descripcion": "Listar asignaciones"},
        {"nombre": "asignaciones.crear", "descripcion": "Crear asignaciones"},
        {"nombre": "mantenimientos.listar", "descripcion": "Listar mantenimientos"},
        {"nombre": "mantenimientos.crear", "descripcion": "Crear mantenimientos"},
        {"nombre": "mantenimientos.editar", "descripcion": "Editar mantenimientos"},
        {"nombre": "dashboard.ver", "descripcion": "Ver dashboard y estadísticas"},
    ]
    for p in permisos_data:
        existing = db.query(Permiso).filter(Permiso.nombre == p["nombre"]).first()
        if not existing:
            db.add(Permiso(**p))


def seed_permisos_asignacion(db: Session, roles_ids: dict[str, int]) -> None:
    from app.models.rol import rol_permiso

    permisos_db = {p.nombre: p.id for p in db.query(Permiso).all()}

    asignacion = {
        "Administrador": list(permisos_db.keys()),
        "Gerente": [
            "contratos.listar", "contratos.crear", "contratos.editar",
            "clientes.listar", "clientes.crear", "clientes.editar",
            "reportes.listar", "reportes.crear",
            "activos.listar",
            "pagos.listar", "pagos.crear",
            "dashboard.ver",
        ],
        "Almacén": [
            "activos.listar", "activos.crear", "activos.editar", "activos.eliminar",
            "categorias.listar", "categorias.crear", "categorias.editar",
            "asignaciones.listar", "asignaciones.crear",
            "reportes.listar",
            "dashboard.ver",
        ],
        "Técnico": [
            "reportes.listar", "reportes.crear", "reportes.editar",
            "mantenimientos.listar", "mantenimientos.crear", "mantenimientos.editar",
            "activos.listar",
            "asignaciones.listar",
            "dashboard.ver",
        ],
        "Operador": [
            "contratos.listar", "contratos.crear", "contratos.editar",
            "clientes.listar", "clientes.crear",
            "reportes.listar", "reportes.crear",
            "activos.listar",
            "pagos.listar",
            "dashboard.ver",
        ],
        "Cliente": [],
    }
    for rol_nombre, permiso_nombres in asignacion.items():
        rol_id = roles_ids.get(rol_nombre)
        if not rol_id:
            continue
        for permiso_nombre in permiso_nombres:
            permiso_id = permisos_db.get(permiso_nombre)
            if not permiso_id:
                continue
            existing = db.execute(
                rol_permiso.select().where(
                    rol_permiso.c.id_rol == rol_id,
                    rol_permiso.c.id_permiso == permiso_id,
                )
            ).first()
            if not existing:
                db.execute(rol_permiso.insert().values(id_rol=rol_id, id_permiso=permiso_id))


def seed_admin(db: Session, roles_ids: dict[str, int]) -> None:
    existing = db.query(Usuario).filter(Usuario.email == "admin@tecnorenta.com").first()
    if not existing:
        admin = Usuario(
            nombre="Administrador",
            email="admin@tecnorenta.com",
            password_hash=hash_password("admin123"),
            telefono="000000000",
            activo=True,
            id_rol=roles_ids["Administrador"],
        )
        db.add(admin)


def main() -> None:
    db = SessionLocal()
    try:
        roles_ids = seed_roles(db)
        seed_permisos(db)
        seed_permisos_asignacion(db, roles_ids)
        seed_admin(db, roles_ids)
        db.commit()
        print(f"Seed data: {len(roles_ids)} roles, permisos asignados")
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
