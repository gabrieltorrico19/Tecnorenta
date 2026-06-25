from datetime import date, timedelta
from random import choice, uniform, randint

from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.core.security import hash_password
from app.models.cliente import Cliente
from app.models.categoria_activo import CategoriaActivo
from app.models.activo import Activo
from app.models.contrato import Contrato
from app.models.pago import Pago
from app.models.asignacion_activo import AsignacionActivo
from app.models.reporte_incidencia import ReporteIncidencia
from app.models.usuario import Usuario


def seed_clientes(db: Session) -> list[Cliente]:
    data = [
        {"razon_social": "TechSolutions SRL", "nit": "1023457011", "direccion": "Av. Ballivián 123, Santa Cruz", "latitud": -17.7833, "longitud": -63.1825, "sector": "Centro"},
        {"razon_social": "DataCenter Bolivia", "nit": "2015678022", "direccion": "Calle Potosí 456, La Paz", "latitud": -16.5000, "longitud": -68.1500, "sector": "Sopocachi"},
        {"razon_social": "NetLogic Solutions", "nit": "3045789033", "direccion": "Av. Prado 789, Cochabamba", "latitud": -17.3935, "longitud": -66.1570, "sector": "Queru Queru"},
        {"razon_social": "Grupo InnovaTech", "nit": "4056891044", "direccion": "Calle Comercio 321, Santa Cruz", "latitud": -17.7894, "longitud": -63.1974, "sector": "Equipetrol"},
        {"razon_social": "Sistemas del Sur", "nit": "5067902055", "direccion": "Av. Integración 654, Tarija", "latitud": -21.5315, "longitud": -64.7296, "sector": "Centro"},
        {"razon_social": "Cloud Works SA", "nit": "6078913066", "direccion": "Calle 21 de Mayo 987, La Paz", "latitud": -16.4944, "longitud": -68.1357, "sector": "Zona Sur"},
        {"razon_social": "TecnoExpress Ltda", "nit": "7089024077", "direccion": "Av. Busch 147, Santa Cruz", "latitud": -17.7755, "longitud": -63.1750, "sector": "El Pourrí"},
        {"razon_social": "ByteCorp Bolivia", "nit": "8090135088", "direccion": "Calle Colombia 258, Cochabamba", "latitud": -17.3800, "longitud": -66.1500, "sector": "Norte"},
        {"razon_social": "Digital Solutions", "nit": "9101246099", "direccion": "Av. San Martín 369, Santa Cruz", "latitud": -17.7800, "longitud": -63.1600, "sector": "Urb. Los Olivos"},
        {"razon_social": "InfraNet Group", "nit": "1012357000", "direccion": "Calle Junín 741, Sucre", "latitud": -19.0333, "longitud": -65.2627, "sector": "Recoleta"},
    ]
    clientes = []
    for d in data:
        existing = db.query(Cliente).filter(Cliente.nit == d["nit"]).first()
        if not existing:
            c = Cliente(**d)
            db.add(c)
            db.flush()
            clientes.append(c)
    return clientes or db.query(Cliente).all()


def seed_categorias(db: Session) -> dict[str, int]:
    cats = {}
    padres = [
        {"nombre": "Laptops", "nivel": "1", "descripcion": "Equipos portátiles"},
        {"nombre": "Accesorios", "nivel": "1", "descripcion": "Periféricos y accesorios"},
    ]
    for p in padres:
        existing = db.query(CategoriaActivo).filter(CategoriaActivo.nombre == p["nombre"], CategoriaActivo.nivel == "1").first()
        if not existing:
            cat = CategoriaActivo(**p)
            db.add(cat)
            db.flush()
            existing = cat
        cats[p["nombre"]] = existing.id

    hijos = [
        {"nombre": "Laptops Gamer", "nivel": "2", "descripcion": "Alto rendimiento", "id_categoria_padre": cats["Laptops"]},
        {"nombre": "Laptops Oficina", "nivel": "2", "descripcion": "Uso corporativo", "id_categoria_padre": cats["Laptops"]},
        {"nombre": "Laptops Ultraligeras", "nivel": "2", "descripcion": "Portabilidad extrema", "id_categoria_padre": cats["Laptops"]},
        {"nombre": "Monitores", "nivel": "2", "descripcion": "Pantallas externas", "id_categoria_padre": cats["Accesorios"]},
    ]
    for h in hijos:
        existing = db.query(CategoriaActivo).filter(CategoriaActivo.nombre == h["nombre"]).first()
        if not existing:
            cat = CategoriaActivo(**h)
            db.add(cat)
            db.flush()
            cats[h["nombre"]] = cat.id
        else:
            cats[h["nombre"]] = existing.id
    return cats


def seed_activos(db: Session, cats: dict[str, int]) -> list[Activo]:
    modelos = [
        ("LPT-GAM-001", "Alienware M18", "SN-AW18-0001", cats.get("Laptops Gamer", 1)),
        ("LPT-GAM-002", "ASUS ROG Strix G16", "SN-ROG16-0002", cats.get("Laptops Gamer", 1)),
        ("LPT-GAM-003", "MSI Raider GE78", "SN-MSI78-0003", cats.get("Laptops Gamer", 1)),
        ("LPT-OFC-001", "Lenovo ThinkPad X1", "SN-LENX1-0004", cats.get("Laptops Oficina", 2)),
        ("LPT-OFC-002", "Dell Latitude 5540", "SN-DEL5540-5", cats.get("Laptops Oficina", 2)),
        ("LPT-OFC-003", "HP EliteBook 840", "SN-HP840-0006", cats.get("Laptops Oficina", 2)),
        ("LPT-OFC-004", "Lenovo ThinkPad T14", "SN-T14-0007", cats.get("Laptops Oficina", 2)),
        ("LPT-OFC-005", "Dell Latitude 7440", "SN-DEL7440-8", cats.get("Laptops Oficina", 2)),
        ("LPT-ULT-001", "MacBook Air M3", "SN-MBA-M3-009", cats.get("Laptops Ultraligeras", 3)),
        ("LPT-ULT-002", "LG Gram 16", "SN-LG16-0010", cats.get("Laptops Ultraligeras", 3)),
        ("LPT-ULT-003", "Samsung Galaxy Book3", "SN-SAMGB3-011", cats.get("Laptops Ultraligeras", 3)),
        ("LPT-ULT-004", "ASUS ZenBook 14", "SN-ZEN14-012", cats.get("Laptops Ultraligeras", 3)),
        ("LPT-GAM-004", "Razer Blade 16", "SN-RAZ16-013", cats.get("Laptops Gamer", 1)),
        ("LPT-OFC-006", "Huawei MateBook 14", "SN-HW14-0014", cats.get("Laptops Oficina", 2)),
        ("LPT-ULT-005", "Acer Swift 5", "SN-ACSW5-015", cats.get("Laptops Ultraligeras", 3)),
        ("LPT-GAM-005", "Gigabyte Aorus 17", "SN-GIG17-016", cats.get("Laptops Gamer", 1)),
        ("LPT-OFC-007", "Fujitsu Lifebook U7", "SN-FUJ-U7-017", cats.get("Laptops Oficina", 2)),
        ("LPT-ULT-006", "Microsoft Surface Laptop 5", "SN-SRF5-018", cats.get("Laptops Ultraligeras", 3)),
        ("LPT-GAM-006", "Lenovo Legion Pro 7", "SN-LEG7-019", cats.get("Laptops Gamer", 1)),
        ("LPT-OFC-008", "Dell Inspiron 16", "SN-DELIN-020", cats.get("Laptops Oficina", 2)),
    ]
    estados = ["disponible", "rentado", "mantenimiento", "disponible"]
    activos = []
    for cod, modelo, serie, cat_id in modelos:
        existing = db.query(Activo).filter(Activo.codigo_inventario == cod).first()
        if not existing:
            a = Activo(
                codigo_inventario=cod,
                modelo=modelo,
                numero_serie=serie,
                estado=choice(estados),
                fecha_compra=date(2024, randint(1, 12), randint(1, 28)),
                valor_depreciado=round(uniform(0, 2500), 2),
                id_categoria=cat_id,
            )
            db.add(a)
            db.flush()
            activos.append(a)
    return activos or db.query(Activo).all()


def seed_contratos(db: Session, clientes: list[Cliente]) -> list[Contrato]:
    data = [
        (5, 4000, "Uso exclusivo para desarrollo de software", "activo"),
        (3, 2500, "Equipo para diseño gráfico", "activo"),
        (4, 3200, "Uso corporativo 24/7", "activo"),
        (2, 1800, "Trabajo remoto - facturación mensual", "activo"),
        (5, 5500, "Servidor de pruebas", "vencido"),
        (1, 2800, "Oficina administrativa", "activo"),
        (4, 3500, "Desarrollo y testing", "activo"),
        (3, 2100, "Uso educativo", "cancelado"),
    ]
    contratos = []
    for idx, (cli_idx, monto, cond, estado) in enumerate(data):
        cliente = clientes[cli_idx % len(clientes)]
        inicio = date(2025, 1 + idx % 12, 1)
        fin = inicio + timedelta(days=30 * (randint(6, 12)))
        c = Contrato(
            fecha_inicio=inicio,
            fecha_fin=fin,
            condiciones_uso=cond,
            estado=estado,
            monto_mensual=monto,
            id_cliente=cliente.id,
        )
        db.add(c)
        db.flush()
        contratos.append(c)
    return contratos


def seed_pagos(db: Session, contratos: list[Contrato]) -> None:
    estados_pago = ["pagado", "pagado", "pagado", "pendiente"]
    for cont in contratos[:6]:
        for mes in range(1, 4):
            existing = db.query(Pago).filter(
                Pago.id_contrato == cont.id,
                Pago.concepto == f"Cuota mes {mes}",
            ).first()
            if not existing:
                p = Pago(
                    id_contrato=cont.id,
                    concepto=f"Cuota mes {mes}",
                    monto=cont.monto_mensual,
                    fecha=date(2025, mes, 5),
                    estado=choice(estados_pago),
                )
                db.add(p)


def seed_asignaciones(db: Session, contratos: list[Contrato], activos: list[Activo]) -> None:
    existing_count = db.query(AsignacionActivo).count()
    if existing_count > 0:
        return
    for i in range(10):
        contrato = choice(contratos)
        activo = choice(activos)
        asig = AsignacionActivo(
            fecha_asignacion=contrato.fecha_inicio + timedelta(days=randint(0, 5)),
            id_contrato=contrato.id,
            id_activo=activo.id,
            latitud=-17.38 + uniform(-0.5, 0.5),
            longitud=-66.15 + uniform(-0.5, 0.5),
        )
        db.add(asig)


def seed_reportes(db: Session, activos: list[Activo]) -> None:
    data = [
        ("Pantalla con píxeles muertos en esquina superior derecha", "leve", "abierto"),
        ("Teclado no responde teclas WASD después de derrame de café", "moderado", "en_atencion"),
        ("Equipo no enciende, posible falla de motherboard", "grave", "abierto"),
        ("Batería dura menos de 30 minutos", "moderado", "cerrado"),
        ("Cargador original dañado, requiere reemplazo", "leve", "cerrado"),
    ]
    existing_count = db.query(ReporteIncidencia).count()
    if existing_count > 0:
        return
    for desc, grav, est in data:
        r = ReporteIncidencia(
            fecha=date(2025, randint(1, 6), randint(1, 28)),
            descripcion=desc,
            gravedad=grav,
            url_foto="https://placehold.co/600x400?text=foto_incidencia",
            estado=est,
            id_activo=choice(activos).id,
        )
        db.add(r)


def main() -> None:
    db = SessionLocal()
    try:
        clientes = seed_clientes(db)
        cats = seed_categorias(db)
        activos = seed_activos(db, cats)
        contratos = seed_contratos(db, clientes)
        seed_pagos(db, contratos)
        seed_asignaciones(db, contratos, activos)
        seed_reportes(db, activos)
        db.commit()
        print(f"Seed data: {len(clientes)} clientes, {len(activos)} activos, {len(contratos)} contratos")
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
