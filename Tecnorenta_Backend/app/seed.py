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
        {"nombre": "reportes.listar", "descripcion": "Listar reportes"},
        {"nombre": "reportes.crear", "descripcion": "Crear reportes"},
        {"nombre": "clientes.listar", "descripcion": "Listar clientes"},
        {"nombre": "clientes.crear", "descripcion": "Crear clientes"},
    ]
    for p in permisos_data:
        existing = db.query(Permiso).filter(Permiso.nombre == p["nombre"]).first()
        if not existing:
            db.add(Permiso(**p))


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
        seed_admin(db, roles_ids)
        db.commit()
        print("Seed data inserted successfully")
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
